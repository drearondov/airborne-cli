from itertools import product
from math import ceil
from pathlib import Path
from typing_extensions import Annotated

import typer

from .lib.ach import ach_required
from .lib.ashrae import ashrae_calculation
from .lib.graphics import risk_ach_graph, risk_aerosol_graph
from .lib.risk import ach_risk_inf_percent_calculation, ach_risk_aerosol_calculation
from .settings.config import config_app, settings
from .utils.io import graphics_output, load_data, save_data, make_results_folder
from .utils.options import AerosolCutoff, MaskType, SaveFormat, ViralLoad


app = typer.Typer(
    help="CLI interface for Air Quality analysis and Air Changes per Hour required for multiple indoor areas"
)
app.add_typer(config_app, name="config")


@app.command()
def run(
    data_in: Annotated[
        Path,
        typer.Argument(
            ...,
            exists=True,
            help="Filepath where the data for analysis is stored. To know the required fields for the data and the supported file formats read the docs",
        ),
    ],
    ach: Annotated[
        bool,
        typer.Option(
            settings["general"]["ach"],
            help="Calculate Required ACH calculations with default values",
        ),
    ],
    ashrae: Annotated[
        bool,
        typer.Option(
            settings["general"]["ashrae"],
            help="Calculate Room Ventilation Requirements according to ASHRAE recomendations with default values",
        ),
    ],
    risk: Annotated[
        bool,
        typer.Option(
            settings["general"]["risk"],
            help="Perform risk analysis for different conditions",
        ),
    ],
    graphics: Annotated[
        bool,
        typer.Option(
            settings["general"]["graphics"],
            help="Make graphics during analysis (Requires kaleido and plotly to be installed)",
        ),
    ],
    save_graphics: Annotated[
        bool,
        typer.Option(
            settings["general"]["save_graphics"],
            help="Save the graphics made. If `false`, program wil just show them during analysis",
        ),
    ],
    save_results: Annotated[
        bool,
        typer.Option(
            settings["general"]["save"], help="Save results to files for analysis"
        ),
    ],
    save_format: Annotated[
        SaveFormat,
        typer.Option(
            SaveFormat(settings["general"]["save_format"]),
            case_sensitive=False,
            help="Format for saving calculation results. Currently supperted: .csv and .xlsx",
        ),
    ],
) -> None:
    """
    Shortcut function to run calculation with default values.
    By default runs Required ACH, ASHRAE ventilation requirement calculations using default values and makes and saves graphics.
    To see configuration options and default values use airborne config --help
    """
    # Setup input and output
    (data, data_folder) = load_data(data_in)
    if save_results or save_graphics:
        results_folder = make_results_folder(data_folder)

    mask_type = MaskType(settings["ach"]["mask_default"])
    viral_load = ViralLoad(settings["ach"]["viral_load"])
    aerosol = AerosolCutoff(settings["ach"]["aerosol"])

    results_data = {}

    # Required ACH calculations
    if ach:
        for occupancy, inf_percent in product(
            settings["general"]["aforo"], settings["ach"]["inf_percent"]
        ):
            data[f"ACH_{occupancy}_aforo_{inf_percent}_inf"] = data.apply(
                lambda x: ach_required(
                    x["Area"],
                    x["Altura"],
                    ceil(x["Aforo_100"] * 0.5),
                    x["Actividad"],
                    x["Permanencia"],
                    set_risk=settings["general"]["max_risk"] / 100,
                    mask_type=int(mask_type.name[-1]),
                    inf_percent=inf_percent,
                    viral_load=int(viral_load.value),
                    cutoff_type=int(aerosol.name[-1]),
                ),
                axis=1,
            )

    # ASHRAE requirements calculations
    if ashrae:
        for occupancy in settings["general"]["aforo"]:
            data = ashrae_calculation(data, occupancy, settings["ashrae"])

    results_data["ach-ashrae"] = data

    # Risk calculations
    if risk:
        if settings["risk"]["risk_inf"]:
            results_data["risk_ach_inf_data"] = ach_risk_inf_percent_calculation(
                data, settings["ach"]["inf_percent"]
            )

        if settings["risk"]["risk_aerosol"]:
            results_data["risk_ach_aerosol_data"] = ach_risk_aerosol_calculation(
                data, settings["ach"]["aerosol"]
            )

    # Making graphics
    if graphics:
        graphic_results = {}

        if settings["risk"]["risk_inf"]:
            graphic_results["risk_ach_inf_graphics"] = risk_ach_graph(
                results_data["risk_ach_inf_data"], settings["graphics"]["color_scheme"]
            )
        if settings["risk"]["risk_aerosol"]:
            graphic_results["risk_ach_aerosol_graphics"] = risk_aerosol_graph(
                results_data["risk_ach_aerosol_data"],
                settings["graphics"]["color_scheme"],
            )

        if save_graphics:
            graphics_output(results_folder, graphic_results)

    # Saving data
    if save_results:
        save_data(data_folder, save_format.value, results_data)


