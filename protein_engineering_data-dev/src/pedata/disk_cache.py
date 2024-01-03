import os
from re import T
import sys
from pathlib import Path
from typing import List, Tuple, Union

import datasets as ds
import jax.numpy as np
import numpy as onp
import pandas as pd


from pedata.integrity import check_dataset
from pedata.config import alphabets, paths, add_encodings
from pedata.mutation.mutation import Mutation

from pedata.exazyme_datasets import dataset_base_processing
import fsspec


def get_missing_values(df: pd.DataFrame, feature: str) -> List[bool]:
    """get missing values in the `feature` column

    Args:
        df: dataframe to check
        feature: which column to check for missing values

    Returns:
        List[bool]: return True for the indices corresponding to the missing values

    """
    return df.loc[:, feature].isna() | df.loc[:, feature].isnull()


def fill_missing_sequences(df: pd.DataFrame, feature: str) -> pd.DataFrame:
    """Fill missing values in the `feature` column

    Args:
        df: dataframe to check
        feature: which column to fill for missing values

    Returns:
        pd.DataFrame: dataframe with filled missing values
    """
    missing_values = get_missing_values(df, feature)

    if missing_values.sum() > 0:
        # Apply mutations to fill in missing values in 'dna_seq' column
        df.loc[missing_values, feature] = pd.DataFrame(
            {feature: Mutation.apply_all_mutations(ds.Dataset.from_pandas(df))}
        ).loc[missing_values, feature]

    return df


def hfds_from_pydict(
    dataset_dict: dict, as_DatasetDict: bool = True, needed_encodings: list[str] = []
) -> ds.Dataset | ds.DatasetDict:
    """Returns a Dataset or DatasetDict from a dataset_dict
    Args:
        dataset_dict: the python dictionnary containing regression data
        as_DatasetDict: whether to return DatasetDictionary with one split or a Dataset
        needed_encodings:
    Returns:
        a Dataset or DatasetDictionary
    """
    hfds = ds.Dataset.from_dict(dataset_dict)
    # Perform dataset integrity check
    check_dataset(hfds)

    feature_keys = hfds.column_names

    if "aa_seq" in feature_keys:
        # Check for missing values in the 'aa_seq' column
        df = fill_missing_sequences(hfds.to_pandas(), "aa_seq")

    elif "dna_seq" in feature_keys:
        # Check for missing values in the 'dna_seq' column
        df = fill_missing_sequences(hfds.to_pandas(), "dna_seq")

    # Convert the dataframe to a back to a dataset object
    hfds = ds.Dataset.from_pandas(df)

    # Add encodings to dataset
    hfds = add_encodings(hfds, needed=needed_encodings)

    # Return the processed dataset
    if as_DatasetDict:
        return ds.DatasetDict({"whole_dataset": hfds})
    else:
        return hfds


