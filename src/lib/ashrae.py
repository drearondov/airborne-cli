import pandas as pd

from math import ceil

def ASHRAE_calculation(data: pd.DataFrame, occupancy_perc:float, ashrae_data:object) -> pd.DataFrame:
    """Función que calcula el flujo necesario para asegurar condiciones de ventilación de los ambientes
        de acuerdo con las recomendaciones de la norma ASHRAE 62.1

    Args:
        data (pd.DataFrame): Dataframe con la data a procesar
        occupancy_perc (float): Porcentaje de ocupación 
        ashrae_data (object): Parametros ashrae para la data

    Returns:
        pd.DataFrame: Nuevo dataframe con los valores ASHRAE calculados
    """
    flujo_gal = data.apply(lambda x: (ceil(x["Aforo_100"]*(occupancy_perc/100))*ashrae_data[x["Tipo"]].rate_people)*3.6, axis=1)
    flujo_ambiente = data.apply(lambda x: (x["Area"]*ashrae_data[x["Tipo"]].rate_area)*3.6, axis=1)

    data[f"Flujo_ASHRAE_{occupancy_perc}"] = flujo_gal + flujo_ambiente

    data[f"ACH_ASHRAE_{occupancy_perc}"] = data.apply(lambda x: x[f"Flujo_ASHRAE_{occupancy_perc}"]/x["Volumen"], axis=1)

    return data