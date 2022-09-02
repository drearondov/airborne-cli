import pandas as pd

from pathlib import Path


def load_data(data_in: str) -> tuple:
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

    return (data, data_folder)


def save_data(
    data: pd.DataFrame,
    data_folder: Path,
    save_format: str,
    risk_ach_data: pd.DataFrame = None,
    aerosol_risk_data: pd.DataFrame = None,
) -> Path:
    """Saves data results to folder in format specified.

    Args:
        data (pd.DataFrame): Main calculation results for rooms
        data_folder (Path): Folder where data is stored
        save_format (str): Format to store data
        risk_ach_data (pd.DataFrame, optional): _description_. Defaults to None.
        aerosol_risk_data (pd.DataFrame, optional): _description_. Defaults to None.
    """

    results_folder = data_folder.joinpath("results").mkdir()

    if save_format == "csv":
        data.to_csv(results_folder.joinpath("results.csv"))
        risk_ach_data.to_csv(results_folder.joinpath("risk_ach.csv"))
        aerosol_risk_data.to_csv(results_folder.joinpath("rishk_flow_aorosol.csv"))
    elif save_format == "xlsx":
        data.to_excel(results_folder.joinpath("results.xlsx"))
        risk_ach_data.to_excel(results_folder.joinpath("risk_ach.xlsx"))
        aerosol_risk_data.to_excel(results_folder.joinpath("rishk_flow_aorosol.xlsx"))
    else:
        print("[bold red]Alert![/bold red] Extension not supported")

    return results_folder


def graphics_output(
    results_folder: Path,
    risk_ach_graphics: dict,
    aerosol_risk_graphics: dict
) -> None:
    """Saves graphics to results folder.

    Args:
        results_folder (Path): Folder where the graphics are going to be stored
        risk_ach_graphics (dict): Dictionary where risk graphics are stored
        aerosol_risk_graphics (dict): Dictionary where aerosol graphics are stored
    """
    risk_ach_graphs = results_folder.joinpath("risk_ach").mkdir()
    risk_aerosol_graphs = results_folder.joinpath("risk_ach").mkdir()

    for name, figure in risk_ach_graphics.items():
        figure.write_image(risk_ach_graphs.joinpath(f"{name}.png"))

    for name, figure in aerosol_risk_graphics.items():
        figure.write_image(risk_aerosol_graphs.joinpath(f"{name}.png"))