def preprocess_data(
    filename: Union[str, Path],
    save_to_path: str | None = None,
    filesystem: fsspec.AbstractFileSystem | None = None,
    needed_encodings: list[str] | set[str] = [],
    add_index: bool = True,
    add_splits: bool = True,
) -> ds.Dataset:
    """Transforms a data file (CSV or Excel) into a Hugging Face dataset and computes all available features.

    Args:
        filename (Union[str, Path]): File name of the source CSV or Excel file.
        save_to_path (str, optional): Path to save the Hugging Face dataset. Defaults to None (not saved).
        filesystem (fsspec.AbstractFileSystem, optional): File system to use for saving. Defaults to None (local filesystem).

    Returns:
        ds.Dataset: The dataset with all precomputed features.

    Example:
        >>> import pandas as pd
        >>> data = pd.DataFrame({"aa_mut": ["wildtype", "T8M", "P3G"],"aa_seq": ["GMPKSEFTHC", None, None],"target foo": [1, 2, 3]})
        >>> csv_file = "test_data.csv"
        >>> data.to_csv(csv_file, index=False)
        >>> dataset = preprocess_data(csv_file)
        >>> print(dataset)
        Dataset({
            features: ['aa_mut', 'aa_seq', 'target foo', 'target summary variable', 'aa_unirep_1900', 'aa_unirep_final', 'aa_len', 'aa_1gram', 'aa_ankh_base', 'aa_esm2_t6_8M', 'aa_1hot'],
            num_rows: 3
        })

    Note:
        The example above converts a dataframe into a CSV file and saves it in the current directory as "test_data.csv".
        The CSV file is then passed to the preprocess_data() function and is preprocessed to compute more features, and return a new HuggingFace dataset.
    """

    filename = str(filename).lower()

    # Check file format
    if filename.endswith("csv"):
        df = read_csv_ignore_case(filename)

    elif filename.endswith("xls") or filename.endswith("xlsx"):
        df = pd.read_excel(filename, 0)

    else:
        raise TypeError("Invalid input: input either a csv or an excel file")

    # Perform dataset integrity check
    check_dataset(ds.Dataset.from_pandas(df))

    feature_keys = df.columns

    if "aa_seq" in feature_keys:
        # Check for missing values in the 'aa_seq' column
        df = fill_missing_sequences(df, "aa_seq")

    elif "dna_seq" in feature_keys:
        # Check for missing values in the 'dna_seq' column
        df = fill_missing_sequences(df, "dna_seq")

    # Convert the dataframe to a dataset object
    dataset = ds.Dataset.from_pandas(df)

    # add the basics to the dataset
    dataset = dataset_base_processing(
        dataset,
        needed_encodings=needed_encodings,
        add_index=add_index,
        add_splits=add_splits,
    )

    # Save the data to a specified path, if provided
    if save_to_path is not None:
        dataset.save_to_disk(save_to_path, storage_options=filesystem.storage_options)

    # Return the processed dataset
    return dataset


