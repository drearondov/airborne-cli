import pytest
import tomlkit

from tomlkit import document, nl, table


@pytest.fixture(scope="module")
def test_config_data() -> tomlkit.TOMLDocument:
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
