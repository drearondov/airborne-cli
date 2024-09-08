"""
Validate input file for required fields, datatypes and values.
"""

import pandas as pd
from numpy import dtype


def validate_existing_columns(columns: pd.Index) -> bool:
    """Validates the existence of all the required columns.

    Args:
        columns (pd.Series): List of colummns in existing Data Frame

    Returns:
        bool: All the columns exist of not"""

    REQUIRED_COLUMNS = [
        "ambiente",
        "area",
        "altura",
        "aforo_100",
        "actividad",
        "permanencia",
    ]

    for column_name in REQUIRED_COLUMNS:
        if column_name not in columns:
            raise ValueError(
                f"[bold red]Alert![/bold red] Column {column_name} not found. Is a required column"
            )

    return True


def validate_data_types(data_frame: pd.DataFrame) -> bool:
    """Validates dtypes for required columns

    Args:
        data_frame (pd.DataFrame): Data frame to validate data types

    Returns:
        bool: Columns are the correct type or not
    """
    REQUIRED_COLUMNS = {
        "ambiente": dtype("object"),
        "area": dtype("float64"),
        "altura": dtype("float64"),
        "aforo_100": dtype("int64"),
        "actividad": dtype("int64"),
        "permanencia": dtype("float64"),
    }

    for column_name, column_type in REQUIRED_COLUMNS.items():
        if data_frame[column_name].dtype != column_type:
            raise ValueError(
                f"[bold red]Alert![/bold red] Column {column_name} is not the correct type {column_type}"
            )

    return True


def validate_input(data_frame: pd.DataFrame) -> bool:
    """Validate allowed values for the required columns

    Args:
        data_frame (pd.DataFrame): Data frame for analysis.

    Returns:
        bool: The data is valid or not
    """
    # Validating area
    if data_frame["area"].min() <= 0:
        raise ValueError(
            f"[bold red]Alert![/bold red] One of the area value in the document is equal to {data_frame['area'].min()} below 0"
        )

    # Validating altura
    if data_frame["altura"].min() <= 0:
        raise ValueError(
            f"[bold red]Alert![/bold red] One of the height values in the document is equal to {data_frame['altura'].min()} below 0"
        )

    # Validating aforo
    if data_frame["aforo_100"].min() <= 0:
        raise ValueError(
            f"[bold red]Alert![/bold red] One of the occupancy values in the document is equal to {data_frame['aforo_100'].min()} below 0"
        )

    # Validating activity
    if not data_frame["actividad"].between(0, 2, inclusive="both").all():
        raise ValueError(
            "[bold red]Alert![/bold red] One of the activity values in the document is outside of the permitted input values 0, 1, 2"
        )

    # Validating permanencia
    if data_frame["permanencia"].min() <= 0:
        raise ValueError(
            f"[bold red]Alert![/bold red] I also wish time could me negative, but it's not. Permanence on a space cannot be equal to {data_frame['permanencia'].min()}"
        )

    return True
