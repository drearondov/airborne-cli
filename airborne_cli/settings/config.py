"""CLI module for config, hold the CLI commands as well as the logic for showing and updating the configuration file.
"""

import typer

from rich.console import Console
from typing_extensions import Annotated

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
config_app = typer.Typer(help="Modify configuration for Airborne CLI")


@config_app.command()
def show(
    all: Annotated[
        bool, typer.Option(help="Show all configurations available")
    ] = False,
    general: Annotated[
        bool, typer.Option(help="Show available options for general configuration.")
    ] = False,
    ach: Annotated[
        bool,
        typer.Option(
            help="Show available options to configure Required ACH calculations."
        ),
    ] = False,
    ashrae: Annotated[
        bool,
        typer.Option(
            help="Show available options to configure the ASHRAE ventilation requirements.",
        ),
    ] = False,
    graphics: Annotated[
        bool,
        typer.Option(help="Show available options to confgure graphic output."),
    ] = False,
) -> None:
    """
    Shows current configurations.
    """
    console = Console()

    if all is True:
        console.print(show_general())
        console.print(show_ach())
        console.print(show_ashrae())
        console.print(show_graphics())
    else:
        if general is True:
            console.print(show_general())

        if ach is True:
            console.print(show_ach())

        if ashrae is True:
            console.print(show_ashrae())

        if graphics is True:
            console.print(show_graphics())


@config_app.command()
def general(
    ach: Annotated[
        bool,
        typer.Option(
            help="Make Required ACH calculations with default values.",
        ),
    ] = settings["general"]["ach"],
    ashrae: Annotated[
        bool,
        typer.Option(
            help="Make ASHRAE ventilation requirements calculation with default values.",
        ),
    ] = settings["general"]["ashrae"],
    graphics: Annotated[
        bool,
        typer.Option(
            help="Make graphics during analysis (Requires kaleido and plotly to be installed).",
        ),
    ] = settings["general"]["graphics"],
    interactive: Annotated[
        bool,
        typer.Option(
            help="Toggle Interactive CLI",
        ),
    ] = settings["general"]["interactive"],
    save_graphics: Annotated[
        bool,
        typer.Option(
            help="Save the graphics made or just show them during analysis.",
        ),
    ] = settings["general"]["save_graphics"],
    save: Annotated[
        bool,
        typer.Option(
            help="Save results",
        ),
    ] = settings[
        "general"
    ]["save"],
    save_format: Annotated[
        SaveFormat,
        typer.Option(
            case_sensitive=False,
            help="Set the default format for saving calculation results. Currently supperted: csv and xlsx",
        ),
    ] = SaveFormat(settings["general"]["save_format"]),
    aforo: Annotated[
        list[float],
        typer.Option(
            help="Set default percentages to calculate occupancy",
        ),
    ] = settings["general"]["aforo"],
) -> None:
    """
    Sets general defaults for `run` command.
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
    max_risk: Annotated[
        float,
        typer.Option(
            min=0,
            max=100,
            help="Set maximum risk for required ACH calculations",
        ),
    ] = settings["ach"]["max_risk"],
    mask_default: Annotated[
        MaskType,
        typer.Option(
            help="Set mask type considered for occupants. Options: No mask, KN95, surgical, 3-ply cloth, 1-ply cloth, on_file.",
        ),
    ] = MaskType(settings["ach"]["mask_default"]),
    inf_percent: Annotated[
        list[int],
        typer.Option(
            help="Percentages of infected people to evaluate",
        ),
    ] = settings["ach"]["inf_percent"],
    viral_load: Annotated[
        ViralLoad,
        typer.Option(
            help="Viral load considered. Options: 8, 9, 10",
        ),
    ] = ViralLoad(settings["ach"]["viral_load"]),
    aerosol: Annotated[
        AerosolCutoff,
        typer.Option(
            help="Maximum size of particles considered aerosol",
        ),
    ] = AerosolCutoff(settings["general"]["default_aerosol"]),
) -> None:
    """
    Sets configuration for required ACH calculations.
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
    key_name: Annotated[str, typer.Argument(help="Name of the new room type to add")],
    rate_people: Annotated[
        float, typer.Argument(help="People rate according to ASHRAE 62.1")
    ],
    rate_area: Annotated[
        float, typer.Argument(help="Room rate according to ASHRAE 62.1")
    ],
) -> None:
    """
    Adds new room type for ASHRAE ventilation requirements calculations.
    """
    settings = load_config()

    settings["ashare"][f"{key_name}"] = {
        "rate_people": rate_people,
        "rate_area": rate_area,
    }

    save_config(settings)


@config_app.command()
def graphics(
    template: Annotated[
        GraphicTemplate,
        typer.Option(
            help="Sets default template for graphics. Availabe options: 'ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff', 'ygridoff', 'gridon', 'none'",
        ),
    ] = GraphicTemplate(settings["graphics"]["template"]),
    color_scheme: Annotated[
        list[str],
        typer.Option(
            help="List of colors to use in graphics",
        ),
    ] = settings["graphics"]["color_scheme"],
    format: Annotated[
        GraphicFormat,
        typer.Option(
            help="Default graphics format to save images in.",
        ),
    ] = GraphicFormat(settings["graphics"]["format"]),
    default_width: Annotated[
        int,
        typer.Option(
            min=0,
            help="Default width for images (in pixels)",
        ),
    ] = settings["graphics"]["default_width"],
    default_height: Annotated[
        int,
        typer.Option(
            min=0,
            help="Default height for images (in pixels)",
        ),
    ] = settings["graphics"]["default_height"],
    scale: Annotated[
        int,
        typer.Option(
            help="Scale for pictures, a higher number makes for better resolution, but it also increases file size",
        ),
    ] = settings["graphics"]["scale"],
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
