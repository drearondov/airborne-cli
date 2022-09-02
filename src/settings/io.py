import tomlkit


def load_config() -> tomlkit.TOMLDocument:
    """Loads TOML configuration file and returns a dictionary with all the variables.

    Returns:
        TOMLDocument: Dictionary with settings
    """
    with open("../settings.toml", mode="rt", encoding="utf-8") as settings_file:
        config = tomlkit.load(settings_file)

    return config
