from typing import List

import typer
from rich.console import Console

from ..utils.options import AerosolCutoff
from ..utils.options import GraphicFormat
from ..utils.options import GraphicTemplate
from ..utils.options import MaskType
from ..utils.options import SaveFormat
from ..utils.options import ViralLoad
from .io import load_config
from .io import save_config
from .io import show_ach
from .io import show_ashrae
from .io import show_general
from .io import show_graphics


settings = load_config()


# Setting management editing CLI
config_app = typer.Typer(help="Modify configuration for Airborn CLI")


@config_app.command()
def show(
    all: bool = typer.Option(False, help="Show all configurations available"),
    general: bool = typer.Option(
        False, help="Show general configuration options available"
    ),
    ach: bool = typer.Option(
        False, help="Show required ACH calculation options available."
    ),
    ashrae: bool = typer.Option(
        False, help="Show ASHRAE calculation options available."
    ),
    graphics: bool = typer.Option(False, help="Show graphics options available."),
) -> None:
    """
    Shows current configurations.
    """
    console = Console()

    if all == True:
        console.print(show_general())
        console.print(show_ach())
        console.print(show_ashrae())
        console.print(show_graphics())
    else:
        if general == True:
            console.print(show_general())

        if ach == True:
            console.print(show_ach())

        if ashrae == True:
            console.print(show_ashrae())

        if graphics == True:
            console.print(show_graphics())


@config_app.command()
def general(
    ach: bool = typer.Option(
        settings["general"]["ach"],
        help="Set whether run commands makes ach calculations with default values automatically or not.",
    ),
    ashrae: bool = typer.Option(
        settings["general"]["ashrae"],
        help="Set whether run command makes ventilation calculation requirements according to ASHRAE recomendations with default values",
    ),
    graphics: bool = typer.Option(
        settings["general"]["graphics"],
        help="Set whether to make graphics during analysis (Requires kaleido and plotly to be installed). Results are saved on the same directory as the data file. Can be changed in settings.",
    ),
    interactive: bool = typer.Option(
        settings["general"]["interactive"],
        help="Sets whether the CLI is interactive or not.",
    ),
    save_graphics: bool = typer.Option(
        settings["general"]["save_graphics"],
        help="Set whether to save the graphics made or just show them during analysis",
    ),
    save: bool = typer.Option(
        settings["general"]["save"],
        help="Set whether to save results to files for analysis",
    ),
    save_format: SaveFormat = typer.Option(
        SaveFormat(settings["general"]["save_format"]),
        case_sensitive=False,
        help="Set the default format for saving calculation results. Currently supperted: csv and xlsx",
    ),
    aforo: List[float] = typer.Option(
        settings["general"]["aforo"],
        help="Set default percentages to calculate occupancy",
    ),
) -> None:
    """
    Set general defaults for run command.
    """
    settings = load_config()

    settings["general"]["ach"] = ach
    settings["general"]["aashrae"] = ashrae
    settings["general"]["graphics"] = graphics
    settings["general"]["interactive"] = interactive
    settings["general"]["save_graphics"] = save_graphics
    settings["general"]["save"] = save
    settings["general"]["save_format"] = save_format
    settings["general"]["aforo"] = aforo

    save_config(settings)


@config_app.command()
def required_ach(
    max_risk: float = typer.Option(
        settings["ach"]["max_risk"],
        min=0,
        max=100,
        help="Set maximum risk for ACH calculations",
    ),
    mask_default: MaskType = typer.Option(
        MaskType(settings["ach"]["mask_default"]),
        help="Set mask type considered for occupants. Options: No mask, KN95, surgical, 3-ply cloth, 1-ply cloth, on_file",
    ),
    inf_percent: List[int] = typer.Option(
        settings["ach"]["inf_percent"],
        help="Percentages of infected people to evaluate",
    ),
    viral_load: ViralLoad = typer.Option(
        ViralLoad(settings["ach"]["viral_load"]),
        help="Viral load considered. Options: 8, 9, 10",
    ),
    aerosol: AerosolCutoff = typer.Option(
        AerosolCutoff(settings["ach"]["aerosol"]),
        help="Maximum size of particles considered aerosol",
    ),
) -> None:
    """
    Sets configuration for ACH calculations.
    """
    settings = load_config()

    settings["ach"]["max_risk"] = max_risk
    settings["ach"]["max_default"] = mask_default.value
    settings["ach"]["inf_percent"] = inf_percent
    settings["ach"]["viral_load"] = viral_load
    settings["ach"]["aerosil"] = aerosol.value

    save_config(settings)


@config_app.command()
def ashrae(
    key_name: str = typer.Argument(..., help="Name of the new room type to add"),
    rate_people: float = typer.Argument(
        ..., help="People rate according to ASHRAE 62.1"
    ),
    rate_area: float = typer.Argument(..., help="Room rate according to ASHRAE 62.1"),
) -> None:
    """
    Adds new room type for ASHRAE calculations
    """
    settings = load_config()

    settings["ashare"][f"{key_name}"] = {
        "rate_people": rate_people,
        "rate_area": rate_area,
    }

    save_config(settings)


@config_app.command()
def graphics(
    template: GraphicTemplate = typer.Option(
        GraphicTemplate(settings["graphics"]["template"]),
        help="Sets default template for graphics",
    ),
    color_scheme: List[str] = typer.Option(
        settings["graphics"]["color_scheme"], help="List of colors to use in graphics"
    ),
    format: GraphicFormat = typer.Option(
        GraphicFormat(settings["graphics"]["format"]),
        help="Default graphics format to save images in.",
    ),
    default_width: int = typer.Option(
        settings["graphics"]["default_width"],
        min=0,
        help="Default width for images (in pixels)",
    ),
    default_height: int = typer.Option(
        settings["graphics"]["default_height"],
        min=0,
        help="Default height for images (in pixels)",
    ),
    scale: int = typer.Option(
        settings["graphics"]["scale"],
        help="Scale for pictures, a higher number makes for better resolution, but it also increases image size",
    ),
) -> None:
    """
    Set graphic defaults.
    """
    settings = load_config()

    settings["graphics"]["template"] = template
    settings["graphics"]["color_scheme"] = color_scheme
    settings["graphics"]["format"] = format
    settings["graphics"]["default_width"] = default_width
    settings["graphics"]["default_height"] = default_height
    settings["graphics"]["scale"] = scale

    save_config(settings)
