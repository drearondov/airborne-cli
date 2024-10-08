import pandas as pd
import plotly.graph_objects as go  # type:ignore
import plotly.io as pio  # type:ignore

from ..settings.config import settings


def graphics_config() -> None:
    """Sets config options for graphics"""
    pio.templates.default = settings["graphics"]["template"]
    pio.kaleido.scope.default_format = settings["graphics"]["format"]
    pio.kaleido.scope.default_width = settings["graphics"]["default_width"]
    pio.kaleido.scope.default_height = settings["graphics"]["default_height"]
    pio.kaleido.scope.default_scale = settings["graphics"]["scale"]


def risk_ach_inf_graph(data: pd.DataFrame, colors: list[str]) -> dict[str, go.Figure]:
    """Makes Risk vs ACH graphs for the data given. Considers different percentages of occupancy

    Args:
        data (pd.DataFrame): Data for graph
        colors (list): List of colors to be used in graph

    Returns:
        dict: List of figures and identifiers
    """
    graphics_config()

    pabellon_figs = {}
    for pabellon in data["pabellon"].unique():
        pabellon_data = data[data["pabellon"] == pabellon]
        for ambiente in pabellon_data["ambiente"].unique():
            fig = go.Figure()

            graph_data = pabellon_data[pabellon_data["ambiente"] == ambiente]
            ach_natural = graph_data["ach_natural"].unique()[0]

            for inf in graph_data["infected"].unique():
                fig.add_trace(
                    go.Scatter(
                        x=graph_data["ach"],
                        y=graph_data[f"riesgo_30_{inf}_inf"] * 100,
                        mode="lines+markers",
                        name="Aforo 30%",
                        marker_color=colors[0],
                        legendgroup=f"{inf}_inf",
                        legendgrouptitle_text=f"{inf}% infectados",
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=graph_data["ach"],
                        y=graph_data[f"riesgo_40_{inf}_inf"] * 100,
                        mode="lines+markers",
                        name="Aforo 40%",
                        marker_color=colors[1],
                        legendgroup=f"{inf}_inf",
                        legendgrouptitle_text=f"{inf}% infectados",
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=graph_data["ach"],
                        y=graph_data[f"riesgo_50_{inf}_inf"] * 100,
                        mode="lines+markers",
                        name="Aforo 50%",
                        marker_color=colors[2],
                        legendgroup=f"{inf}_inf",
                        legendgrouptitle_text=f"{inf}% infectados",
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=graph_data["ach"],
                        y=graph_data[f"riesgo_70_{inf}_inf"] * 100,
                        mode="lines+markers",
                        name="Aforo 70%",
                        marker_color=colors[3],
                        legendgroup=f"{inf}_inf",
                        legendgrouptitle_text=f"{inf}% infectados",
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=graph_data["ach"],
                        y=graph_data[f"riesgo_90_{inf}_inf"] * 100,
                        mode="lines+markers",
                        name="Aforo 90%",
                        marker_color=colors[4],
                        legendgroup=f"{inf}_inf",
                        legendgrouptitle_text=f"{inf}% infectados",
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=graph_data["ach"],
                        y=graph_data[f"riesgo_100_{inf}_inf"] * 100,
                        mode="lines+markers",
                        name="Aforo 100%",
                        marker_color=colors[5],
                        legendgroup=f"{inf}_inf",
                        legendgrouptitle_text=f"{inf}% infectados",
                    )
                )

                fig.add_hline(
                    y=3,
                    line_color="#333333",
                    line_dash="dash",
                    line_width=1,
                    annotation_text="Riesgo 3%",
                    annotation_position="top right",
                )

                fig.add_vline(
                    x=ach_natural,
                    line_color="#333333",
                    line_dash="dash",
                    line_width=1,
                    annotation_text="ACH natural de ambiente",
                    annotation_position="top right",
                )

                fig.update_xaxes(title_text="ACH (-)")
                fig.update_yaxes(title_text="Riesgo (%)")

                fig.update_layout(
                    height=600, width=800, title_text=f"{ambiente} - ACH vs. Riesgo"
                )

                pabellon_figs[f"{pabellon}_{ambiente}_{inf}_inf"] = fig

    return pabellon_figs


