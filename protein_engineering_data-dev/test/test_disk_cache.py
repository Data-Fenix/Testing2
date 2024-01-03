import pandas as pd
import os
import pytest
from pedata.disk_cache import (
    preprocess_data,
    load_similarity,
    get_missing_values,
    fill_missing_sequences,
    hfds_from_pydict,
)

from pedata.static.example_data.example_data import dataset_dict_regression
import fsspec
import shutil
from pytest import fixture


@fixture(scope="module")
def aa_expected_new_features():
    return [
        "aa_unirep_1900",
        "aa_unirep_final",
        "aa_len",
        "aa_1gram",
        "aa_1hot",
    ]


@fixture(scope="module")
def hfds_from_dict():
    return hfds_from_pydict(dataset_dict_regression)["whole_dataset"]


@fixture(scope="module")
def dna_expected_new_features():
    return ["dna_len", "dna_1hot"]


@fixture(scope="module")
def alphabet_type_dna():
    return "dna"


@fixture(scope="module")
def alphabet_type_aa():
    return "aa"


@fixture(scope="module")
def csv_file():
    return "test_data.csv"


@fixture(scope="module")
def folder_path():
    return "processed_data"


@fixture
def xls_file():
    return "test_data.xls"


def clean_up(
    csv_file="test_data.csv",
    csv_file_2="tEsT_DATA.CsV",
    xls_file="test_data.xls",
    folder_path="processed_data",
):
    """Delete created temporarly files and folders"""

    if os.path.exists(csv_file):
        os.remove(csv_file)

    if os.path.exists(csv_file_2):
        os.remove(csv_file_2)

    if os.path.exists(xls_file):
        os.remove(xls_file)

    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)


def test_hfds_from_pydict(hfds_from_dict):
    """hfds_from_pydict test: Create a dataset from a dictionary"""
    assert len(hfds_from_dict) == 21


def test_get_missing_values(hfds_from_dict):
    """get_missing_values test: Missing values in "aa_seq" column"""
    get_missing_values(hfds_from_dict.to_pandas(), "aa_seq")


def test_fill_missing_sequences(hfds_from_dict):
    """fill_missing_sequences test: Missing values in "aa_seq" column"""
    fill_missing_sequences(hfds_from_dict.to_pandas(), "aa_seq")


def test_preprocess_data_wrong_file():
    """preprocess_data test: Input a filename that is neither a csv nor an excel file"""
    filename = "sample.txt"
    with pytest.raises(TypeError):
        preprocess_data(filename)


def test_preprocess_data_invalid_alphabet(csv_file):
    """preprocess_data test: Containing invalid AA alphabets"""
    data = pd.DataFrame(
        {
            "aa_mut": ["wildtype", "T8M", "P3G"],
            "aa_seq": ["XMPBSOFT", None, None],  # X,B, AND O are invalid aa alphabets
            "target foo": [1, 2, 3],
        }
    )
    data.to_csv(csv_file, index=False)
    with pytest.raises(ValueError):
        _ = preprocess_data(csv_file)

    clean_up()


def test_preprocess_data_missing_values(aa_expected_new_features, csv_file):
    """preprocess_data test: Missing values in "aa_seq" column"""
    pd.DataFrame(
        {
            "aa_mut": ["wildtype", "T8M", "P3G"],
            "aa_seq": ["GMPKSEFTHC", None, None],
            "target foo": [1, 2, 3],
        }
    ).to_csv(csv_file, index=False)
    dataset = preprocess_data(csv_file)
    clean_up()
    assert all(
        feature in list(dataset.features.keys()) for feature in aa_expected_new_features
    )


def test_preprocess_data_no_missing_values(aa_expected_new_features, csv_file):
    """preprocess_data test: No missing values in "aa_seq" column"""
    pd.DataFrame(
        {"aa_seq": ["GMPKSEFTHC", "GMPKSEFMHC", "GMGKSEFTHC"], "target foo": [1, 2, 3]}
    ).to_csv(csv_file, index=False)
    dataset = preprocess_data(csv_file)
    clean_up()
    assert all(
        feature in list(dataset.features.keys()) for feature in aa_expected_new_features
    )


def test_preprocess_data_file_name_upper(aa_expected_new_features):
    """preprocess_data test: Input a filename with capital letters
    (It gets converted to lower case)"""
    pd.DataFrame(
        {"aa_seq": ["GMPKSEFTHC", "GMPKSEFMHC", "GMGKSEFTHC"], "target foo": [1, 2, 3]}
    ).to_csv("tEsT_DATA.CsV", index=False)
    dataset = preprocess_data("tEsT_DATA.CsV")
    clean_up()
    assert all(
        feature in list(dataset.features.keys()) for feature in aa_expected_new_features
    )


def test_preprocess_data_local_filesytem(
    aa_expected_new_features, csv_file, folder_path
):
    """preprocess_data test: using local file system"""

    pd.DataFrame(
        {"aa_seq": ["GMPKSEFTHC", "GMPKSEFMHC", "GMGKSEFTHC"], "target foo": [1, 2, 3]}
    ).to_csv(csv_file, index=False)
    local_filesystem = fsspec.filesystem("file")
    dataset = preprocess_data(
        csv_file, save_to_path=folder_path, filesystem=local_filesystem
    )
    clean_up()
    assert all(
        feature in list(dataset.features.keys()) for feature in aa_expected_new_features
    )