@app.command(name="ach")
def required_ach(
    data_in: Annotated[
        Path,
        typer.Argument(
            ...,
            exists=True,
            help="Filepath where the data for analysis is stored. To know the required fields for the data, read the docs.",
        ),
    ],
    max_risk: Annotated[
        float,
        typer.Option(
            settings["ach"]["max_risk"],
            min=0,
            max=100,
            help="Maximum risk acceptable for calculation",
        ),
    ],
    mask_type: Annotated[
        MaskType,
        typer.Option(
            MaskType(settings["ach"]["mask_default"]),
            help="Mask type considered for occupants. Options: No mask, KN95, surgical, 3-ply cloth, 1-ply cloth, on_file",
        ),
    ],
    inf_percent: Annotated[
        list[float],
        typer.Option(
            settings["ach"]["inf_percent"],
            help="Percentages of infected people to evaluate",
        ),
    ],
    viral_load: Annotated[
        ViralLoad,
        typer.Option(
            ViralLoad(settings["ach"]["viral_load"]),
            help="Viral load considered. Options: 8, 9, 10",
        ),
    ],
    aerosol: Annotated[
        AerosolCutoff,
        typer.Option(
            AerosolCutoff(settings["general"]["default_aerosol"]),
            help="Maximum size of particles considered aerosol",
        ),
    ],
    aforo: Annotated[
        list[float],
        typer.Option(
            settings["general"]["aforo"], help="Percentages to calculate occupancy"
        ),
    ],
    save: Annotated[
        bool,
        typer.Option(
            settings["general"]["save"], help="Save results to files for analysis"
        ),
    ],
    save_format: Annotated[
        SaveFormat,
        typer.Option(
            SaveFormat(settings["general"]["save_format"]),
            help="Format for saving calculation results. Currently supperted: csv and xlsx",
        ),
    ],
) -> None:
    """
    Make Required ACH calculations with custom parameters.
    """
    (data, data_folder) = load_data(data_in)

    # Checking options
    for percentage in inf_percent:
        if (percentage < 0) or (percentage > 100):
            raise ValueError(f"{percentage} is not on the 0% to 100% range")

    for people in aforo:
        if type(people) not in [float, int]:
            raise TypeError("Ocuupancy percentage can only be integers or decimals")
        if people < 0:
            raise ValueError(
                "There cannot be less than zero people in a room right? ¯\\_(ツ)_/¯"
            )

    # Making the calculations
    for occupancy, percent in product(aforo, inf_percent):
        data[f"ACH_{occupancy}_aforo_{percent}_inf"] = data.apply(
            lambda x: ach_required(
                x["Area"],
                x["Altura"],
                ceil(x["Aforo_100"] * 0.5),
                x["Actividad"],
                x["Permanencia"],
                set_risk=max_risk / 100,
                mask_type=int(mask_type.name[-1])
                if mask_type != MaskType.i5
                else x["Mask Type"],
                inf_percent=percent,
                viral_load=int(viral_load.value),
                cutoff_type=int(aerosol.name[-1]),
            ),
            axis=1,
        )

    if save:
        results_folder = make_results_folder(data_folder)
        save_data(results_folder, save_format.value, {"required_ach": data})


