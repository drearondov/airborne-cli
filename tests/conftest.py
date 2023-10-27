import pandas as pd
import pytest

from faker import Faker
from pathlib import Path
from random import uniform, randint


@pytest.fixture(scope="session")
def general_data() -> pd.DataFrame:
    """Generates test data in the supported formats

    Returns:
        pd.DataFrame: DataFrame with fake entries ready to be converted into the formats for testing
    """
    data = {
        "ambiente": [],
        "pabellon": [],
        "area": [],
        "altura": [],
        "aforo_100": [],
        "ACH_natural": [],
        "actividad": [],
        "permanencia": [],
    }

    fake = Faker()

    for _ in range(0, 10, 1):
        data["ambiente"].append(fake.sentence(nb_words=2))
        data["pabellon"].append(fake.sentence(nb_words=2))
        data["area"].append(uniform(0, 1000))
        data["altura"].append(uniform(0, 15))
        data["aforo_100"].append(randint(0, 100))
        data["ACH_natural"].append(uniform(0, 50))
        data["actividad"].append(randint(0, 3))
        data["permanencia"].append(uniform(0, 500))

    data_frame = pd.DataFrame.from_dict(data)

    return data_frame


@pytest.fixture(scope="session")
def file_structure_root(tmp_path_factory) -> Path:
    """Returns the file structure for a test session.

    Returns:
        Path: Path object with file structure for tests
    """
    return tmp_path_factory.mktemp("temp_root")


@pytest.fixture(scope="session")
def xlsx_input_file(general_data: pd.DataFrame, file_structure_root: Path) -> Path:
    """Returns the path for the Excel test file

    Args:
        general_data (pd.DataFrame): Pandas DataFrame with fake data
        file_structure_root (Path): Path of the root of the temporary test file

    Returns:
        Path: Path of the Excel test file
    """
    excel_file_path = file_structure_root.joinpath("excel_input.xlsx")
    general_data.to_excel(excel_file_path)
    return excel_file_path


@pytest.fixture(scope="session")
def csv_input_file(general_data: pd.DataFrame, file_structure_root: Path) -> Path:
    """Returns the path for the Excel test file

    Args:
        general_data (pd.DataFrame): Pandas DataFrame with fake data
        file_structure_root (Path): Path of the root of the temporary test file

    Returns:
        Path: Path of the Excel test file
    """
    csv_file_path = file_structure_root.joinpath("csv_input.csv")
    general_data.to_csv(csv_file_path)
    return csv_file_path


@pytest.fixture(scope="session")
def json_input_file(general_data: pd.DataFrame, file_structure_root: Path) -> Path:
    """Returns the path for the Excel test file

    Args:
        general_data (pd.DataFrame): Pandas DataFrame with fake data
        file_structure_root (Path): Path of the root of the temporary test file

    Returns:
        Path: Path of the Excel test file
    """
    json_file_path = file_structure_root.joinpath("json_input.json")
    general_data.to_json(json_file_path)
    return json_file_path


@pytest.fixture(scope="session")
def feather_input_file(general_data: pd.DataFrame, file_structure_root: Path) -> Path:
    """Returns the path for the Excel test file

    Args:
        general_data (pd.DataFrame): Pandas DataFrame with fake data
        file_structure_root (Path): Path of the root of the temporary test file

    Returns:
        Path: Path of the Excel test file
    """
    feather_file_path = file_structure_root.joinpath("feather_input.json")
    general_data.to_feather(feather_file_path)
    return feather_file_path
