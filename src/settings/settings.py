import typer

from typing import List

from config import settings
from io import load_config
from src.utils.options import AerosolCutoff, SaveFormat, MaskType, ViralLoad, GraphicTemplate, GraphicFormat


app = typer.Typer(help="Modify configuration for Airborn CLI", rich_markup_mode="rich")


@app.command()
def show() -> None:
    """
    Shows current configurations.
    """
    config = load_config()


@app.command()
def general(
    ach: bool = typer.Option(settings.general.ach, help="Set whether run commands makes ach calculations with default values automatically or not."),
    ashrae: bool = typer.Option(settings.general.ashrae, "Set whether run command makes ventilation calculation requirements according to ASHRAE recomendations with default values"),
    graphics: bool = typer.Option(settings.general.graphics, help="Set whether to make graphics during analysis (Requires kaleido and plotly to be installed). Results are saved on the same directory as the data file. Can be changed in settings."),
    interactive: bool = typer.Option(settings.general.interactive, help="Sets whether the CLI is interactive or not."),
    save_graphics: bool = typer.Option(settings.general.save_graphics, help="Set whether to save the graphics made or just show them during analysis"),
    save: bool = typer.Option(settings.general.save, help="Set whether to save results to files for analysis"),
    save_format: SaveFormat = typer.Option(SaveFormat(settings.general.save_format), case_sensitive=False, help="Set the default format for saving calculation results. Currently supperted: csv and xlsx"),
    aforo: List[float] = typer.Option(settings.general.aforo, help="Set default percentages to calculate occupancy")
    ) -> None:
    """
    Set general defaults for run command.
    """
    pass


@app.command()
def ach(
    max_risk: int = typer.Option(settings.ach.mask_risk, min=0, max=100, help="Set maximum risk for ACH calculations."),
    mask_default: MaskType = typer.Option(MaskType(settings.ach.mask_default), help="Set mask type considered for occupants. Options: No mask, KN95, surgical, 3-ply cloth, 1-ply cloth, on_file"),
    inf_percent: List[int] = typer.Option(settings.ach.inf_percent, help="Percentages of infected people to evaluate"),
    viral_load: ViralLoad = typer.Option(ViralLoad(settings.ach.viral_load), help="Viral load considered. Options: 8, 9, 10"),
    aerosol: AerosolCutoff = typer.Option(AerosolCutoff(settings.ach.aerosol), help="Maximum size of particles considered aerosol"),
) -> None:
    """
    Sets configuration for ACH calculations.
    """
    pass


@app.command()
def ashrae(
    key_name: str = typer.Argument(..., help="Name of the new room type to add"),
    rate_people: float = typer.Argument(..., help="People rate according to ASHRAE 62.1"),
    rate_area: float = typer.Argument(..., help="Room rate according to ASHRAE 62.1")
) -> None:
    """
    Adds new room type for ASHRAE calculations
    """
    pass


@app.command()
def graphics(
    template: GraphicTemplate = typer.Option(GraphicTemplate(settings.graphics.template), help="Sets default template for graphics"),
    color_scheme: List[str] = typer.Option(settings.graphics.color_sheme, help="List of colors to use in graphics"),
    format: GraphicFormat = typer.Option(GraphicFormat(settings.graphics.format), help="Default graphics format to save images in."),
    default_width: int = typer.Option(settings.graphics.default_width, min=0, help="Default width for images (in pixels)"),
    default_height: int = typer.Option(settings.graphics.default_height, min=0, help="Default height for images (in pixels)"),
    scale: int = typer.Option(settings.gaphics.scale, help="Scale for pictures, a higher number makes for better resolution, but it also increases image size")
) -> None:
    """
    Set graphic defaults.
    """
    pass