@app.command()
def ashrae(
    data_in: Annotated[
        Path,
        typer.Argument(
            ...,
            exists=True,
            help="Filepath where the data for analysis is stored. To know the required fields for the data, read the docs.",
        ),
    ],
    aforo: Annotated[
        list[float],
        typer.Option(
            settings["general"]["aforo"], help="Percentages to calculate occupancy"
        ),
    ],
    save: Annotated[
        bool,
        typer.Option(
            settings["general"]["save"], help="Save results to files for analysis"
        ),
    ],
    save_format: Annotated[
        SaveFormat,
        typer.Option(
            SaveFormat(settings["general"]["save_format"]),
            help="Format for saving calculation results. Currently supperted: csv and xlsx",
        ),
    ],
) -> None:
    """
    Makes recommended flow calculations for analysis according to ASHRAE recomendations with custom parameters.
    """
    (data, data_folder) = load_data(data_in)

    for people in aforo:
        if people < 0:
            raise ValueError(
                "There cannot be less than zero people in a room right? ¯\\_(ツ)_/¯"
            )

    for occupancy in aforo:
        data = ashrae_calculation(data, occupancy, settings["ashrae"])

    if save:
        results_folder = make_results_folder(data_folder)
        save_data(results_folder, save_format.value, {"required_ventilation": data})


@app.command(name="risk")
def risk_analysis(
    data_in: Annotated[
        Path,
        typer.Argument(
            ...,
            exists=True,
            help="Filepath where the data for analysis is stored. To know the required fields for the data, read the docs.",
        ),
    ],
    risk_inf: Annotated[
        bool,
        typer.Option(
            settings["risk"]["risk_inf"],
            help="Make risk calculations for differente percentage of infected people",
        ),
    ],
    risk_aerosol: Annotated[
        bool,
        typer.Option(
            settings["risk"]["risk_aerosol"],
            help="Make risk calculations for different aerosol cutoff values",
        ),
    ],
    graphics: Annotated[
        bool,
        typer.Option(
            settings["general"]["graphics"],
            help="Make graphics during analysis (Requires kaleido and plotly to be installed). Results are saved on the same directory as the data file. Can be changed in settings.",
        ),
    ],
    save_graphics: Annotated[
        bool,
        typer.Option(
            settings["general"]["save_graphics"],
            help="Save the graphics made or just show them during analysis",
        ),
    ],
    save: Annotated[
        bool,
        typer.Option(
            settings["general"]["save"], help="Save results to files for analysis"
        ),
    ],
    save_format: Annotated[
        SaveFormat,
        typer.Option(
            SaveFormat(settings["general"]["save_format"]),
            help="Format for saving calculation results. Currently supperted: csv and xlsx",
        ),
    ],
) -> None:
    """
    Perform risk analysis calculations and graphics.
    """
    (data, data_folder) = load_data(data_in)
    if save or save_graphics:
        results_folder = make_results_folder(data_folder)

    risk_results = {}

    if risk_inf:
        risk_results["risk_ach_inf_data"] = ach_risk_inf_percent_calculation(
            data, settings["ach"]["inf_percent"]
        )

    if risk_aerosol:
        risk_results["risk_ach_aerosol_data"] = ach_risk_aerosol_calculation(
            data, settings["ach"]["aerosol"]
        )

    # Making graphics
    graphic_results = {}

    if graphics:
        if risk_inf:
            graphic_results["risk_ach_inf_graphics"] = risk_ach_graph(
                risk_results["risk_ach_inf_data"], settings["graphics"]["color_scheme"]
            )
        if risk_aerosol:
            graphic_results["risk_ach_aerosol_graphics"] = risk_aerosol_graph(
                risk_results["risk_ach_aerosol_data"],
                settings["graphics"]["color_scheme"],
            )
    else:
        save_graphics = False

    # Saving data
    if save:
        save_data(data_folder, save_format.value, risk_results)

    if save_graphics:
        graphics_output(results_folder, graphic_results)


# @app.command(name="dash")
# def dashboard_app(
#     data_in: Path = typer.Argument(..., exists=True, help="Filepath where the data for analysis is stored. To know the required fields for the data, read the docs.")
# ) -> None:
#     """
#     Fires up a dashboard for analysis.
#     """
