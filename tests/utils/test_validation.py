import pytest
import pandas as pd

from faker import Faker
from random import choice, randint, uniform

from airborne_cli.utils.validation import (
    validate_existing_columns,
    validate_data_types,
    validate_input,
)


def test_validate_existing_columns(general_data: pd.DataFrame) -> None:
    """Tests validation script for columns

    Args:
        general_data (pd.DataFrame): Dataframe wit test data
    """
    assert validate_existing_columns(general_data.columns) is True

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
        validate_existing_columns(dropped_data.columns)


def test_validate_data_types(general_data: pd.DataFrame) -> None:
    """Test validation script for data types.

    Args:
        general_data (pd.DaraFrame): Dataframe with test data
    """
    assert validate_data_types(general_data) is True

    wrong_data = general_data.astype("object")

    with pytest.raises(ValueError):
        validate_data_types(wrong_data)


class TestValidateInput:
    def test_validate_input_right(self, general_data: pd.DataFrame) -> None:
        """Test input validation for good data.

        Args:
            general_data (pd.DataFrame): DataFrame with test data.
        """
        assert validate_input(general_data) is True

    def test_validate_input_wrong_area(
        self, faker: Faker, general_data: pd.DataFrame
    ) -> None:
        """Test validation function with area less than 0.

        Args:
            general_data (pd.DataFrame): DataFrame with starting test data.
        """
        new_data = pd.DataFrame.from_dict(
            {
                "ambiente": [faker.sentence(nb_words=2)],
                "pabellon": [faker.sentence(nb_words=2)],
                "area": [uniform(-1000, 0)],
                "altura": [uniform(0, 15)],
                "aforo_100": [randint(0, 100)],
                "ACH_natural": [uniform(0, 50)],
                "actividad": [randint(0, 5)],
                "permanencia": [uniform(0, 500)],
            }
        )

        test_data = pd.concat([general_data, new_data], ignore_index=True)

        with pytest.raises(ValueError):
            validate_input(test_data)

    def test_validate_input_wrong_altura(
        self, faker: Faker, general_data: pd.DataFrame
    ) -> None:
        """Test validation function with height less than 0.

        Args:
            general_data (pd.DataFrame): DataFrame with starting test data.
        """
        new_data = pd.DataFrame.from_dict(
            {
                "ambiente": [faker.sentence(nb_words=2)],
                "pabellon": [faker.sentence(nb_words=2)],
                "area": [uniform(0, 1000)],
                "altura": [uniform(-15, 0)],
                "aforo_100": [randint(0, 100)],
                "ACH_natural": [uniform(0, 50)],
                "actividad": [randint(0, 5)],
                "permanencia": [uniform(0, 500)],
            }
        )

        test_data = pd.concat([general_data, new_data], ignore_index=True)

        with pytest.raises(ValueError):
            validate_input(test_data)

    def test_validate_input_wrong_aforo(
        self, faker: Faker, general_data: pd.DataFrame
    ) -> None:
        """Test validation function with occupancy less than 0.

        Args:
            general_data (pd.DataFrame): DataFrame with starting test data.
        """
        new_data = pd.DataFrame.from_dict(
            {
                "ambiente": [faker.sentence(nb_words=2)],
                "pabellon": [faker.sentence(nb_words=2)],
                "area": [uniform(0, 1000)],
                "altura": [uniform(0.1, 50)],
                "aforo_100": [randint(-100, 0)],
                "ACH_natural": [uniform(0, 50)],
                "actividad": [randint(0, 5)],
                "permanencia": [uniform(0, 500)],
            }
        )

        test_data = pd.concat([general_data, new_data], ignore_index=True)

        with pytest.raises(ValueError):
            validate_input(test_data)

    def test_validate_input_wrong_activity(
        self, faker: Faker, general_data: pd.DataFrame
    ) -> None:
        """Test validation function with wrong activity option.

        Args:
            general_data (pd.DataFrame): DataFrame with starting test data.
        """
        new_data = pd.DataFrame.from_dict(
            {
                "ambiente": [faker.sentence(nb_words=2)],
                "pabellon": [faker.sentence(nb_words=2)],
                "area": [uniform(0, 1000)],
                "altura": [uniform(0.1, 15)],
                "aforo_100": [randint(1, 100)],
                "ACH_natural": [uniform(0, 50)],
                "actividad": [randint(5, 15)],
                "permanencia": [uniform(0, 500)],
            }
        )

        test_data = pd.concat([general_data, new_data], ignore_index=True)

        with pytest.raises(ValueError):
            validate_input(test_data)

    def test_validate_input_wrong_permanencia(
        self, faker: Faker, general_data: pd.DataFrame
    ) -> None:
        """Test validation function with wrong activity option.

        Args:
            general_data (pd.DataFrame): DataFrame with starting test data.
        """
        new_data = pd.DataFrame.from_dict(
            {
                "ambiente": [faker.sentence(nb_words=2)],
                "pabellon": [faker.sentence(nb_words=2)],
                "area": [uniform(0, 1000)],
                "altura": [uniform(0.1, 15)],
                "aforo_100": [randint(1, 100)],
                "ACH_natural": [uniform(0, 50)],
                "actividad": [randint(5, 15)],
                "permanencia": [uniform(-500, -0.1)],
            }
        )

        test_data = pd.concat([general_data, new_data], ignore_index=True)

        with pytest.raises(ValueError):
            validate_input(test_data)
