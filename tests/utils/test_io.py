import pytest
import pandas as pd

from loguru import logger
from random import choice

from airborne_cli.utils.io import check_data, load_data, make_results_folder


def test_check_data(general_data):
    assert check_data(general_data) is True

    required_columns = [
        "ambiente",
        "area",
        "altura",
        "aforo_100",
        "actividad",
        "permanencia",
    ]
    dropped_data = general_data.drop(choice(required_columns), axis=1)

    with pytest.raises(ValueError):
        check_data(dropped_data)


class TestDataLoading:
    def test_xls_input(self, xlsx_input_file):
        (data, data_folder) = load_data(xlsx_input_file)
        assert isinstance(data, pd.DataFrame)
        assert data_folder.exists()

        logger.info(f"Data: {data.head()} - Data Folder: {data_folder}")

    def test_csv_input(self, csv_input_file):
        (data, data_folder) = load_data(csv_input_file)
        assert isinstance(data, pd.DataFrame)
        assert data_folder.exists()

        logger.info(f"Data: {data.head()} - Data Folder: {data_folder}")

    def test_json_input(self, json_input_file):
        (data, data_folder) = load_data(json_input_file)
        assert isinstance(data, pd.DataFrame)
        assert data_folder.exists()

        logger.info(f"Data: {data.head()} - Data Folder: {data_folder}")

    def test_feather_input(self, feather_input_file):
        with pytest.raises(ValueError):
            load_data(feather_input_file)


def test_make_results_folder(file_structure_root):
    results = make_results_folder(file_structure_root)

    assert results.exists()
    assert results.parent == file_structure_root
