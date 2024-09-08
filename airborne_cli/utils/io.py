from pathlib import Path

import pandas as pd
import plotly.graph_objects as go  # type:ignore

from .validation import validate_data_types
from .validation import validate_existing_columns
from .validation import validate_input


def load_data(data_in: Path) -> tuple[pd.DataFrame, Path] | None:
    """Loads the data from the specified path

    Args:
        data_path (str): Data path for processing

    Returns:
        tuple: Tuple containing the data frame as well as the path to the data folder.
    """
    data_path = Path(data_in)
    data_format = data_path.suffix
    data_folder = data_path.parent

    match data_format:
        case ".xlsx":
            data = pd.read_excel(data_path)
        case ".csv":
            data = pd.read_csv(data_path)
        case ".json":
            data = pd.read_json(data_path)
        case _:
            raise ValueError(
                f"[bold red]Alesrt![/bold red]Format {data_format} not supported. Only .xlsx, .csv and .json are supported"
            )

    if check_data(data):
        return (data, data_folder)

    return None


def check_data(data_frame: pd.DataFrame) -> bool:
    """Checks if the Data Frame entered has the appropriate columns and data types.

    Args:
        data (pd.DataFrame): Data frame entered

    Returns:
        bool: does the data pass the validation
    """
    validate_existing_columns(data_frame.columns)
    validate_data_types(data_frame)
    validate_input(data_frame)

    return True


def make_results_folder(data_folder: Path) -> Path:
    """Created a folder to house results

    Args:
        data_folder (Path): Folder where input data is stored

    Returns:
        Path: Path of the results folder
    """
    results_folder = data_folder.joinpath("results")
    results_folder.mkdir()

    return results_folder


def save_data(
    results_folder: Path, save_format: str, data_to_save: dict[str, pd.DataFrame]
) -> None:
    """Saves data results to folder in format specified.

    Args:
        data_folder (Path): Folder where data is stored
        save_format (str): Format to store data
        data_to_save(dict[str, pd.DataFrame]): Names and pd.DataFrame to save
    """

    match save_format:
        case "csv":
            for name, df in data_to_save.items():
                df.to_csv(results_folder.joinpath(f"{name}.csv"))
        case "xlsx":
            for name, df in data_to_save.items():
                df.to_excel(results_folder.joinpath(f"{name}.xlsx"))
        case _:
            raise ValueError("[bold red]Alert![/bold red] Extension not supported")


def graphics_output(
    results_folder: Path,
    graphics: dict[str, dict[str, go.Figure]],
) -> None:
    """Saves graphics to results folder.

    Args:
        results_folder (Path): Folder where the graphics are going to be stored
        risk_ach_graphics (dict): Dictionary where risk graphics are stored
        aerosol_risk_graphics (dict): Dictionary where aerosol graphics are stored
    """
    for graphics_group, graphics_dict in graphics.items():
        match graphics_group:
            case "risk_ach_inf_graphics":
                graph_path = results_folder.joinpath("risk_ach_inf")
                graph_path.mkdir()

            case "risk_ach_aerosol_graphics":
                graph_path = results_folder.joinpath("risk_ach_aerosol")
                graph_path.mkdir()

        for name, figure in graphics_dict.items():
            figure.write_image(graph_path.joinpath(f"{name}.png"))
