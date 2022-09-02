#TODO: Major refactoring
import pandas as pd
import plotly.io as pio
import typer

from itertools import product
from math import ceil
from pathlib import Path
from typing import List

#FIXME: Routing imports
from config import settings
from setup import setup 
from src.ach.ach import ACH_calculation
from src.lib.ashrae import ASHRAE_calculation
from src.lib.graphics import risk_ach_graph, risk_flow_graph
from src.io import load_data, save_data, graphics_output
from src.options import AerosolCutoff, SaveFormat, MaskType, ViralLoad
from src.ach.risk import ach_risk_calculation, aerosol_risk_calculation


app = typer.Typer(help="CLI interface for ACH and air quality analysis for indoor areas",rich_markup_mode="rich")
app.add_typer(setup.app, name="config")


@app.callback()
def main():
    pio.templates.default = settings.graphics.template
    pio.kaleido.scope.default_format = settings.graphics.format
    pio.kaleido.scope.default_width = settings.graphics.default_width
    pio.kaleido.scope.default_height = settings.graphics.default_height
    pio.kaleido.scope.default_scale = settings.graphics.scale


@app.command()
def run(
    data_in: Path = typer.Argument(..., exists=True, help="Filepath where the data for analysis is stored. To know the required fields for the data and the supported file formats read the docs."),
    ach: bool = typer.Option(settings.general.ach, help="Do ACH calculations with default values"),
    ashrae: bool = typer.Option(settings.general.ashrae, "Do ventilation calculation requirements according to ASHRAE recomendations with default values"),
    graphics: bool = typer.Option(settings.general.graphics, help="Make graphics during analysis (Requires kaleido and plotly to be installed). Results are saved on the same directory as the data file. Can be changed in settings."),
    save_graphics: bool = typer.Option(settings.general.save_graphics, help="Save the graphics made or just show them during analysis"),
    save: bool = typer.Option(settings.general.save, help="Save results to files for analysis"),
    save_format: SaveFormat = typer.Option(SaveFormat(settings.general.save_format), case_sensitive=False, help="Format for saving calculation results. Currently supperted: csv and xlsx")
) -> None:
    """
    Runs calculations using default values. To see or change values run airborne config --help
    """
    (data, data_folder) = load_data(data_in)

    mask_type = MaskType(settings.ach.mask_default)
    viral_load = ViralLoad(settings.ach.viral_load)
    aerosol = AerosolCutoff(settings.ach.aerosol)

    if ach == True:
        for occupancy, inf_percent in product(settings.general.aforo, settings.ach.inf_percent):
            data[f"ACH_{occupancy}_aforo_{inf_percent}_inf"] = data.apply(
                lambda x: ACH_calculation(
                    x["Area"],
                    x["Altura"],
                    ceil(x["Aforo_100"]*0.5),
                    x["Actividad"],
                    x["Permanencia"],
                    set_risk=settings.general.max_risk/100,
                    mask_type=int(mask_type.name[-1]),
                    inf_percent=inf_percent,
                    viral_load=viral_load.value,
                    cutoff_type=int(aerosol.name[-1])
                    ), axis=1
                )

    if ashrae == True:
        for occupancy in settings.general.aforo:
            data = ASHRAE_calculation(data, occupancy, settings.ashrae)

    if graphics == True:
        risk_ach_data = ach_risk_calculation(data, settings.ach.inf_percent)
        risk_ach_graphics = risk_ach_graph(risk_ach_data, settings.graphics.color_scheme)

        aerosol_risk_data = aerosol_risk_calculation(data)
        aerosol_risk_graphics = risk_flow_graph(aerosol_risk_data, settings.graphics. color_scheme)

    if save == True:
        results_folder = save_data(data, data_folder, save_format.value, risk_ach_data, aerosol_risk_data)

        if save_graphics == True:
            graphics_output(results_folder, risk_ach_graphics, aerosol_risk_graphics)

