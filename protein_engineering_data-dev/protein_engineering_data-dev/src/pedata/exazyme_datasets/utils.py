from math import isqrt
from datasets import Dataset
import numpy as np

from pedata.exazyme_datasets import (
    append_split_columns_to_dataset,
)
from pedata.config import add_encodings


def append_index_column_to_dataset(dataset: Dataset) -> Dataset:
    """Add an index column to the dataset
    Args:
        dataset: dataset to add index column to

    Returns:
        ds.Dataset: dataset with index column added

    Raises:
        TypeError: If the input type is not datasets.Dataset.
    """
    if not isinstance(dataset, Dataset):
        raise TypeError(
            f"Input a valid dataset -> datasets.Dataset - here is {type(dataset)}"
        )

    if "index" not in dataset.column_names:
        return dataset.add_column("index", np.arange(dataset.num_rows))
    else:
        return dataset


def dataset_base_processing(
    dataset: Dataset,
    needed_encodings: list[str] | set[str] = [],
    add_index: bool = True,
    add_splits: bool = True,
) -> Dataset:
    """Perform base processing on the dataset
    Args
        dataset: dataset to process
        add_index: whether to add an index column to the dataset
        add_splits: whether to add split columns to the dataset
        needed_encoding: encodings to add to the dataset
    Returns:
        ds.Dataset: processed dataset
    Raises:
        TypeError: If the input is not a valid dataset or dictionary of datasets.
    """
    if not isinstance(dataset, Dataset):
        raise TypeError(
            f"Input a valid dataset -> datasets.Dataset - here is {type(dataset)}"
        )

    # Add encodings to dataset
    dataset = add_encodings(dataset, needed=needed_encodings)

    if add_index:
        # Add index column to dataset
        dataset = append_index_column_to_dataset(dataset)

    if add_splits:
        # Add split columns to dataset
        dataset = append_split_columns_to_dataset(dataset)

    return dataset


if __name__ == "__main__":
    pass
