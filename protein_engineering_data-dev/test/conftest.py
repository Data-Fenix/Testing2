from pytest import fixture
from pedata.static.example_data.example_data import RegressionToyDataset
from datasets import Dataset


@fixture()
def regr_dataset_train() -> Dataset:
    """Regression dataset - train split
    Args:
        needed_encodings (list): list of encodings needed for the model. Default: []
    Returns:
        dataset: train split"""
    ds = RegressionToyDataset()
    return ds.train


@fixture()
def regr_dataset_test() -> Dataset:
    """Regression dataset - test split
    Args:
        needed_encodings (list): list of encodings needed for the model. Default: []

    Returns:
        dataset: train split"""
    ds = RegressionToyDataset()
    return ds.test


@fixture()
def regr_dataset() -> Dataset:
    """Regression dataset - full dataset
    Args:
        needed_encodings (list): list of encodings needed for the model. Default: []
    Returns:
        dataset: train split"""
    ds = RegressionToyDataset()
    return ds.full_dataset