#TODO: Make ACH CLI
@app.command()
def ach(
    data_in: Path = typer.Argument(..., exists=True, help="Filepath where the data for analysis is stored. To know the required fields for the data, read the docs."),
    max_risk: int = typer.Option(settings.ach.max_risk, min=0, max=100, help="Maximum risk acceptable for calculation"),
    mask_type: MaskType = typer.Option(MaskType(settings.ach.mask_default), help="Mask type considered for occupants. Options: No mask, KN95, surgical, 3-ply cloth, 1-ply cloth, on_file"),
    inf_percent: List[int] = typer.Option(settings.ach.inf_percent, help="Percentages of infected people to evaluate"),
    viral_load: ViralLoad = typer.Option(ViralLoad(settings.ach.viral_load), help="Viral load considered. Options: 8, 9, 10"),
    aerosol: AerosolCutoff = typer.Option(AerosolCutoff(settings.ach.aerosol), help="Maximum size of particles considered aerosol"),
    aforo: List[float] = typer.Option(settings.general.aforo, help="Percentages to calculate occupancy"),
    graphics: bool = typer.Option(settings.general.graphics, help="Make graphics during analysis (Requires kaleido and plotly to be installed). Results are saved on the same directory as the data file. Can be changed in settings."),
    save_graphics: bool = typer.Option(settings.general.save_graphics, help="Save the graphics made or just show them during analysis"),
    save: bool = typer.Option(settings.general.save, help="Save results to files for analysis"),
    save_format: SaveFormat = typer.Option(SaveFormat(settings.general.save_format), help="Format for saving calculation results. Currently supperted: csv and xlsx")
) -> None:
    """
    Makes ACH calculations with custom parameters.
    """
    (data, data_folder) = load_data(data_in)

    # Checking options
    for percentage in inf_percent:
        if (percentage < 0) or (percentage > 100):
            raise ValueError(f"{percentage} is not on the 0% to 100% range")

    for people in aforo:
        if people < 0:
            raise ValueError("There cannot be less than zero people in a room right? ¯\_(ツ)_/¯")

    # Making the calculations
    for occupancy, percent in product(aforo, inf_percent):
        data[f"ACH_{occupancy}_aforo_{percent}_inf"] = data.apply(
            lambda x: ACH_calculation(
                x["Area"],
                x["Altura"],
                ceil(x["Aforo_100"]*0.5),
                x["Actividad"],
                x["Permanencia"],
                set_risk=max_risk/100,
                mask_type=int(mask_type.name[-1]) if mask_type != MaskType.i5 else x["Mask Type"],
                inf_percent=percent,
                viral_load=viral_load.value,
                cutoff_type=int(aerosol.name[-1])
                ), axis=1
            )

    # Making graphics
    if graphics == True:
        risk_ach_data = ach_risk_calculation(data, settings.ach.inf_percent)
        risk_ach_graphics = risk_ach_graph(risk_ach_data, settings.graphics.color_scheme)

        aerosol_risk_data = aerosol_risk_calculation(data)
        aerosol_risk_graphics = risk_flow_graph(aerosol_risk_data, settings.graphics. color_scheme)

    if save == True:
        results_folder = save_data(data, data_folder, save_format.value, risk_ach_data, aerosol_risk_data)

        if save_graphics == True:
            save_graphics(results_folder, risk_ach_graphics, aerosol_risk_graphics)

#TODO: Make ASHRAE CLI
@app.command()
def ashrae(
    data_in: Path = typer.Argument(..., exists=True, help="Filepath where the data for analysis is stored. To know the required fields for the data, read the docs."),
    aforo: List[float] = typer.Option(settings.general.aforo, help="Percentages to calculate occupancy"),
    save: bool = typer.Option(settings.general.save, help="Save results to files for analysis"),
    save_format: SaveFormat = typer.Option(SaveFormat(settings.general.save_format), help="Format for saving calculation results. Currently supperted: csv and xlsx")
) -> None:
    """
    Makes recommended flow calculations for analysis according to ASHRAE recomendations with custom parameters.
    """
    (data, data_folder) = load_data(data_in)

    for people in aforo:
        if people < 0:
            raise ValueError("There cannot be less than zero people in a room right? ¯\_(ツ)_/¯")

    for occupancy in aforo:
        data = ASHRAE_calculation(data, occupancy, settings.ashrae)

    if save == True:
        _ = save_data(data, data_folder, save_format.value)
