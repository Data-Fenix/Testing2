from pedata.pytorch_dataloaders import Dataloader, Transformer, Encoder
from datasets import load_dataset
import torch
from pytest import fixture
import pytest

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


# ============ fixtures =============


@fixture
def dataset():
    return load_dataset("Exazyme/TemStaPro-Minor-bal65", split="testing[:10]")


@fixture
def odd_dataset():
    return load_dataset("Exazyme/TemStaPro-Minor-bal65", split="testing[:17]")


@fixture
def batch_size():
    return 8


@fixture
def embedding_names_ankh():
    return ["ankh", "aa_1hot"]


@fixture
def embedding_names_esm():
    return ["esm", "aa_1hot"]


@fixture
def transformer():
    return Transformer()


# ============ tests =============


def test_transformer(transformer):
    """testing transformer

    Args:
        transformer [Transformer]: transformer to be used
    """
    x = [234, 657]
    transformed_sequences = transformer.transform(x)
    assert transformed_sequences.shape == (2, 1)

    x = torch.tensor([1, 2, 3])
    transformed_sequences = transformer.transform(x)
    assert transformed_sequences.shape == (3, 1)

    x = torch.tensor([[1, 2, 3], [4, 5, 6]])
    transformed_sequences = transformer.transform(x)
    assert transformed_sequences.shape == (2, 3)


def test_encoder_init():
    with pytest.raises(Exception):
        Encoder()


def test_dataloader_init(dataset, embedding_names_ankh):
    dataloader = Dataloader(dataset=dataset, embedding_names=embedding_names_ankh)

    assert isinstance(dataloader, torch.utils.data.Dataset)


def test_dataloader_init_odd(odd_dataset, embedding_names_ankh):
    dataloader = Dataloader(
        dataset=odd_dataset,
        embedding_names=embedding_names_ankh,
        targets=["growth_temp"],
        batch_size=8,
        batch_norm=True,
    )

    assert isinstance(dataloader, torch.utils.data.Dataset)


def test_dataloader_training_mode_ankh(dataset, batch_size, embedding_names_ankh):
    """testing Dataloader for training mode

    Args:
        dataset [hf dataset]: dataset to be used
        batch_size [int]: batch size to be used
        embedding_names [list]: list of embedding names to be used
    """

    dataloader = Dataloader(
        dataset=dataset,
        embedding_names=embedding_names_ankh,
        targets=["growth_temp"],
        batch_size=batch_size,
        device=device,
        shuffle=True,
    )

    num_samples = 0
    for X, y in dataloader:
        num_samples += len(X["ankh"])

    assert num_samples == len(dataset)


def test_dataloader_test_mode_ankh(dataset, batch_size, embedding_names_ankh):
    """testing Dataloader for testing mode

    Args:
        dataset [hf dataset]: dataset to be used
        batch_size [int]: batch size to be used
        embedding_names [list]: list of embedding names to be used
    """
    dataloader = Dataloader(
        dataset=dataset,
        embedding_names=embedding_names_ankh,
        batch_size=batch_size,
        device=device,
        shuffle=True,
    )

    num_samples = 0
    for X in dataloader:
        num_samples += len(X["ankh"])

    assert num_samples == len(dataset)


def test_dataloader_training_mode_esm(dataset, batch_size, embedding_names_esm):
    """testing Dataloader for training mode

    Args:
        dataset [hf dataset]: dataset to be used
        batch_size [int]: batch size to be used
        embedding_names [list]: list of embedding names to be used
    """

    dataloader = Dataloader(
        dataset=dataset,
        embedding_names=embedding_names_esm,
        targets=["growth_temp"],
        batch_size=batch_size,
        device=device,
        shuffle=True,
    )

    num_samples = 0
    for X, y in dataloader:
        num_samples += len(X["esm"])

    assert num_samples == len(dataset)


def test_dataloader_test_mode_esm(dataset, batch_size, embedding_names_esm):
    """testing Dataloader for testing mode

    Args:
        dataset [hf dataset]: dataset to be used
        batch_size [int]: batch size to be used
        embedding_names [list]: list of embedding names to be used
    """
    dataloader = Dataloader(
        dataset=dataset,
        embedding_names=embedding_names_esm,
        batch_size=batch_size,
        device=device,
        shuffle=True,
    )

    num_samples = 0
    for X in dataloader:
        num_samples += len(X["esm"])

    assert num_samples == len(dataset)
