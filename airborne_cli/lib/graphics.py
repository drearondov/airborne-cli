import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

from ..settings.config import settings



def risk_ach_graph(data: pd.DataFrame, colors:list) -> dict:
    """Makes Risk vs ACH graphs for the data given.

    Args:
        data (pd.DataFrame): Data for graph
        colors (list): List of colors to be used in graph

    Returns:
        dict: List of figures and identifiers
    """
    pio.templates.default = settings["graphics"]["template"]
    pio.kaleido.scope.default_format = settings["graphics"]["format"]
    pio.kaleido.scope.default_width = settings["graphics"]["default_width"]
    pio.kaleido.scope.default_height = settings["graphics"]["default_height"]
    pio.kaleido.scope.default_scale = settings["graphics"]["scale"]

    pabellon_figs = {}
    for pabellon in data["pabellon"].unique():
        pabellon_data = data[data["pabellon"] == pabellon]    
        for ambiente in pabellon_data["ambiente"].unique():
            fig = go.Figure()

            graph_data = pabellon_data[pabellon_data["ambiente"] == ambiente]
            ach_natural = graph_data["ach_natural"].unique()[0]

            for inf in graph_data["infected"].unique():

                fig.add_trace(go.Scatter(
                        x = graph_data["ach"],
                        y = graph_data[f"riesgo_30_{inf}_inf"]*100,
                        mode="lines+markers",
                        name=f"Aforo 30%",
                        marker_color = colors[0],
                        legendgroup=f"{inf}_inf",
                        legendgrouptitle_text=f"{inf}% infectados"
                    )
                )

                fig.add_trace(go.Scatter(
                        x = graph_data["ach"],
                        y = graph_data[f"riesgo_40_{inf}_inf"]*100,
                        mode="lines+markers",
                        name="Aforo 40%",
                        marker_color = colors[1],
                        legendgroup=f"{inf}_inf",
                        legendgrouptitle_text=f"{inf}% infectados"
                    )
                )

                fig.add_trace(go.Scatter(
                        x = graph_data["ach"],
                        y = graph_data[f"riesgo_50_{inf}_inf"]*100,
                        mode="lines+markers",
                        name="Aforo 50%",
                        marker_color = colors[2],
                        legendgroup=f"{inf}_inf",
                        legendgrouptitle_text=f"{inf}% infectados"
                    )
                )

                fig.add_trace(go.Scatter(
                        x = graph_data["ach"],
                        y = graph_data[f"riesgo_70_{inf}_inf"]*100,
                        mode="lines+markers",
                        name="Aforo 70%",
                        marker_color = colors[3],
                        legendgroup=f"{inf}_inf",
                        legendgrouptitle_text=f"{inf}% infectados"
                    )
                )

                fig.add_trace(go.Scatter(
                        x = graph_data["ach"],
                        y = graph_data[f"riesgo_90_{inf}_inf"]*100,
                        mode="lines+markers",
                        name="Aforo 90%",
                        marker_color = colors[4],
                        legendgroup=f"{inf}_inf",
                        legendgrouptitle_text=f"{inf}% infectados"
                    )
                )

                fig.add_trace(go.Scatter(
                        x = graph_data["ach"],
                        y = graph_data[f"riesgo_100_{inf}_inf"]*100,
                        mode="lines+markers",
                        name="Aforo 100%",
                        marker_color = colors[5],
                        legendgroup=f"{inf}_inf",
                        legendgrouptitle_text=f"{inf}% infectados"
                    )
                )

                fig.add_hline(
                    y=3,
                    line_color="#333333",
                    line_dash="dash",
                    line_width=1,
                    annotation_text="Riesgo 3%",
                    annotation_position="top right"
                )

                fig.add_vline(
                    x=ach_natural,
                    line_color="#333333",
                    line_dash="dash",
                    line_width=1,
                    annotation_text="ACH natural de ambiente",
                    annotation_position="top right"
                )

                fig.update_xaxes(title_text="ACH (-)")
                fig.update_yaxes(title_text="Riesgo (%)")

                fig.update_layout(
                    height=600,
                    width=800,
                    title_text=f"{ambiente} - ACH vs. Riesgo")

                pabellon_figs[f"{pabellon}_{ambiente}_{inf}_inf"] = fig    

    return pabellon_figs

def risk_flow_graph(data: pd.DataFrame, colors:list) -> dict:
    """Makes graph of Max risk vs. Flow Rate

    Args:
        data (pd.DataFrame): Data to graph
        colors (list): List of colors used in Hex code format

    Returns:
        dict: Dictionary of figures and identifiers
    """
    pabellon_figs = {}
    for pabellon in data["pabellon"].unique():
        pabellon_data = data[data["pabellon"] == pabellon]    
        for ambiente in pabellon_data["ambiente"].unique():
            fig = go.Figure()

            graph_data = pabellon_data[pabellon_data["ambiente"] == ambiente]


            fig.add_trace(go.Scatter(
                    x = graph_data["flujo"],
                    y = graph_data[f"riesgo_20_um"]*100,
                    mode="lines+markers",
                    name=f"Aerosoles 20um",
                    marker_color = colors[0],

                )
            )

            fig.add_trace(go.Scatter(
                    x = graph_data["flujo"],
                    y = graph_data[f"riesgo_40_um"]*100,
                    mode="lines+markers",
                    name=f"Aerosoles 40um",
                    marker_color = colors[1],

                )
            )

            fig.add_hline(
                y=3,
                line_color="#333333",
                line_dash="dash",
                line_width=1,
                annotation_text="Riesgo 3%",
                annotation_position="top right"
            )

            fig.add_hline(
                y=5,
                line_color="#333333",
                line_dash="dash",
                line_width=1,
                annotation_text="Riesgo 5%",
                annotation_position="top right"
            )

            fig.add_vrect(
                    x0=200,
                    x1=500,
                    fillcolor = "#333333",
                    line_width = 0,
                    opacity = 0.2,
                    annotation_text="200 - 500 m<sup>3</sup>/h",
                    annotation_position="top left"
                )


            fig.update_xaxes(title_text="Flujo (m<sup>3</sup>/h)")
            fig.update_yaxes(title_text="Riesgo (%)")

            fig.update_layout(
                height=800,
                width=1200,
                title_text=f"{ambiente} - Flujo vs. Riesgo",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )

            pabellon_figs[f"{pabellon}_{ambiente}"] = fig 

    return pabellon_figs
