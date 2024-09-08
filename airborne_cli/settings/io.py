"""
Module tha hold the import and exprt functions for the configuration app.
"""

from pathlib import Path
from typing import Any

import tomlkit
from rich import print
from rich.panel import Panel
from rich.table import Table
from tomlkit import document
from tomlkit import nl
from tomlkit import table


def load_config() -> dict[str, Any]:
    """Loads TOML configuration file and returns a dictionary with all the variables.

    Returns:
        TOMLDocument: Dictionary with settings
    """
    if Path("airborne_cli/settings.toml").exists():
        with open("airborne_cli/settings.toml", encoding="utf-8") as settings_file:
            config = tomlkit.load(settings_file)

        return dict(config)
    else:
        print(
            "[bold red]Alert![/bold red] Settings file not found. Generating default file."
        )
        config = generate_config()
        save_config(config)
        return config


def generate_config() -> tomlkit.TOMLDocument:
    """Generates and saves new config file if for whatver reason default one gets deleted or the user wants to go back to the defaults.

    Returns:
        TOMLDocument: Dictionary with default settings
    """
    config = document()

    general = table()
    ach = table()
    ashrae = table()
    graphics = table()

    general["ach"] = False
    general["ashrae"] = True
    general["risk"] = True
    general["graphics"] = True
    general["interactive"] = False
    general["save_graphics"] = True
    general["save"] = True
    general["save_format"] = "csv"
    general["aforo"] = [30.0, 40.0, 50.0, 70.0, 100.0]
    general["default_aerosol"] = "40"

    ach["max_risk"] = 3.0
    ach["mask_default"] = "KN95"
    ach["inf_percent"] = [10.0]
    ach["viral_load"] = "10"
    ach["aerosol"] = ["20", "40", "100"]

    ashrae["oficina"] = {"rate_people": 2.5, "rate_area": 0.3}
    ashrae["teatro"] = {"rate_people": 5, "rate_area": 0.3}
    ashrae["aula"] = {"rate_people": 3.8, "rate_area": 0.3}
    ashrae["taller"] = {"rate_people": 5, "rate_area": 0.9}
    ashrae["laboratorio"] = {"rate_people": 5, "rate_area": 0.9}
    ashrae["laboratorio_computacion"] = {"rate_people": 5, "rate_area": 0.6}

    graphics["template"] = "plotly_white"
    graphics["color_scheme"] = [
        "#458588",
        "#FABD2F",
        "#B8BB26",
        "#CC241D",
        "#B16286",
        "#8EC07C",
        "#FE8019",
    ]
    graphics["format"] = "png"
    graphics["default_width"] = 1600
    graphics["default_height"] = 1200
    graphics["scale"] = 2

    config.add("general", general)
    config.add(nl())
    config.add("ach", ach)
    config.add(nl())

    return config


def save_config(config: dict[str, Any]) -> None:
    """Saves new configuration file.

    Args:
        config (tomlkit.TOMLDocument): Config object ready to save
    """
    with open(
        "airborne_cli/settings.toml", mode="w", encoding="utf-8"
    ) as settings_file:
        settings_file.write(tomlkit.dumps(config))


def show_general() -> Panel:
    """Pretty prints general settings to console

    Returns:
        Panel: Rich panel with general settings
    """
    settings = load_config()

    table = Table(show_header=False, box=None)

    for key, value in settings["general"].items():
        if isinstance(type(value), list):
            table.add_row(key, f"{value}")
        else:
            table.add_row(key, f"{value}")

    return Panel(table, title="General", style="green", width=80)


def show_ach() -> Panel:
    """Pretty prints general settings to console

    Returns:
        Panel: Rich panel with general settings
    """
    settings = load_config()

    table = Table(show_header=False, box=None)

    for key, value in settings["ach"].items():
        table.add_row(key, f"{value}")

    return Panel(table, title="ACH", style="red", width=80)


def show_ashrae() -> Panel:
    """Pretty prints general settings to console

    Returns:
        Panel: Rich panel with general settings
    """
    settings = load_config()

    table = Table(box=None)

    table.add_column("Room Type")
    table.add_column("Rate for people")
    table.add_column("Rate for area")

    for key, value in settings["ashrae"].items():
        table.add_row(key, f"{value['rate_people']}", f"{value['rate_area']}")

    return Panel(table, title="ASHRAE parameters", style="yellow", width=80)


def show_graphics() -> Panel:
    """Pretty prints general settings to console

    Returns:
        Panel: Rich panel with general settings
    """
    settings = load_config()

    table = Table(show_header=False, box=None)

    for key, value in settings["graphics"].items():
        if isinstance(type(value), list):
            table.add_row(key, f"{value}")
        else:
            table.add_row(key, f"{value}")
    return Panel(table, title="Graphics", style="magenta", width=80)
