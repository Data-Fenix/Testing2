import datasets
from datasets import load_dataset
import os

from pedata.exazyme_datasets.upload import ReadMe

from pedata.exazyme_datasets import (
    plot_target_distributions,
    append_index_column_to_dataset,
    append_split_columns_to_dataset,
)
from pedata.config import add_encodings
from pedata.util import get_target


if __name__ == "__main__":
    raise DeprecationWarning(
        "This script still works but it not intended to be used anymore."
    )
    # ========= Modifying a pre-existing dataset on the hub ============
    repo = "exazyme_mockup"
    update_README = True  # FIXME: needs to do it for all the sections
    push_README_to_hub = True
    update_dataset_to_hub = False  # TODO

    # current working directory
    cwd = os.getcwd()
    # local directory
    local_dir = os.path.join(cwd, f"examples/datasets/{repo}")
    # create the local directory
    os.makedirs(local_dir, exist_ok=True)
    # create the figures directory
    os.makedirs(f"{local_dir}/figures", exist_ok=True)

    # load dataset
    dataset = load_dataset(
        f"Exazyme/{repo}",
        cache_dir=local_dir,
    )  # when working online
    # dataset = load_dataset(
    #     "examples/datasets/exazyme_mockup/Exazyme___exazyme_mockup"
    # )  # when working offline

    assert isinstance(dataset, datasets.DatasetDict)

    # modify dataset
    # mock task: removing a column and adding it back as an encoding
    needed = ["aa_1gram"]
    for data_splits in dataset.keys():
        dataset[data_splits] = dataset[data_splits].remove_columns(needed)
    dataset = add_encodings(dataset, needed)

    # add index column
    dataset = append_index_column_to_dataset(dataset)

    # add split columns
    dataset = append_split_columns_to_dataset(dataset)

    assert isinstance(dataset, datasets.Dataset)

    # datapoints
    datapoints_n = [f"number of datapoints = {dataset.num_rows}"]

    # get target
    targets = get_target(dataset, as_dict=True)

    assert isinstance(targets, dict)

    # get all target names
    target_names = list(targets.keys())
    # get all features names
    feature_names = [
        col for col in dataset.column_names if col not in target_names + ["data_split"]
    ]

    ## plotting target distributions
    plot_target_distributions(targets, savedir=local_dir)

    if update_README:
        readME = ReadMe(local_dir=local_dir)
        readme_path = readME.pull_readme_from_hub(repo_id=f"Exazyme/{repo}")
        readME.update_readme(datapoints_n, "datapoints")
        readME.update_readme(feature_names, "embeddings")
        readME.update_readme(target_names, "targets")
        figure_path = f"{local_dir}/figures"
        readME.update_readme_figures(figure_path=figure_path)

        readME.push_figures_to_hub()
        readME.push_readme_to_hub()
        # print(readME.readme_content)
