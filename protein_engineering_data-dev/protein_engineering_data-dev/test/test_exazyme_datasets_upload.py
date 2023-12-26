from pedata.exazyme_datasets.upload import DatasetUpload
import subprocess

run_command_line_tests = False
# repo_name = "Exazyme/test_example_dataset_ha1"
repo_name = "Exazyme/exazyme_mockup"


def test_Dataset_upload():
    """processing an csv file,
    creating a dataset acccording to exazyme standards
    and uploading a dataset to a huggingface repository"""
    upload = DatasetUpload(
        repo="Exazyme/test_example_dataset_ha1",
        csv_filename="local_datasets/datafiles/example_dataset_ha1.csv",
    )
    upload.process()


def test_Dataset_update():
    """pulling dataset from huggingface,
    updating it according to exazyme standards and uploading to huggingface"""
    update = DatasetUpload(
        repo=repo_name,
    )
    update.process()


if run_command_line_tests:
    # These tests are redundant with the above tests
    # Keep them as an example to test how to run the commands in the command line
    def run_command(command):
        try:
            # Execute the command
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            # Raise a custom exception if the command fails
            raise Exception(f"Error executing the command: {e}")
        except Exception as e:
            # Handle any other exceptions here
            raise Exception(f"Error executing the command: {e}")

    # === same tests but in the command line ===
    def test_upload_csv_to_huggingface():
        """processing and csv file and uploading a dataset to a huggingface repository"""
        command = (
            "python "
            "src/pedata/exazyme_datasets/upload.py "
            "--repo Exazyme/test_example_dataset_ha1 "
            "--filename local_datasets/datafiles/example_dataset_ha1.csv"
        )
        run_command(command)

    def test_update_huggingface_dataset():
        """pulling a dataset from huggingface, updating it and uploading it uploading to the same repo"""

        command = (
            "python "
            "src/pedata/exazyme_datasets/upload.py "
            "--repo Exazyme/test_example_dataset_ha1"
        )
        run_command(command)
