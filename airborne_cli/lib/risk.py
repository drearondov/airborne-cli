from itertools import product
from math import ceil

import numpy as np
import pandas as pd

from airborne_cli.lib.ach import room_calculation


def ach_risk_inf_percent_calculation(
    data: pd.DataFrame, inf_percent: list[float]
) -> pd.DataFrame:
    """Calculates the variation in risk at different ACH values for different occupancy percentages. Returns a dataframe rates of infection at different ach.

    Args:
        data (pd.DataFrame): Data to process
        inf_percent (List): List of percentages of infections to evaluate.

    Returns:
        pd.DataFrame: Data frame with the risk evaluation for different occupancies at different rates of infections
    """
    ach_list = np.geomspace(0.5, 50, num=25).tolist()
    occupancy_list = [0.3, 0.4, 0.5, 0.7, 0.9, 1]

    results: dict[str, list[str | int | float | list[float]]] = {
        "ambiente": [],
        "pabellon": [],
        "Aforo_100": [],
        "ach": [],
        "ach_natural": [],
        "infected": [],
    }

    for infected in inf_percent:
        results[f"aforo_30_{infected}_inf"] = []
        results[f"riesgo_30_{infected}_inf"] = []
        results[f"aforo_40_{infected}_inf"] = []
        results[f"riesgo_40_{infected}_inf"] = []
        results[f"aforo_50_{infected}_inf"] = []
        results[f"riesgo_50_{infected}_inf"] = []
        results[f"aforo_70_{infected}_inf"] = []
        results[f"riesgo_70_{infected}_inf"] = []
        results[f"aforo_90_{infected}_inf"] = []
        results[f"riesgo_90_{infected}_inf"] = []
        results[f"aforo_100_{infected}_inf"] = []
        results[f"riesgo_100_{infected}_inf"] = []

    for ambiente, ach in product(
        data.itertuples(index=False, name="Ambiente"), ach_list
    ):
        results["ambiente"].append(ambiente.Ambiente)
        results["pabellon"].append(ambiente.Pabellon)
        results["ach"].append(ach)
        results["Aforo_100"].append(ambiente.Aforo_100)
        results["ach_natural"].append(ambiente.ACH_natural)

        for infected in inf_percent:
            results["infected"].append(inf_percent)

            for occupancy in occupancy_list:
                (_, R, _, _, _, _, _) = room_calculation(
                    Ar=ambiente.Area,
                    Hr=ambiente.Altura,
                    n_people=ceil(ambiente.Aforo_100 * occupancy),
                    activity_type=ambiente.Actividad,
                    activity_type_sick=ambiente.Actividad,
                    permanence=ambiente.Permanencia,
                    ACH_custom=ach,
                    inf_percent=infected,
                )
                results[f"aforo_{occupancy * 100}_{infected}_inf"].append(
                    ceil(ambiente.Aforo_100 * occupancy)
                )
                results[f"riesgo_{occupancy * 100}_{infected}_inf"].append(R[-1])

    results_df = pd.DataFrame.from_dict(results)

    return results_df


def ach_risk_aerosol_calculation(
    data: pd.DataFrame, aerosol_cutoff: list[int]
) -> pd.DataFrame:
    """ "Calculates the variation in risk at different ACH values at maximum occupancy for different aerosol cuttof values. Returns a dataframe rates of infection at different ach.

    Args:
        data (pd.DataFrame): Data for processing
        aerosol_cutoff (list[int]): List of aerosol cuttoff values fo analysis

    Returns:
        pd.DataFrame: Data frame with maximum values of risk for different ach/flow rates for different cutoff values
    """
    ach_list = np.geomspace(0.5, 50, num=25).tolist()
    occupancy_list = [0.3, 0.4, 0.5, 0.7, 0.9, 1]

    results: dict[str, list[str | int | float | list[float]]] = {
        "ambiente": [],
        "volumen": [],
        "pabellon": [],
        "ach": [],
        "Aforo_100": [],
        "aerosol": [],
    }

    for aerosol in aerosol_cutoff:
        results[f"aforo_30_{aerosol}_um"] = []
        results[f"riesgo_30_{aerosol}_um"] = []
        results[f"aforo_40_{aerosol}_um"] = []
        results[f"riesgo_40_{aerosol}_um"] = []
        results[f"aforo_50_{aerosol}_um"] = []
        results[f"riesgo_50_{aerosol}_um"] = []
        results[f"aforo_70_{aerosol}_um"] = []
        results[f"riesgo_70_{aerosol}_um"] = []
        results[f"aforo_90_{aerosol}_um"] = []
        results[f"riesgo_90_{aerosol}_um"] = []
        results[f"aforo_100_{aerosol}_um"] = []
        results[f"riesgo_100_{aerosol}_um"] = []

    for ambiente, ach in product(
        data.itertuples(index=False, name="Ambiente"), ach_list
    ):
        results["ambiente"].append(ambiente.Ambiente)
        results["pabellon"].append(ambiente.Pabellon)
        results["volumen"].append(ambiente.Volumen)
        results["Aforo_100"].append(ambiente.Aforo_100)
        results["ach"].append(ach)

        for cutoff in aerosol_cutoff:
            results["aerosol"].append(cutoff)

            for occupancy in occupancy_list:
                (_, R, _, _, _, _, _) = room_calculation(
                    Ar=ambiente.Area,
                    Hr=ambiente.Altura,
                    n_people=ambiente.Aforo_100 * occupancy,
                    activity_type=ambiente.Actividad,
                    activity_type_sick=ambiente.Actividad,
                    permanence=ambiente.Permanencia,
                    ACH_custom=ach,
                    inf_percent=10,
                    cutoff_type=cutoff,
                )
                results[f"aforo_{occupancy * 100}_{cutoff}_um"].append(
                    ceil(ambiente.Aforo_100 * occupancy)
                )
                results[f"riesgo_{occupancy * 100}_{cutoff}_um"].append(R[-1])

    results_df = pd.DataFrame.from_dict(results)

    results_df["flujo"] = results_df["ach"] * results_df["volumen"]

    return results_df


# def ach_risk_co2_calculation():  # TODO: New CO2 risk feature
#     """ """
