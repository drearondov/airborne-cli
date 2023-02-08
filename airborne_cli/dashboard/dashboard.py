import pandas as pd

from dash import Dash, html, dcc

from ..settings.io import load_config
from ..utils.options import MaskType, ViralLoad, AerosolCutoff


def make_dashboard(data:pd.DataFrame) -> Dash:
    """Creates a Dash application with the data to analyse

    Args:
        data (pd.DataFrame): Pandas dataframe with the data to analyse

    Returns:
        Dash: Dash application ready for running
    """
    app = Dash(__name__)

    settings = load_config()

    app.layout = html.Div(children=[
        html.Header(children=[
            html.H1(children="ACH - risk analysis")
        ]),
        html.Main(children=[
            html.Div(children=[
                # Selección de ambiente y pabellón
                html.Div(children=[
                    html.Label("Pabellón"),
                    dcc.Dropdown(data["Pabellon"].unique(), value=data["Pabellon"].unique()[0], id="pabellon-dropdown"),
                    html.Br(),
                    html.Label("Ambiente"),
                    dcc.Dropdown(children=[], value="", id="ambiente-dropdown")
                ]),
                # Panel de opciones
                html.Div(children=[
                    html.H2(children="Options:"),
                    html.Br(),
                    html.Label("Max risk"),
                    dcc.Slider(0, 100, 10, value=settings["ach"]["max_risk"], id="max-risk-slider"),
                    html.Br(),
                    html.Label("Mask type"),
                    dcc.Dropdown(children=[mask_type.value for mask_type in MaskType], value=settings["ach"]["mask_default"], multi=True, id="mask-type-dropdown"),
                    html.Br(),
                    html.Label("Percentage of infected"),
                    dcc.Slider(0, 100, 10, value=settings["ach"]["inf_percent"], id="inf-percent-slider"),
                    html.Br(),
                    html.Label("Viral Load"),
                    dcc.Dropdown(children=[viral_load.value for viral_load in ViralLoad], value=settings["ach"]["viral_load"], multi=True, id="viral-load-dropdown"),
                    html.Br(),
                    html.Label("Aerosol Cutoff"),
                    dcc.Dropdown(children=[aerosol.value for aerosol in AerosolCutoff], value=settings["ach"]["aerosol"],multi=True, id="aerosol-cutoff-dropdown"),
                    html.Br(),
                    html.Label("Occupancy"),
                    dcc.Checklist(children=[occupancy for occupancy in range(0, 110, 10)], id="occupancy-checklist")
                ])
            ], style={"flex": 1}),
            html.Div(id="tabs_graphs", value="risk_time_graph", children=[
                dcc.Tabs(children=[
                    dcc.Tab(label="Risk - Time", value="risk-time-graph"),
                    dcc.Tab(label="Risk - ACH", value="risk-ach-graph"),
                    dcc.Tab(label="CO<sub>2</sub> - Time", value="co2_time_graph")
                ]),
            html.Div(id="content-graph")
            ], style={"flex": 2})
        ], style={"display": "flex", "flex-direction": "row"})
    ])

    #TODO: Callbacks and functionality