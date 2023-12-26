import argparse
import os
import numpy as np
from typing import Sequence
from datasets import load_dataset, Dataset

from huggingface_hub import hf_hub_download, HfApi
from pedata.disk_cache import preprocess_data
from pedata.util import get_target

from pedata.exazyme_datasets.constants import README_FORMATTING
from pedata.exazyme_datasets import dataset_base_processing
from pedata.exazyme_datasets.vis import plot_target_distributions
from datasets import concatenate_datasets


# FIXME - DELETE DATASET WHEN single split and NAME IS CHANGED to whole_dataset


class DatasetUpload:
    """A class to handle dataset creation, update and upload to Hugging Face Hub.
    Note:
    Usage from the command line:
    Required argument:
        --repo, Name of the repository on Hugging Face
    None required arguments:
        --filename, Path to the CSV file for dataset creation. default=None,
        --local_dir, Name of the local directory to save the dataset to. default="./local_datasets",
        --save_locally, Name of the local directory to save the dataset to. default=True,

    Example usage:
        ```bash
        python examples/dataset_upload.py --repo Exazyme/test_example_dataset_ha1 --filename examples/datasets/test_example_dataset_ha1.csv
        ```
    """

    def __init__(
        self,
        repo: str,
        local_dir: str = "./local_datasets",
        csv_filename: str = None,
        save_locally: bool = True,
        splits_to_combine_as_whole_ds: list = [],
    ):
        """Initialize the class and run the creation, update and upload pipeline.
        Args:
            repo (str): Hugging Face Hub repository name (format: 'Exazyme/dataset-name').
            local_dir (str): Local directory to save the dataset to.
            csv_filename (str): Path to the CSV file for dataset creation.
                if None, the dataset is pulled from Hugging Face Hub and updated. - default: None
            save_locally (bool): Whether to save the dataset to a local directory. - default: True
            splits_to_combine_as_whole_ds: The name of the splits to combine as the whole dataset
                - when updating a dataset which is already on the hub. - default: []
        """

        self._repo = repo
        self._local_dir = local_dir
        self._csv_filename = csv_filename
        self._save_locally = save_locally
        self._whole_split_name = "whole_dataset"
        self._splits_to_combine_as_whole_ds = splits_to_combine_as_whole_ds
        self._init_process()

    def _init_process(self):
        if self._csv_filename is not None:
            self._dataset = self.create_and_preprocess(self._csv_filename)
        else:
            self._dataset = self.pull_and_update(
                self._repo,
                whole_split_name=self._whole_split_name,
                splits_to_combine_as_whole_ds=self._splits_to_combine_as_whole_ds,
            )

    @property
    def local_path(self):
        return os.path.join(self._local_dir, self._repo)

    @property
    def figure_path(self):
        return os.path.join(self.local_path, "figures")

    def process(self, verbose=True, readme=True):
        """Run the creation, update and upload pipeline."""
        if verbose:
            print(self.__repr__())

        # create local directory
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)

        if readme:
            # create the figures directory
            os.makedirs(f"{self.local_path}/figures", exist_ok=True)

        # save
        if self._save_locally:
            self.save(self._dataset, self.local_path)

        # push
        self.push(self._dataset, self._repo)

        if verbose:
            print(self.__repr__())

        if readme:
            self.update_readme()

    def make_read_me_figures(self):
        plot_target_distributions(self.targets, savedir=self.local_path)

    def update_readme(self):
        """Update the readme file"""
        readme = ReadMe(local_dir=self.local_path)
        readme.pull_readme_from_hub(repo_id=self._repo)

        readme.update_readme(self.datapoints_n, "datapoints")
        readme.update_readme(self.feature_names, "embeddings")
        readme.update_readme(self.target_names, "targets")
        readme.update_readme(self.available_splits, "available_splits")

        self.make_read_me_figures()

        readme.update_readme_figures(figure_path=self.figure_path)
        readme.push_figures_to_hub()
        readme.push_readme_to_hub(repo_id=self._repo)

    def __repr__(self):
        """Print the processing to be done or the processing done."""

        def print_list(l):
            return "\n".join([f" - {item}" for item in l])

        if "_dataset" not in self.__dict__:
            return f"""
------------------------------------
DatasetUpload - Processing to be done
------------------------------------
- repo={self._repo} 
- local_dir={self._local_dir}
- csv_filename={self._csv_filename}
- save_locally={self._save_locally}
            """
        else:
            return f"""
-------------------------------
DatasetUpload - Processing done
-------------------------------
Saved locally: {self.local_path}
Pushed to the huggingface repository: {self._repo}
Available features:
{print_list(self.feature_names)}
Available targets: 
{print_list(self.target_names)}
Available splits:
{print_list(self.available_splits)}
            """

    @property
    def target_names(self) -> list[str]:
        """get all target names"""
        targets = get_target(self._dataset, as_dict=True)
        return list(targets.keys())

    @property
    def targets(self) -> dict[Sequence[str], np.ndarray]:
        """Getting all targets
        Returns:
            Dictionary of targets with the target names as keys and the target values as values
        """
        return get_target(self._dataset, as_dict=True)

    @property
    def available_splits(self) -> list[str]:
        """get all available splits"""
        return [col for col in self._dataset.column_names if "split" in col]

    @property
    def feature_names(self) -> list[str]:
        """get all features names"""
        return [
            col
            for col in self._dataset.column_names
            if not (
                col in self.target_names
                or col in self.available_splits
                or col in ["index"]
            )
        ]

    @property
    def datapoints_n(self) -> list[int]:
        """get the number of datapoints"""
        return [self._dataset.num_rows]

    @staticmethod
    def create_and_preprocess(csv_filename: str) -> Dataset:
        """Create a dataset from a CSV file and push it to Hugging Face.
        Args:
            filename (str): Path to the CSV file.
        Returns:
            ds.Dataset: Dataset created from the CSV file.
        """
        # Convert CSV to Hugging Face dataset
        return preprocess_data(csv_filename, add_index=True, add_splits=True)

        # print(f"Dataset '{repo}' successfully pushed to Hugging Face.")

    @staticmethod
    def pull_and_update(
        repo: str,
        whole_split_name: str = "whole_dataset",
        splits_to_combine_as_whole_ds: list = [],
    ) -> Dataset:
        """Pull a dataset from Hugging Face, update it.
        Args:
            repo (str): Hugging Face Hub repository name (format: 'Exazyme/dataset-name').
        returns:
            ds.Dataset: Dataset pulled from Hugging Face.
        """
        # Pull dataset from Hugging Face
        # concatenate_datasets makes sure that the dataset is a dataset and not a dataset dictionary (which is the case when pulling from the hub)
        dataset_dict = load_dataset(f"{repo}")
        splits_already_in_dataset = list(dataset_dict.keys())
        # return the dataset in the a dataset dictionary with the whole dataset as one split named 'whole_dataset'

        if len(dataset_dict) > 1 and whole_split_name not in splits_already_in_dataset:
            raise ValueError(
                f"DatasetDict has more than one split and does not have a split named {whole_split_name}."
                "Use splits_to_combine_as_whole_ds as argument to specify which splits to combine."
            )

        if splits_to_combine_as_whole_ds == []:
            splits_to_combine_as_whole_ds = splits_already_in_dataset

        dataset = concatenate_datasets(
            [dataset_dict[ds] for ds in splits_to_combine_as_whole_ds]
        )

        return dataset_base_processing(dataset)

    @staticmethod
    def save(dataset: Dataset, local_path: str) -> None:
        """Save a dataset to a local directory and push it to Hugging Face.
        Args:
            dataset (ds.Dataset): Dataset to save and push.
            local_dir (str): Local directory to save the dataset to."""

        # Save to a local directory
        dataset.save_to_disk(local_path)

    @staticmethod
    def push(dataset: Dataset, repo: str = None) -> None:
        """Save a dataset to a local directory and push it to Hugging Face.
        Args:
            dataset (ds.Dataset): Dataset to save and push.
            repo (str): Hugging Face Hub repository name (format: 'Exazyme/dataset-name').
        """
        # push to hub
        dataset.push_to_hub(
            repo, private=True, split="whole_dataset", embed_external_files=False
        )


