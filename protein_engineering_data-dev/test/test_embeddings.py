from pedata.encoding.embeddings import ESM, Ankh

from datasets import Dataset
import pytest


@pytest.fixture()
def esm():
    return ESM()


@pytest.fixture()
def ankh():
    return Ankh()


@pytest.fixture()
def str_input():
    return "ATGC"


@pytest.fixture()
def empty_input():
    return []


@pytest.fixture()
def invalid_input():
    return [1, "GCTA", 2]


@pytest.fixture()
def valid_input_sequences():
    return ["ATGC", "GCTA"]


# ======= Esm tests =======


def test_esm_str_input(esm: ESM, str_input: str):
    """Test ESM class: raise ValueError when Non-list input
    Args:
        esm (ESM): ESM class
        str_input (str): string input
    """
    with pytest.raises(ValueError):
        esm.transform(str_input)


def test_esm_empty_in(esm: ESM, empty_input: list):
    """Test ESM class: raise ValueError when empty input
    Args:
        esm (ESM): ESM class
        empty_input (list): empty input
    """
    empty_input = []
    with pytest.raises(ValueError):
        esm.transform(empty_input)


def test_esm_invalid_input(esm: ESM, invalid_input: list):
    """Test ESM class: raise ValueError when invalid input, containing non-string values
    Args:
        esm (ESM): ESM class
        invalid_input (list): invalid input
    """
    with pytest.raises(ValueError):
        esm.transform(invalid_input)


def test_esm_valid_input(esm: ESM, valid_input_sequences: list):
    # Test case 4: Transforming valid input sequences
    transformed_sequences = esm.transform(valid_input_sequences)
    assert round(transformed_sequences[-1][-1][-1], 3) == round(-0.03196923807263374, 3)


def test_esm_on_dataset(esm: ESM, regr_dataset):
    # Test case 5: Loaded dataset Oshan/Uniref90_temp
    batch = regr_dataset[:2]
    assert round(esm.transform(batch["aa_seq"])[-1][-1][-1], 3) == round(-0.057, 3)


# ======= Ankh tests =======
def test_ankh_nonelist_input(ankh: Ankh, str_input: str):
    """Test Ankh class: raise ValueError when Non-list input
    Args:
        ankh (Ankh): Ankh class
        str_input (str): string input
    """
    with pytest.raises(ValueError):
        ankh.transform(str_input)


def test_ankh_empty_in(ankh, empty_input: list):
    """Test Ankh class: raise ValueError when empty input
    Args:
        ankh (Ankh): Ankh class
        empty_input (list): empty input
    """
    empty_input = []
    with pytest.raises(ValueError):
        ankh.transform(empty_input)


def test_ankh_invalid_input(ankh: Ankh, invalid_input: list):
    """Test Ankh class: raise ValueError when invalid input, containing non-string values
    Args:
        ankh (Ankh): Ankh class
        invalid_input (list): invalid input
    """
    with pytest.raises(ValueError):
        ankh.transform(invalid_input)


def test_ankh_valid_input(ankh: Ankh, valid_input_sequences: list[str]):
    """Test Ankh class with a valid sequence input
    Args
        ankh (Ankh): Ankh class
        valid_input_sequences (list): valid input sequences
    """
    transformed_sequences = ankh.transform(valid_input_sequences)
    assert round(transformed_sequences[-1][-1][-1], 3) == round(-0.0032451250590384007, 3)


def test_ankh_on_dataset(ankh: Ankh, regr_dataset: Dataset):
    """Test Ankh class with a valid dataset input
    Args
        ankh (Ankh): Ankh class
        regr_dataset (Dataset): valid dataset
    """
    batch = regr_dataset[:2]
    assert ankh.transform(batch["aa_seq"])[-1][-1][-1], 3 == round(-0.057, 3)
