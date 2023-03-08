from pathlib import Path
from typing import Optional

import pandas as pd


def load_data(data_in: Path) -> tuple[pd.DataFrame, Path]:
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
                "Format not supported, only .xlsx, .csv and .json are supported"
            )

    if check_data(data.columns):
        return (data, data_folder)
    else:
        raise ValueError("Check that input data contains all the required columns")


def check_data(data_columns: pd.Index) -> bool:
    """Checks if the Data Frame entered has the appropriate columns and data types.

    Args:
        data (pd.DataFrame): Data frame entered
    """
    required_columns = ["area", "altura", "aforo", "actividad", "permanencia"]

    return all(parameter in data_columns for parameter in required_columns)


def save_data(
    data_folder: Path, save_format: str, data_to_save: dict[str, pd.DataFrame]
) -> Path:
    """Saves data results to folder in format specified.

    Args:
        data_folder (Path): Folder where data is stored
        save_format (str): Format to store data
        **data_to_save: Names and pd.DataFrame to save

    Returns:
        Path: Path of the results folder
    """

    results_folder = data_folder.joinpath("results")
    results_folder.mkdir()

    if save_format == "csv":
        for name, df in data_to_save.items():
            df.to_csv(results_folder.joinpath(f"{name}.csv"))
            # data.to_csv(results_folder.joinpath("results.csv"))
            # risk_ach_data.to_csv(results_folder.joinpath("risk_ach.csv"))
            # aerosol_risk_data.to_csv(results_folder.joinpath("risk_flow_aorosol.csv"))
    elif save_format == "xlsx":
        for name, df in data_to_save.items():
            df.to_excel(results_folder.joinpath(f"{name}.xlsx"))
            # data.to_excel(results_folder.joinpath("results.xlsx"))
            # risk_ach_data.to_excel(results_folder.joinpath("risk_ach.xlsx"))
            # aerosol_risk_data.to_excel(results_folder.joinpath("rishk_flow_aorosol.xlsx"))
    else:
        print("[bold red]Alert![/bold red] Extension not supported")

    return results_folder


def graphics_output(
    results_folder: Path,
    risk_ach_graphics: dict,
    aerosol_risk_graphics: Optional[dict] = None,
) -> None:
    """Saves graphics to results folder.

    Args:
        results_folder (Path): Folder where the graphics are going to be stored
        risk_ach_graphics (dict): Dictionary where risk graphics are stored
        aerosol_risk_graphics (dict): Dictionary where aerosol graphics are stored
    """
    risk_ach_graphs = results_folder.joinpath("risk_ach")
    risk_ach_graphs.mkdir()
    risk_aerosol_graphs = results_folder.joinpath("risk_aerosol")
    risk_aerosol_graphs.mkdir()

    for name, figure in risk_ach_graphics.items():
        figure.write_image(risk_ach_graphs.joinpath(f"{name}.png"))

    if aerosol_risk_graphics != None:
        for name, figure in aerosol_risk_graphics.items():
            figure.write_image(risk_aerosol_graphs.joinpath(f"{name}.png"))