def test_preprocess_data_xls_file(aa_expected_new_features, xls_file, folder_path):
    """preprocess_data test: Process data from an XLS file"""
    pd.DataFrame(
        {
            "aa_mut": ["wildtype", "T8M", "P3G"],
            "aa_seq": ["GMPKSEFTHC", None, None],
            "target foo": [1, 2, 3],
        }
    ).to_excel(xls_file, index=False, engine="openpyxl")

    local_filesystem = fsspec.filesystem("file")
    dataset = preprocess_data(
        xls_file, save_to_path=folder_path, filesystem=local_filesystem
    )
    clean_up()
    assert all(
        feature in list(dataset.features.keys()) for feature in aa_expected_new_features
    )


def test_preprocess_data_missing_dna_seq_val(dna_expected_new_features, csv_file):
    """preprocess_data test: Missing values in "dna_seq" column"""
    pd.DataFrame(
        {
            "dna_mut": ["wildtype", "G6T", "T3G"],
            "dna_seq": ["GCTCCG", None, None],
            "target foo": [1, 2, 3],
        }
    ).to_csv(csv_file, index=False)
    dataset = preprocess_data(csv_file)
    clean_up()
    assert all(
        [
            feature in list(dataset.features.keys())
            for feature in dna_expected_new_features
        ]
    )


def test_preprocess_data_no_missing_dna_seq_val(dna_expected_new_features, csv_file):
    """preprocess_data test: No missing values in "dna_seq" column"""
    pd.DataFrame(
        {"dna_seq": ["GCTCCG", "GCTCCT", "GCGCCG"], "target foo": [1, 2, 3]}
    ).to_csv(csv_file, index=False)
    dataset = preprocess_data(csv_file)
    clean_up()
    assert all(
        [
            feature in list(dataset.features.keys())
            for feature in dna_expected_new_features
        ]
    )


def test_load_similarity_invalid_alphabet():
    """Test load_similarity: Invalid alphabet type"""
    alphabet_type_bb = "bb"
    similarity_name = "Simple"
    with pytest.raises(ValueError):
        load_similarity(alphabet_type_bb, similarity_name)


def test_load_similarity_single_dna_simil_mat(alphabet_type_dna):
    """Test load_similarity: Load single DNA similarity matrix and replace disk cache"""
    similarity_name = "Simple"
    _, similarity_matrix = load_similarity(
        alphabet_type_dna, similarity_name, replace_existing=True
    )
    assert similarity_matrix[0][0] == 1 and similarity_matrix[-1][-1] == 1


def test_load_similarity_multiple_dna_simil_mat(alphabet_type_dna):
    """Test load_similarity: Load multiple DNA similarity matrix and replace disk cache"""
    similarity_name = ["Simple", "Identity"]
    _, similarity_matrix = load_similarity(
        alphabet_type_dna, similarity_name, replace_existing=True
    )
    assert similarity_matrix[0][0][-1] == 0 and similarity_matrix[1][2][2] == 1


def test_load_similarity_without_ow_dna_simil_mat(alphabet_type_dna):
    """Test load_similarity: Withought overwriting an existing DNA similarity matrix (replace_existing=False)"""
    similarity_name = "Simple"
    _, similarity_matrix = load_similarity(
        alphabet_type_dna, similarity_name, replace_existing=False
    )
    assert similarity_matrix[0][0] == 1 and similarity_matrix[-1][-1] == 1


def test_load_similarity_single_aa_simil_mat(alphabet_type_aa):
    """Test load_similarity:  Load single AA similarity matrix and replace disk cache"""
    similarity_name = "BLOSUM62"
    _, similarity_matrix = load_similarity(
        alphabet_type_aa, similarity_name, replace_existing=True
    )
    assert similarity_matrix[0][0] == 4 and similarity_matrix[13][4] == -3


def test_load_similarity_multiple_aa_simil_mat(alphabet_type_aa):
    """Test load_similarity: Load multiple AA similarity matrix and replace disk cache"""
    similarity_name = ["BLOSUM62", "BLOSUM90", "IDENTITY", "PAM20"]
    _, similarity_matrix = load_similarity(
        alphabet_type_aa, similarity_name, replace_existing=True
    )
    assert (
        similarity_matrix[0][0][0] == 4
        and similarity_matrix[1][10][10] == 7
        and similarity_matrix[2].shape[0] == 21
        and similarity_matrix[3][0][4] == -9
    )


def test_load_similarity_without_ow_aa_simil_mat(alphabet_type_aa):
    """Test load_similarity: Without overwriting an existing AA similarity matrix (replace_existing=False)"""
    similarity_name = "PAM20"
    _, similarity_matrix = load_similarity(
        alphabet_type_aa, similarity_name, replace_existing=False
    )
    assert similarity_matrix[0][4] == -9 and similarity_matrix[-1][1] == -19
