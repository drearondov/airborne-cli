import csv
import json
from pathlib import Path

import pytest
from openpyxl import Workbook


@pytest.fixture(scope="session")
def test_file_structure(tmp_path_factory: Path) -> Path:
    """Returns the file structure for a test session.

    Args:
        tmp_path_factory (Path): Path object of builtin fixture to create temporary directories.

    Returns:
        Path: Path object with file structure for tests
    """
    return tmp_path_factory.mktemp("test_results")


@pytest.fixture(scope="session")
def test_data() -> tuple:
    """Generates test data in the supported formats

    Returns:
        tuple: Tuple of different temporary files for testing
    """
    pass
