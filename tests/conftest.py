import csv
import json
import openpyxl
import pytest
import random

from openpyxl import Workbook
from pathlib import Path


@pytest.fixture(scope="session", autouse=True)
def general_data(faker) -> dict:
    """Generates test data in the supported formats

    Returns:
        dict: Dictionary of fake entries ready to be converted into the formats for testing
    """
    data = {
        "Ambiente": [],
        "Pabellon": [],
        "Area": [],
        "Altura": [],
        "Aforo_100": [],
        "ACH_natural": [],
        "Actividad": [],
        "Permanencia": [],
    }

    for _ in data:
        data["Ambiente"].append(faker.sentence(nb_words=2))
        data["Pabellon"].append(faker.sentence(nb_words=2))
        data["Area"].append(random.uniform(0, 1000))

    return data


@pytest.fixture(scope="session", autouse=True)
def file_structure(tmp_path_factory: Path) -> Path:
    """Returns the file structure for a test session.

    Args:
        tmp_path_factory (Path): Path object of builtin fixture to create temporary directories.

    Returns:
        Path: Path object with file structure for tests
    """
    return tmp_path_factory.mktemp("test_data_folder")