class ReadMe:
    """A class to handle the readme file"""

    def __init__(self, local_dir: str = None):
        """Initialize the class

        Args:
            local_dir (str): The local folder containing the readme file.

        Raises:
            ValueError: readme_path must be specified
        """
        if local_dir is None:
            raise ValueError("readme_path must be specified")

        self._local_dir = os.path.abspath(local_dir)
        self._readme_path = os.path.join(local_dir, "README.md")
        self._readme_content = ""

    @property
    def readme_content(self):
        """The content of the readme"""
        return self._readme_content

    @property
    def readme_path(self):
        """The path to the readme file"""
        return self._readme_path

    @property
    def figure_path(self):
        """The path to the figures"""
        return self._figure_path

    @staticmethod
    def insert_section(section_start, section_end, updated_section, readme_content):
        """Insert the updated section in the readme

        Args:
            section_start: The start of the section to update
            section_end: The end of the section to update
            updated_section: The updated section
            readme_content: The content of the readme

        Returns:
            The updated content of the readme
        """
        return (
            readme_content[:section_start]
            + updated_section
            + readme_content[section_end:]
        )

    @staticmethod
    def write_readme(readme_path, updated_readme_content):
        """Write the updated readme content to the readme file

        Args:
            readme_path: The path to the readme file
            updated_readme_content: The updated content of the readme
        """
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_readme_content)

    def create_readme():
        # TODO
        pass

    def pull_readme_from_hub(self, repo_id: str = None, repo_type="dataset") -> None:
        """Pulls the readme file from the hub into the local directory

        Args:
            repo_id: The id of the repo to pull the readme from
            repo_type: The type of repo to pull the readme from. Defaults to "dataset"

        Returns:
            None
        """
        if repo_id is None:
            raise ValueError("repo_id must be provided")

        self.repo_id = repo_id
        self.repo_type = repo_type

        _ = hf_hub_download(
            repo_id=repo_id,
            filename="README.md",
            repo_type=self.repo_type,
            local_dir=self._local_dir,
        )
        # return the path to the readme file
        self._readme_path = os.path.join(self._local_dir, "README.md")
        return self.readme_path

    def update_readme(
        self,
        section_elements: list,
        section_name: str = "features",
    ) -> None:
        """Update the section of the readme with the updated information

        Args:
            section_list (list): The updated features section
            section_name (str): The name of the section to update.
        """
        with open(self.readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()

        # Create the new section
        element_info = "".join(
            [
                f"- {element}{README_FORMATTING['in_section_sep']}"
                for element in section_elements
            ]
        )

        # Find and replace the element section with the updated information
        section_start = readme_content.find(f"{README_FORMATTING[section_name]}")
        section_end = readme_content.find("\n\n\n", section_start)
        updated_section = f"{README_FORMATTING[section_name]}{README_FORMATTING['section_end']}{element_info}{README_FORMATTING['section_end']}"

        self._readme_content = self.insert_section(
            section_start, section_end, updated_section, readme_content
        )
        self.write_readme(self.readme_path, self._readme_content)

    def push_readme_to_hub(
        self,
        repo_id: str = None,
        verbose=True,
    ) -> None:
        """Pushes the readme file to the hub

        Args:
            readme_path: The path to the readme file. If None, defaults to
                the README.md file in the current directory
            repo_id: The id of the repo to push the readme to
                default to None, which sets it to the repo_id used to pull the readme

        Returns:
            None

        """
        if repo_id is None:
            repo_id = self.repo_id

        api = HfApi()
        api.upload_file(
            path_or_fileobj=self.readme_path,
            path_in_repo="README.md",
            repo_id=repo_id,
            repo_type=self.repo_type,
        )
        if verbose:
            print(f"Pushed {self.readme_path} to {repo_id}")

    def update_readme_figures(
        self,
        figure_path: str = None,
    ) -> None:
        """Update the figures section of the readme with the updated information

        Args:
            figure_path: The directory containing the figures to add to the readme

        Returns:
            None

        Raises:
            ValueError: figure_path must be specified
        """

        def make_relative_path(base_path, target_path):
            return os.path.relpath(target_path, os.path.dirname(base_path))

        if figure_path is None:
            raise ValueError("readme_path must be specified")

        self._figure_path = os.path.abspath(figure_path)
        self.figure_rel_path = make_relative_path(self.readme_path, figure_path)

        with open(self.readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()

        # Create the new section
        figure_names = os.listdir(figure_path)
        figure_info = "".join(
            [
                f'<img src="{self.figure_rel_path}/{figure_name}"> {README_FORMATTING["in_section_sep"]}'
                for figure_name in figure_names
            ]
        )

        # Find and replace the element section with the updated information
        section_start = readme_content.find(f"{README_FORMATTING['figures']}")
        section_end = readme_content.find("\n\n\n", section_start)

        updated_section = f"{README_FORMATTING['section_end']}{README_FORMATTING['figures']}{README_FORMATTING['in_section_sep']}{figure_info}{ README_FORMATTING['section_end']}"

        self._readme_content = self.insert_section(
            section_start, section_end, updated_section, readme_content
        )
        self.write_readme(self.readme_path, self._readme_content)

    def push_figures_to_hub(self):
        """Pushes the figures to the hub"""
        api = HfApi()
        api.upload_folder(
            folder_path=self._figure_path,
            path_in_repo=self.figure_rel_path,
            repo_id=self.repo_id,
            repo_type=self.repo_type,
        )


if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(
        description="Create and push a dataset to Hugging Face."
    )
    # required arguments
    parser.add_argument(
        "--repo",
        required=True,
        help="Name of the repository to pull from on Hugging Face.",
    )
    # optional arguments
    parser.add_argument(
        "--filename",
        required=False,
        help="Path to the CSV file for dataset creation.",
        default=None,
    )
    parser.add_argument(
        "--local_dir",
        required=False,
        help="Name of the local directory to save the dataset to.",
        default="./local_datasets",
    )
    parser.add_argument(
        "--save_locally",
        required=False,
        help="Name of the local directory to save the dataset to.",
        default=True,
    )

    args = parser.parse_args()
    print(args)
    # create dataset upload object
    data_upload = DatasetUpload(
        args.repo,
        csv_filename=args.filename,
        local_dir=args.local_dir,
        save_locally=args.save_locally,
    )

    # process dataset
    data_upload.process(verbose=True)

    # exmaple usage:
    # python examples/dataset_upload.py --repo Exazyme/test_example_dataset_ha1 --filename examples/datasets/test_example_dataset_ha1.csv
