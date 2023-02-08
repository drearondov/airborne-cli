import csv
import json
import pytest

from openpyxl import Workbook
from pathlib import Path


@pytest.fixture(scope="session")
def test_file_structure(tmp_path_directory: Path) -> Path:
    """Returns the file structure for a test session.

    Args:
        tmp_path_directory (Path): Path object for temporary directory.

    Returns:
        Path: Path object with file structure for tests
    """
    pass
