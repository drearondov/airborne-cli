import pytest

from enum import Enum

from airborne_cli.utils.options import (
    SaveFormat,
    GraphicFormat,
    GraphicTemplate,
    MaskType,
    ViralLoad,
    AerosolCutoff,
)


class TestSaveFormat:
    @pytest.mark.parametrize("save_format", ["csv", "excel", "json"])
    def test_correct_format(self, save_format):
        assert isinstance(SaveFormat(save_format), Enum)

    def test_wrong_format(self, faker):
        with pytest.raises(ValueError):
            SaveFormat(faker.file_extension(category="image"))


class TestGraphicFormat:
    @pytest.mark.parametrize(
        "graphic_format", ["png", "jpeg", "webp", "svg", "pdf", "eps"]
    )
    def test_correct_format(self, graphic_format):
        assert isinstance(GraphicFormat(graphic_format), Enum)

    def test_wrong_format(self, faker):
        with pytest.raises(ValueError):
            GraphicFormat(faker.file_extension(category="text"))


class TestGraphicTemplate:
    @pytest.mark.parametrize(
        "graphic_template",
        [
            "ggplot2",
            "seaborn",
            "simple_white",
            "plotly",
            "plotly_white",
            "plotly_dark",
            "presentation",
            "xgridoff",
            "ygridoff",
            "gridon",
            "none",
        ],
    )
    def test_correct_template(self, graphic_template):
        assert isinstance(GraphicTemplate(graphic_template), Enum)

    def test_wrong_template(self, faker):
        with pytest.raises(ValueError):
            GraphicTemplate(faker.word())


class TestMaskType:
    @pytest.mark.parametrize(
        "mask_type",
        ["no_mask", "KN95", "surgical", "cloth_3ply", "cloth_1ply", "on_file"],
    )
    def test_correct_type(self, mask_type):
        assert isinstance(MaskType(mask_type), Enum)

    def test_wrong_type(self, faker):
        with pytest.raises(ValueError):
            MaskType(faker.word())


class TestViralLoad:
    @pytest.mark.parametrize("viral_load", ["8", "9", "10"])
    def test_correct_load(self, viral_load):
        assert isinstance(ViralLoad(viral_load), Enum)

    def test_wrong_load(self, faker):
        with pytest.raises(ValueError):
            ViralLoad(faker.word())


class TestAerosolCutoff:
    @pytest.mark.parametrize("aerosol_cutoff", ["5", "10", "20", "40", "40", "100"])
    def test_correct_cutoff(self, aerosol_cutoff):
        assert isinstance(AerosolCutoff(aerosol_cutoff), Enum)

    def test_wrong_cutoff(self, faker):
        with pytest.raises(ValueError):
            AerosolCutoff(faker.word())