def load_similarity(
    alphabet_type: str,
    similarity_name: Union[str, List[str]],
    replace_existing: bool = False,
) -> Tuple[List[str], np.ndarray]:
    """
    Load similarity matrices.
        Loads similarity matrices based on the specified alphabet type and similarity names. It provides the capability to load
        multiple similarity matrices simultaneously and preprocesses them into usable similarity matrices. The function also supports
        optional caching of the loaded matrices for improved performance in subsequent operations.

    Args:
        alphabet_type (str): Specifies the type of alphabet used in the similarity calculation. It can be either "aa" for amino acids or "dna" for DNA sequences.
        similarity_name (Union[str, List[str]]): The name or list of names of the similarity matrix/matrixes to be loaded.
        replace_existing (bool, optional): Determines if an existing matrix should be overwritten. Defaults to False.

    Returns:
        Tuple[List[str], np.ndarray]: A tuple containing the alphabet used for the similarity calculation and the preprocessed similarity matrix.

    Example:
    >>> similarity_names = ['name1', 'name2']
    >>> alphabet, similarity_matrix = load_similarity('aa', similarity_names)
    >>> print(similarity_matrix)

    Raises:
        #FIXME Check that these exceptions are all tested
        ValueError: If the specified alphabet type is invalid.
        ValueError: If the similarity matrix dimensions are not valid.
        ValueError: If the similarity matrix contains superfluous entries.
        Exception: If the similarity matrix is missing entries.

    """

    # check which alphabet to use
    if alphabet_type == "aa":
        alph = onp.array(alphabets.aa_alphabet)
    elif alphabet_type == "dna":
        alph = onp.array(alphabets.dna_alphabet)
    else:
        raise ValueError(f"Invalid alphabet type: {alphabet_type}")

    rval = []  # Stores preprocessed similarity matrix as return value

    # Ensure similarity_name is a list
    if isinstance(similarity_name, str):
        similarity_name = [similarity_name]

    for s in similarity_name:
        # Prepare file paths
        similarity_filename, file_extension = alphabet_type + "_" + s, ".txt"
        output_file_path = os.path.join(
            paths.path_simil, f"{similarity_filename}_ordered.csv"
        )

        if paths.data_exists(output_file_path) and not replace_existing:
            # Load the similarity matrix from cache
            print(
                f"\n--- Existing disk cache ---\nFile: {output_file_path}\nStatus: Existing file will not be replaced\n---\n",
                file=sys.stderr,
            )
            rval.append(onp.loadtxt(output_file_path, delimiter=","))

        else:
            # Open the similarity matrix file and read its lines
            with open(
                os.path.join(paths.path_simil, similarity_filename + file_extension)
            ) as matrix_file:
                lines = matrix_file.readlines()

            header = None  # Variable to store the header of the similarity matrix
            col_header = []  # List to store the column header of the similarity matrix
            similarity_matrix = []  # List to store the similarity matrix entries

            for idx, row in enumerate(lines):
                # Skip commented lines and empty lines
                if row[0] == "#" or len(row) == 0:
                    continue

                # Strip leading and trailing whitespace from the row
                row = row.strip()

                # Split the row into individual entries
                entries = row.split()

                if header is None:
                    # First non-comment and non-empty line represents the header
                    header = entries
                    continue

                else:
                    # The first entry in each subsequent line is the column header
                    col_header.append(entries.pop(0))

                    # Convert the remaining entries to floats and append them to the similarity matrix
                    similarity_matrix.append(list(map(float, entries)))

            # Convert the header and column header to numpy arrays
            header, col_header = onp.array(header), onp.array(col_header)

            # Convert the similarity matrix to a numpy array
            similarity_matrix = np.array(similarity_matrix)

            # Check the dimensions and consistency of the matrix
            if not np.all(header == col_header):
                raise ValueError(
                    "Inconsistent header and column header in the similarity matrix: "
                    "The values in the header and column header do not match."
                )

            if (
                len(header) != similarity_matrix.shape[0]
                or similarity_matrix.shape[0] != similarity_matrix.shape[1]
            ):
                raise ValueError("Dimensions of the similarity matrix are not valid.")

            # ?? Replace the missing value placeholder in the header if present
            if header[-1] == "*":
                header[-1] = alphabets.missing_value_enc

            # Check for superfluous entries in the similarity matrix
            superfluous_entries = set(header).difference(alph)
            if len(superfluous_entries) > 0:
                print(
                    f"Similarity matrix contains superfluous entries {superfluous_entries}"
                )

            # Check for missing entries in the similarity matrix
            missing_entries = set(alph).difference(header)
            if len(missing_entries) != 0:
                raise Exception(f"Similarity matrix doesn't contain {missing_entries}")

            # Reorder the similarity matrix based on the alphabet order
            reorder = np.argmax(header[:, None] == alph[None, :], 0)

            # Append the reordered similarity matrix to the result list
            rval.append(similarity_matrix[reorder, :][:, reorder])

            # Save the reordered similarity matrix to disk for future use
            onp.savetxt(
                output_file_path,
                rval[-1],
                delimiter=",",
                header=", ".join(alph),
                fmt="%.2f",
            )

    return (
        alph,
        onp.array(rval).squeeze(),
    )  # Return the alphabet and the preprocessed similarity matrix


def read_csv_ignore_case(file_path: str) -> pd.DataFrame:
    """Reads a CSV file with a case-insensitive match
    Args:
        file_path: path to the file
    Returns:
        pd.DataFrame: the dataframe
    """
    directory, file_name = os.path.split(file_path)
    if len(directory) == 0:
        directory = os.getcwd()
    # List all files in the directory
    files_in_directory = os.listdir(directory)

    # Find the file with a case-insensitive match
    matching_files = [
        file for file in files_in_directory if file.lower() == file_name.lower()
    ]

    if not matching_files:
        raise FileNotFoundError(f"No file found matching: {file_name}")

    # Use the first matching file (in case there are multiple matches)
    matching_file_path = os.path.join(directory, matching_files[0])

    # Use pd.read_csv with the found file path
    return pd.read_csv(matching_file_path)
