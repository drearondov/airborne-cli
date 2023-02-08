import tomlkit
from rich.panel import Panel
from rich.table import Table


def load_config() -> tomlkit.TOMLDocument:
    """Loads TOML configuration file and returns a dictionary with all the variables.

    Returns:
        TOMLDocument: Dictionary with settings
    """
    with open("airborne_cli/settings.toml", mode="rt", encoding="utf-8") as settings_file:
        config = tomlkit.load(settings_file)

    return config


def save_config(config: tomlkit.TOMLDocument) -> None:
    """Saves new configuration file.

    Args:
        config (tomlkit.TOMLDocument): Config object ready to save
    """
    with open("airborne_cli/settings.toml", mode="wt", encoding="utf-8") as settings_file:
        settings_file.write(tomlkit.dumps(config))


def show_general() -> Panel:
    """Pretty prints general settings to console

    Returns:
        Panel: Rich panel with general settings
    """
    settings = load_config()

    table = Table(show_header=False, box=None)

    for key, value in settings["general"].items():
        if type(value) != tomlkit.items.Array:
            table.add_row(key, f"{value}")
        else:
            table.add_row(key, f"{list(value)}")

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
        if type(value) != tomlkit.items.Array:
            table.add_row(key, f"{value}")
        else:
            table.add_row(key, f"{list(value)}")
    return Panel(table, title="Graphics", style="magenta", width=80)
