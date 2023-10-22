from airborne_cli.settings.io import generate_config


def test_generate_config(test_config_data):
    default_config = generate_config()

    assert test_config_data == default_config
