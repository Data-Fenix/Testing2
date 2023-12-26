from pedata.disk_cache import hfds_from_pydict

dataset_dict_regression = {
    "aa_mut": [
        "wildtype (WT)",
        "R227G_G425E",
        "G172S_R227C",
        "G172P_R227K_G425H",
        "T226V_R227A",
        "R227E",
        "G172T",
        "G172R_R227E",
        "R227L",
        "R227M",
        "G172F",
        "R227T",
        "C170P",
        "C170A",
        "C170V",
        "C225I",
        "C225Y",
        "K228Y",
        "E231V",
        "E231I",
        "H482I_H484Y",
    ],
    "target kcat / kmol": [
        837.0,
        6389.4,
        3804.3,
        2222.22,
        2394.44,
        1999.0,
        2938.0,
        8923.0,
        823.0,
        2389.0,
        9823.0,
        8923.0,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.5,
        0.0,
        0.0,
        0.0,
    ],
    "aa_seq": [
        "MAAPAAEAPLSHVQQALAELAKPKDDPTRKHVCVQVAPAVRVAIAETLGLAPGATTPKQLAEGLRRLGFDEVFDTLFGADLTIMEEGSELLHRLTEHLEAHPHSDEPLPMFTSCCPGWIAMLEKSYPDLIPYVSSCKSPQMMLAAMVKSYLAEKKGIAPKDMVMVSIMPCTRKQSEADRDWFCVDADPTLRQLDHVITTVELGNIFKERGINLAELPEGEWDNPMGVGSGAGVLFGTTGGVMEAALRTAYELFTGTPLPRLSLSEVRGMDGIKETNITMVPAPGSKFEELLKHRAAARAEAAAHGTPGPLAWDGGAGFTSEDGRGGITLRVAVANGLGNAKKLITKMQAGEAKYDFVEIMACPAGCVGGGGQPRSTDKAITQKRQAALYNLDEKSTLRRSHENPSIRELYDTYLGEPLGHKAHELLHTHYVAGGVEEKDEKK",
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ],
}


dataset_dict_class = {
    "aa_mut": [
        "wildtype (WT)",
        "R227G_G425E",
        "G172S_R227C",
        "G172P_R227K_G425H",
        "T226V_R227A",
        "R227E",
        "G172T",
        "G172R_R227E",
        "R227L",
        "R227M",
        "G172F",
        "R227T",
        "C170P",
        "C170A",
        "C170V",
        "C225I",
        "C225Y",
        "K228Y",
        "E231V",
        "E231I",
        "H482I_H484Y",
    ],
    "target high_low": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ],
    "aa_seq": [
        "MAAPAAEAPLSHVQQALAELAKPKDDPTRKHVCVQVAPAVRVAIAETLGLAPGATTPKQLAEGLRRLGFDEVFDTLFGADLTIMEEGSELLHRLTEHLEAHPHSDEPLPMFTSCCPGWIAMLEKSYPDLIPYVSSCKSPQMMLAAMVKSYLAEKKGIAPKDMVMVSIMPCTRKQSEADRDWFCVDADPTLRQLDHVITTVELGNIFKERGINLAELPEGEWDNPMGVGSGAGVLFGTTGGVMEAALRTAYELFTGTPLPRLSLSEVRGMDGIKETNITMVPAPGSKFEELLKHRAAARAEAAAHGTPGPLAWDGGAGFTSEDGRGGITLRVAVANGLGNAKKLITKMQAGEAKYDFVEIMACPAGCVGGGGQPRSTDKAITQKRQAALYNLDEKSTLRRSHENPSIRELYDTYLGEPLGHKAHELLHTHYVAGGVEEKDEKK",
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ],
}


class RegressionToyDataset:
    """Toy dataset for regression with the needed encodings"""

    def __init__(self, needed_encodings: list[str] = []) -> None:
        """Initializes a toy dataset for regression with the needed encodings and splits it into train and test splits
        Args:
            needed_encodings (list[str], optional): list of encodings needed for the model.
                Defaults to [] -> all encodings are used (see `disk_cache.add_encodings`).
        """
        self.needed_encodings = needed_encodings
        self._unsplit_dataset = hfds_from_pydict(
            dataset_dict_regression,
            as_DatasetDict=False,
            needed_encodings=needed_encodings,
        )
        self._dataset = self._unsplit_dataset.train_test_split(0.2, seed=42)

    def __repr__(self):
        return (
            f"RegressionToyDataset(needed_encodings={self.needed_encodings}) \n"
            f"Full_dataset = {self.full_dataset} \n"
            f"Train split = {self.train} \n"
            f"Test split = {self.test}"
        )

    @property
    def full_dataset(self):
        """Returns the full dataset"""
        return self._unsplit_dataset

    @property
    def train_test_split_dataset(self):
        """Returns the split dataset"""
        return self._dataset

    @property
    def train(self):
        """Returns the train split of the dataset"""
        return self._dataset["train"]

    @property
    def test(self):
        """returns the test split of the dataset"""
        return self._dataset["test"]


class ClassficationToyDataset:
    """Toy dataset for regression with the needed encodings"""

    def __init__(self, needed_encodings: list[str] = []) -> None:
        """Initializes a toy dataset for regression with the needed encodings and splits it into train and test splits
        Args:
            needed_encodings (list[str], optional): list of encodings needed for the model.
                Defaults to [] -> all encodings are used (see `disk_cache.add_encodings`).
        """
        self.needed_encodings = needed_encodings
        self._unsplit_dataset = hfds_from_pydict(
            dataset_dict_class,
            as_DatasetDict=False,
            needed_encodings=needed_encodings,
        )
        self._dataset = self._unsplit_dataset.train_test_split(0.2, seed=42)

    def __repr__(self):
        return (
            f"ClassificationToyDataset(needed_encodings={self.needed_encodings}) \n"
            f"Full_dataset = {self.full_dataset} \n"
            f"Train split = {self.train} \n"
            f"Test split = {self.test}"
        )

    @property
    def full_dataset(self):
        """Returns the full dataset"""
        return self._unsplit_dataset

    @property
    def train_test_split_dataset(self):
        """Returns the split dataset"""
        return self._dataset

    @property
    def train(self):
        """Returns the train split of the dataset"""
        return self._dataset["train"]

    @property
    def test(self):
        """returns the test split of the dataset"""
        return self._dataset["test"]
