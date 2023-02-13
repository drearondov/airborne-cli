"""Module that contains the options used along the program

Option classes for parameters which require input to chose between different options.
"""
from enum import Enum


class SaveFormat(str, Enum):
    csv = "csv"
    excel = "excel"
    json = "json"


class GraphicFormat(str, Enum):
    png = "png"
    jpeg = "jpeg"
    webp = "webp"
    svg = "svg"
    pdf = "pdf"
    eps = "eps"


class GraphicTemplate(str, Enum):
    ggplot2 = ("ggplot2",)
    seaborn = ("seaborn",)
    simple_white = ("simple_white",)
    plotly = ("plotly",)
    plotly_white = ("plotly_white",)
    plotly_dark = ("plotly_dark",)
    presentation = ("presentation",)
    xgridoff = ("xgridoff",)
    ygridoff = ("ygridoff",)
    gridon = ("gridon",)
    none = "none"


class MaskType(Enum):
    i0 = "no_mask"
    i1 = "KN95"
    i2 = "surgical"
    i3 = "cloth_3ply"
    i4 = "cloth_1ply"
    i5 = "on_file"


class ViralLoad(Enum):
    i8 = "8"
    i9 = "9"
    i10 = "10"


class AerosolCutoff(Enum):
    i0 = "5"
    i1 = "10"
    i2 = "20"
    i3 = "40"
    i4 = "100"