def risk_ach_aerosol_graph(
    data: pd.DataFrame, colors: list[str]
) -> dict[str, go.Figure]:
    """Makes graph of Max risk vs. Flow Rate

    Args:
        data (pd.DataFrame): Data to graph
        colors (list): List of colors used in Hex code format

    Returns:
        dict: Dictionary of figures and identifiers
    """
    graphics_config()

    pabellon_figs = {}
    for pabellon in data["pabellon"].unique():
        pabellon_data = data[data["pabellon"] == pabellon]
        for ambiente in pabellon_data["ambiente"].unique():
            fig = go.Figure()

            graph_data = pabellon_data[pabellon_data["ambiente"] == ambiente]

            for aerosol in data["aerosol"].unique():
                fig.add_trace(
                    go.Scatter(
                        x=graph_data["flujo"],
                        y=graph_data[f"riesgo_30_{aerosol}_um"],
                        mode="lines+markers",
                        name="Aforo 30%",
                        marker_color=colors[0],
                        legendgroup=f"{aerosol}_um",
                        legendgrouptitle=f"Aerosol cutoff {aerosol}um",
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=graph_data["flujo"],
                        y=graph_data[f"riesgo_40_{aerosol}_um"],
                        mode="lines+markers",
                        name="Aforo 40%",
                        marker_color=colors[1],
                        legendgroup=f"{aerosol}_um",
                        legendgrouptitle=f"Aerosol cutoff {aerosol}um",
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=graph_data["flujo"],
                        y=graph_data[f"riesgo_50_{aerosol}_um"],
                        mode="lines+markers",
                        name="Aforo 50%",
                        marker_color=colors[2],
                        legendgroup=f"{aerosol}_um",
                        legendgrouptitle=f"Aerosol cutoff {aerosol}um",
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=graph_data["flujo"],
                        y=graph_data[f"riesgo_70_{aerosol}_um"],
                        mode="lines+markers",
                        name="Aforo 70%",
                        marker_color=colors[3],
                        legendgroup=f"{aerosol}_um",
                        legendgrouptitle=f"Aerosol cutoff {aerosol}um",
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=graph_data["flujo"],
                        y=graph_data[f"riesgo_90_{aerosol}_um"],
                        mode="lines+markers",
                        name="Aforo 90%",
                        marker_color=colors[4],
                        legendgroup=f"{aerosol}_um",
                        legendgrouptitle=f"Aerosol cutoff {aerosol}um",
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=graph_data["flujo"],
                        y=graph_data[f"riesgo_100_{aerosol}_um"],
                        mode="lines+markers",
                        name="Aforo 100%",
                        marker_color=colors[5],
                        legendgroup=f"{aerosol}_um",
                        legendgrouptitle=f"Aerosol cutoff {aerosol}um",
                    )
                )

                fig.add_hline(
                    y=3,
                    line_color="#333333",
                    line_dash="dash",
                    line_width=1,
                    annotation_text="Riesgo 3%",
                    annotation_position="top right",
                )

                fig.add_hline(
                    y=5,
                    line_color="#333333",
                    line_dash="dash",
                    line_width=1,
                    annotation_text="Riesgo 5%",
                    annotation_position="top right",
                )

                fig.add_vrect(
                    x0=200,
                    x1=500,
                    fillcolor="#333333",
                    line_width=0,
                    opacity=0.2,
                    annotation_text="200 - 500 m<sup>3</sup>/h",
                    annotation_position="top left",
                )

                fig.update_xaxes(title_text="Flujo (m<sup>3</sup>/h)")
                fig.update_yaxes(title_text="Riesgo (%)")

                fig.update_layout(
                    height=800,
                    width=1200,
                    title_text=f"{ambiente} - Flujo vs. Riesgo",
                    legend=dict(
                        orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
                    ),
                )

                pabellon_figs[f"{pabellon}_{ambiente}"] = fig

    return pabellon_figs
