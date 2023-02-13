from math import ceil

import numpy as np
import pandas as pd

from airborne_cli.lib.ach import room_calculation


def ach_risk_calculation(data: pd.DataFrame, inf_percent: list) -> pd.DataFrame:
    """Calculates the variation in risk at different ACH values for different rates of infection.

    Args:
        data (pd.DataFrame): Data to process
        inf_percent (List): List of percentages of infections to evaluate.

    Returns:
        pd.DataFrame: Data frame with the risk evaluation for different occupancies at different rates of infections
    """
    ach_list = np.geomspace(0.5, 50, num=25).tolist()

    results = {
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

    for ambiente in data.itertuples(index=False, name="Ambiente"):

        for ach in ach_list:

            results["ambiente"].append(ambiente.Ambiente)
            results["pabellon"].append(ambiente.Pabellon)
            results["ach"].append(ach)
            results["Aforo_100"].append(ambiente.Aforo_100)
            results["ach_natural"].append(ambiente.ACH_natural)

            for infected in inf_percent:

                results["infected"].append(inf_percent)

                (_, R, _, _, _, _, _) = room_calculation(
                    Ar=ambiente.Area,
                    Hr=ambiente.Altura,
                    n_people=ceil(ambiente.Aforo_100 * 0.3),
                    activity_type=ambiente.Actividad,
                    activity_type_sick=ambiente.Actividad,
                    permanence=ambiente.Permanencia,
                    ACH_custom=ach,
                    inf_percent=infected,
                )
                results[f"aforo_30_{infected}_inf"].append(
                    ceil(ambiente.Aforo_100 * 0.3)
                )
                results[f"riesgo_30_{infected}_inf"].append(R[-1])

                (_, R, _, _, _, _, _) = room_calculation(
                    Ar=ambiente.Area,
                    Hr=ambiente.Altura,
                    n_people=ceil(ambiente.Aforo_100 * 0.5),
                    activity_type=ambiente.Actividad,
                    activity_type_sick=ambiente.Actividad,
                    permanence=ambiente.Permanencia,
                    ACH_custom=ach,
                    inf_percent=infected,
                )
                results[f"aforo_40_{infected}_inf"].append(
                    ceil(ambiente.Aforo_100 * 0.4)
                )
                results[f"riesgo_40_{infected}_inf"].append(R[-1])

                (_, R, _, _, _, _, _) = room_calculation(
                    Ar=ambiente.Area,
                    Hr=ambiente.Altura,
                    n_people=ceil(ambiente.Aforo_100 * 0.5),
                    activity_type=ambiente.Actividad,
                    activity_type_sick=ambiente.Actividad,
                    permanence=ambiente.Permanencia,
                    ACH_custom=ach,
                    inf_percent=infected,
                )
                results[f"aforo_50_{infected}_inf"].append(
                    ceil(ambiente.Aforo_100 * 0.5)
                )
                results[f"riesgo_50_{infected}_inf"].append(R[-1])

                (_, R, _, _, _, _, _) = room_calculation(
                    Ar=ambiente.Area,
                    Hr=ambiente.Altura,
                    n_people=ceil(ambiente.Aforo_100 * 0.7),
                    activity_type=ambiente.Actividad,
                    activity_type_sick=ambiente.Actividad,
                    permanence=ambiente.Permanencia,
                    ACH_custom=ach,
                    inf_percent=infected,
                )
                results[f"aforo_70_{infected}_inf"].append(
                    ceil(ambiente.Aforo_100 * 0.7)
                )
                results[f"riesgo_70_{infected}_inf"].append(R[-1])

                (_, R, _, _, _, _, _) = room_calculation(
                    Ar=ambiente.Area,
                    Hr=ambiente.Altura,
                    n_people=ceil(ambiente.Aforo_100 * 0.9),
                    activity_type=ambiente.Actividad,
                    activity_type_sick=ambiente.Actividad,
                    permanence=ambiente.Permanencia,
                    ACH_custom=ach,
                    inf_percent=infected,
                )
                results[f"aforo_90_{infected}_inf"].append(
                    ceil(ambiente.Aforo_100 * 0.9)
                )
                results[f"riesgo_90_{infected}_inf"].append(R[-1])

                (_, R, _, _, _, _, _) = room_calculation(
                    Ar=ambiente.Area,
                    Hr=ambiente.Altura,
                    n_people=ceil(ambiente.Aforo_100),
                    activity_type=ambiente.Actividad,
                    activity_type_sick=ambiente.Actividad,
                    permanence=ambiente.Permanencia,
                    ACH_custom=ach,
                    inf_percent=infected,
                )
                results[f"aforo_100_{infected}_inf"].append(ceil(ambiente.Aforo_100))
                results[f"riesgo_100_{infected}_inf"].append(R[-1])

    results_df = pd.DataFrame.from_dict(results)

    return results_df


def aerosol_risk_calculation(data: pd.DataFrame, aerosol_cutoff: list) -> pd.DataFrame:
    """Maximum risk for different flow rates at different aerosol cuttoff.

    Args:
        data (pd.DataFrame): Data for processing

    Returns:
        pd.DataFrame: Data frame with maximum values of risk for different flow rates for 20um and 40um cuttoff
    """
    ach_list = np.geomspace(0.5, 50, num=25).tolist()

    results = {
        "ambiente": [],
        "volumen": [],
        "pabellon": [],
        "ach": [],
        "riesgo_20_um": [],
        "riesgo_40_um": [],
    }

    for ambiente in data.itertuples(index=False, name="Ambiente"):

        for ach in ach_list:

            results["ambiente"].append(ambiente.Ambiente)
            results["pabellon"].append(ambiente.Pabellon)
            results["volumen"].append(ambiente.Volumen)
            results["ach"].append(ach)

            for cutoff in aerosol_cutoff:

                (_, R, _, _, _, _, _) = room_calculation(
                    Ar=ambiente.Area,
                    Hr=ambiente.Altura,
                    n_people=ambiente.Aforo_100,
                    activity_type=ambiente.Actividad,
                    activity_type_sick=ambiente.Actividad,
                    permanence=ambiente.Permanencia,
                    ACH_custom=ach,
                    inf_percent=10,
                    cutoff_type=cutoff,
                )
                results[f"riesgo_{cutoff}_um"].append(R[-1])

    results_df = pd.DataFrame.from_dict(results)

    results_df["flujo"] = results_df["ach"] * results_df["volumen"]

    return results_df
