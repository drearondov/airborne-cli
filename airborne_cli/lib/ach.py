from math import ceil
from math import exp

import numpy as np


def infected_people(people: int, percent: float, infmin: int, toggle_inf: bool) -> int:
    """Returns the number of infected people for a certain population.

    Args:
        people (int): Number of people
        percent (int): Percentage of infected people.
        infmin (int): Minimum number of infected people
        toggle_inf (bool): Whether the toggle for infected percentage is active or not.

    Returns:
        infected (int): Number of infected people
    """
    percent_people = ceil(people * (percent / 100))
    infected = percent_people if toggle_inf else infmin

    return infected


def gaussian_distribution(n_people: int = 10, permanence: float = 120, t: float = 0):
    b = permanence / 2
    c = permanence / 6
    return n_people * exp(-((t - b) ** 2) / ((2 * c) ** 2))


# Default values
def room_calculation(
    Ar: float = 100,
    Hr: float = 3,
    s_ACH_type=6,
    inf_percent: float = 10,
    inf_min=1,
    n_people=10,
    Vli=10,
    mask_type=1,
    activity_type=0,
    mask_type_sick=1,
    activity_type_sick=0,
    cutoff_type=3,
    verticalv_type=0,
    occupancy_type=0,
    permanence=120,
    ACH_custom: float = 20,
    s_filter_type=0,
    outside_air=100,
    inf_checked=True,
) -> tuple:
    """Returns a tuple containing data of the risk of infection.

    Args:
        Ar (int, optional): Area of the room. Defaults to 100.
        Hr (int, optional): Height of the room. Defaults to 3.
        s_ACH_type (int, optional): Selection of type of ACH. Defaults to 6 which means custom.
        inf_percent (int, optional): Percentage of infected people. Defaults to 20.
        inf_min (int, optional): Minimum of infected people. Defaults to 1.
        n_people (int, optional): Number of people in the room. Defaults to 10.
        Vli (int, optional): Viral load considered. Defaults to 10.
        mask_type (int, optional): Type of mask to select from list. Defaults to 1 which corresponds to KN95.
        activity_type (int, optional): [description]. Defaults to 0.
        mask_type_sick (int, optional): [description]. Defaults to 1 which corresponds to KN95.
        activity_type_sick (int, optional): Activity type to select on list. Defaults to 0 which corresponds to sedentary activity.
        cutoff_type (int, optional): [description]. Defaults to 3.
        verticalv_type (int, optional): [description]. Defaults to 0.
        occupancy_type (int, optional): [description]. Defaults to 0.
        permanence (int, optional): Time of permanence in the room in minutes. Defaults to 60.
        ACH_custom (int, optional): Custom value of ACH. Defaults to 1.
        s_filter_type (int, optional): [description]. Defaults to 0.
        outside_air (int, optional): [description]. Defaults to 100.
        inf_checked (bool, optional): Whether the infected percentage toggle is active. Defaults to True.

    Returns:
        Tuple: [description]
    """

    # People over time
    def people_inst(permanence, t) -> dict:
        people = (
            n_people
            if occupancy_type == 0
            else gaussian_distribution(n_people, permanence, t)
        )
        infected = infected_people(ceil(people), inf_percent, inf_min, inf_checked)

        return {"people": people, "infected": infected}

    #   Filter in the ventilation system based on the modes set at the interface
    #   These values of filter efficiency need changing according to
    #   https:#www.venfilter.com/normativa/comparative-guide-norms-classification-air-filters
    #   Types are: (i) none - 0% (ii) HEPA () -%
    #              (iii) ISO ePM1 -% (iv) ISO ePM2.5 -% (v) ISO ePM10 -% (vi) ISO coarse -%

    #   -------------------------------
    #   Fraction of suspended virus (PFU) in each class in %
    #   -------------------------------
    #   Rows: cut-off diameter
    #   Columns: [0.3-1um],[1-2.5um],[2.5-5um],[5-10um],[10-20um],[20-40um],[40-100um]
    #   -------------------------------
    #   Vertical velocity = 0 m/s
    #   0.1384    5.8893   93.9723       NaN       NaN       NaN       NaN
    #   0.0086    0.3673    5.8605   93.7636       NaN       NaN       NaN
    #   0.0007    0.0293    0.4682    7.4907   92.0111       NaN       NaN
    #   0.0001    0.0022    0.0358    0.5730    9.1790   90.2099       NaN
    #   0.0000    0.0004    0.0059    0.0947    1.5175   23.9912   74.3903
    #   -------------------------------
    #   Vertical velocity = 0.1 m/s
    #   0.1384    5.8893   93.9723       NaN       NaN       NaN       NaN
    #   0.0086    0.3673    5.8605   93.7636       NaN       NaN       NaN
    #   0.0005    0.0229    0.3658    5.8529   93.7578       NaN       NaN
    #   0.0000    0.0014    0.0227    0.3640    5.8303   93.7815       NaN
    #   0.0000    0.0002    0.0037    0.0587    0.9411   15.1371   83.8592

    #   Cuttoff first then velocity

    PM1_base = [0.1384, 0.0086, 0.0007, 0.0001, 0.0, 0.1384, 0.0086, 0.005, 0.0, 0.0]
    PM2d5_base = [
        5.8893,
        0.3673,
        0.0293,
        0.0022,
        0.0004,
        5.8893,
        0.3673,
        0.0229,
        0.0014,
        0.0002,
    ]
    PM5_base = [
        93.9723,
        5.8605,
        0.4682,
        0.0358,
        0.0059,
        93.9723,
        5.8605,
        0.3658,
        0.0227,
        0.0037,
    ]
    PM10_base = [
        0.0,
        93.7636,
        7.4907,
        0.573,
        0.0947,
        0.0,
        93.7636,
        5.8529,
        0.364,
        0.0587,
    ]
    PM20_base = [0.0, 0.0, 92.0111, 9.179, 1.5175, 0.0, 0.0, 93.7578, 5.8303, 0.9411]
    PM40_base = [0.0, 0.0, 0.0, 90.2099, 23.9912, 0.0, 0.0, 0.0, 93.7815, 15.1371]
    PM100_base = [0.0, 0.0, 0.0, 0.0, 74.3903, 0.0, 0.0, 0.0, 0.0, 83.8592]

    # we do not PM5, PM20 and PM40 since they are already accounted for in PM10, PM100 and PM100, respectively.
    PM1 = PM1_base[cutoff_type + 5 * verticalv_type] / 100
    PM2d5 = PM1 + PM2d5_base[cutoff_type + 5 * verticalv_type] / 100
    PM5 = PM2d5 + PM5_base[cutoff_type + 5 * verticalv_type] / 100
    PM10 = PM5 + PM10_base[cutoff_type + 5 * verticalv_type] / 100
    PM20 = PM10 + PM20_base[cutoff_type + 5 * verticalv_type] / 100
    PM40 = PM20 + PM40_base[cutoff_type + 5 * verticalv_type] / 100
    PM100 = PM40 + PM100_base[cutoff_type + 5 * verticalv_type] / 100

    # -------------------------------
    # none
    # HEPA 99.5% efficient in PM1 class and 100% everywhere else
    # ePM1 (90%): 90% efficient in PM1 class and 100% everywhere else
    # ePM2.5 (90%): 90% efficient in PM2.5 class and 100% everywhere else
    # ePM10 (90%): 90% efficient in PM10 class and 100% everywhere else
    # ISO coarse: 40% efficient in PM10 class and 100% everywhere else
    # none           HEPA ePM1  ePM2.5  ePM10  coarse

    sFilterPM1_base = [0, 99.5, 90.0, 90.0, 90.0, 40.0]
    sFilterPM2d5_base = [0, 100.0, 100.0, 90.0, 90.0, 40.0]
    sFilterPM10_base = [0, 100.0, 100.0, 100.0, 90.0, 40.0]
    sFilterRest_base = [0, 100.0, 100.0, 100.0, 100.0, 100.0]

    # The efficiency is like a weighted average
    filterEff = (
        (sFilterPM1_base[s_filter_type] / 100.0) * PM1
        + (sFilterPM2d5_base[s_filter_type] / 100.0) * (PM2d5 - PM1)
        + (sFilterPM10_base[s_filter_type] / 100.0) * (PM10 - PM2d5)
        + (sFilterRest_base[s_filter_type] / 100.0) * (PM100 - PM10)
    )
    # The above filter applies only to recirculated air. Outside air varies between 0--100% (variable is outsideAir)

    # Sets ACH based on the modes set at the interface
    sACH = [0.3, 1, 3, 5, 10, 20, 999]
    ACH = ACH_custom if s_ACH_type == 6 else sACH[s_ACH_type]

    # Decay rates
    # First five values are for zero vertical velocity and last five values are for 0.1 m/s upward vertical velocity
    # The indices are based on the aerosol cut-off diameter
    kappa_base = [
        0.39,
        0.39,
        0.39,
        0.39,
        0.39,
        0,
        0,
        0,
        0,
        0,
    ]  # ... gravitational settling rate , 1/h
    kappa = kappa_base[
        cutoff_type + 5 * verticalv_type
    ]  # ... set gravitational settling rate, 1/h
    delta = 0.636  # ... viral decay rate, 1/h

    # Define background CO2 (hope this does not change a lot...)
    co2_background = 415  # ... CO2 outdoors, ppm

    # Base value for CO2 emission (based on https:#doi.org/10.1111/ina.12383)
    # H_forCO2 = 1.8; # height of individual, m
    # W_forCO2 = 80; # weight of individual, kg
    # AD_forCO2 = 0.202*Math.pow(H_forCO2,0.725)*Math.pow(W_forCO2,0.425); # DuBois surface area, m^2
    AD_forCO2 = 1.8  # averaged size adult, DuBois surface area, m^2
    RQ_forCO2 = 0.85  # respiratory quotient (dimensionless)
    co2_exhRate_without_met = (0.00276 * AD_forCO2 * RQ_forCO2) / (
        0.23 * RQ_forCO2 + 0.77
    )  # ltr/s/met
    met_ref = 1.15  # reference metabolic rate, met
    co2_exhRate_ref = (
        co2_exhRate_without_met * met_ref
    )  # ... indicative CO2 emission rate, ltr/s

    # Metabolic rate applied to to co2_exhRate_ref (based on https:#doi.org/10.1111/ina.12383).
    # (i) sitting/breathing, (ii) standing/light exercise, (iii) heavy exercise
    # in the paper these are taken for:
    # (i) average from range in sitting quietly 1.15 met (see met_ref above)
    # (ii) standing quietly,  light exercise  1.3 met
    # (iii) calisthenics, moderate effort 3.8 met
    metabolic_rate_forCO2 = [
        met_ref,
        1.3,
        3.8,
    ]  # metabolic rate based on activity, met

    # Base value for inhalation rate
    inhRate_pure = 0.521  # ... inhalation rate, ltr/s,

    # Activity multiplier applied to inhRate_pure
    # (i) sitting breathing, (ii) standing speaking, (iii) speaking loudly, (iv) heavy activity
    # from Buonanno et al 2020 (https:#doi.org/10.1016/j.envint.2020.106112)
    # IR = 0.54 m3/h : sedentary activity
    # IR = 1.38 m3/h : <light exercise, unmodulated vocalization> or <light exercise, voiced counting>
    # IR = 3.3 m3/h : <heavy exercise, oral breathing>
    # in Activity_type_inh we I take ratios of IR but we keep the inhRate_pure the same as a reference
    Activity_type_inh = [
        1,
        2.5556,
        6.1111,
    ]  # multiplier for inhalation rate based on activity.

    # Base value for exhalation rate
    # exhRate_pure = (
    # 0.211  # ... exhlation rate for speaking from (Gupta et al., 2010), ltr/s
    # )

    # Activity multiplier applied to Ngen based on similar analysis with inhalation
    Activity_type_Ngen = [
        1,
        2.5556,
        6.1111,
    ]  # multiplier for exhalation rate based on activity.

    # Multiplier based on mask efficiency
    # No mask, N95, surgical and 3-ply cloth [medrxiv.org/content/10.1101/2020.10.05.20207241v1]
    # 90% for N95 for safety (see manual)
    # 1- ply cloth REF???
    Mask_type = [0, 0.9, 0.59, 0.51, 0.35]

    # Conversions with applications of mask and activity to inhalation rate and CO2 emission
    # *** the exhalation equivalent for the virus is being accounted for in N_r
    inhRate = (
        inhRate_pure * (1 - Mask_type[mask_type]) * Activity_type_inh[activity_type]
    )  # ... actual inhlation rate, ltr/s
    co2_exhRate = (
        co2_exhRate_ref * metabolic_rate_forCO2[activity_type]
    ) / met_ref  # ... actual CO2 emission rate, ltr/s

    # Here we need an "effective" N_gen for aerosol particles
    # First five values are for zero vertical velocity and last five values are for 0.1 m/s upward vertical velocity
    # The indices are based on the aerosol cut-off diameter
    Ngen_base = [
        0.4527,
        0.4843,
        0.589,
        5.1152,
        16.2196,
        0.4728,
        0.5058,
        0.647,
        8.6996,
        30.073,
    ]
    # Find actual emission
    base_N_r = (
        Activity_type_Ngen[activity_type_sick]
        * Ngen_base[cutoff_type + 5 * verticalv_type]
    ) / 10**9
    Vl = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # viral load exponent, copies/ml
    N_r = (
        10 ** Vl[Vli] * base_N_r * (1 - Mask_type[mask_type_sick])
    )  # ... effective aerosol emission rate, PFU/s

    # Risk is p(N_vs) = 1-exp(-N_vs/riskConst);
    risk = 410  # ... constant for risk estimation, PFU

    # Additional variables
    V = Ar * Hr  # ... room volume, m^3
    Vperson = round(
        (ACH / 3600) * (V * 1000) * (1 / n_people)
    )  # ... ventilation rate, l/s/person

    # Conversions
    kappa = kappa / 3600  # ... 1/s
    delta = delta / 3600  # ... 1/s
    inhRate = inhRate / 1000  # ... m3/s

    ACH_fresh = (ACH * outside_air) / 100  # ...1/h
    ACH_recirc = ACH * (1 - (outside_air / 100))  # ... 1/h
    vent_fresh = ACH_fresh / 3600  # ... 1/s
    steril_rate = filterEff * (ACH_recirc / 3600)  # 1/s

    loss_rate = vent_fresh + steril_rate + kappa + delta
    loss_rate_co2 = vent_fresh

    co2_exhRate = co2_exhRate / 1000  # ,,, m3/s
    co2_exhRate = co2_exhRate * 10**6  # ...scale to calculate ppm in the end

    # Find minimum and maximum time for each event in seconds
    t0 = 0
    tMax = permanence * 60

    # Solver settings
    # dt = 0.5 * 60; # ... time increment, s
    dt = tMax / 400  # ... time increment, s

    # Initialisation
    R = []  # ... Risk over time
    C = []  # ... concentration vector, PFU/m3
    Ninh = []  # ... inhaled virus vector, PFU
    XCO2 = []  # ... CO2 mole fraction vector, ppm
    people_over_time = []  # ... total number of people within room, #
    infected_people_over_time = []  # ... total number of people within room, #

    time_series = np.arange(start=t0, stop=tMax, step=dt).tolist()

    people_over_time = [people_inst(tMax, t)["people"] for t in time_series]
    infected_people_over_time = [people_inst(tMax, t)["infected"] for t in time_series]

    for i in range(len(time_series)):
        t = time_series[i]
        hasPeople = people_over_time[i] > 0

        try:
            # Virus concentration
            C.append(
                (hasPeople * people_inst(tMax, t)["infected"] * N_r) / (V * loss_rate)
                + (
                    C[i - 1]
                    - (hasPeople * people_inst(tMax, t)["infected"] * N_r)
                    / (V * loss_rate)
                )
                * exp(-loss_rate * dt)
            )

            # CO2 Concentration
            if loss_rate_co2 > 0.0:
                XCO2.append(
                    co2_background
                    + (hasPeople * people_inst(tMax, t)["people"] * co2_exhRate)
                    / (V * loss_rate_co2)
                    + (
                        XCO2[i - 1]
                        - (hasPeople * people_inst(tMax, t)["people"] * co2_exhRate)
                        / (V * loss_rate_co2)
                    )
                    - (co2_background * exp(-loss_rate_co2 * dt))
                )
            else:
                # account for case where loss_rate_co2 is zero and the previous equation is not defined
                XCO2.append(
                    XCO2[i - 1]
                    + ((hasPeople * people_inst(tMax, t)["people"] * co2_exhRate) / V)
                    * dt
                )

            # Inhaled virus
            Ninh.append(Ninh[i - 1] + hasPeople * inhRate * dt * C[i])
            R.append(1 - exp(-Ninh[i] / risk))
        except IndexError:
            # Virus concentration
            C.append(
                (hasPeople * people_inst(tMax, t)["infected"] * N_r) / (V * loss_rate)
                + (
                    0
                    - (hasPeople * people_inst(tMax, t)["infected"] * N_r)
                    / (V * loss_rate)
                )
                * exp(-loss_rate * dt)
            )

            # CO2 Concentration
            if loss_rate_co2 > 0.0:
                XCO2.append(
                    co2_background
                    + (hasPeople * people_inst(tMax, t)["people"] * co2_exhRate)
                    / (V * loss_rate_co2)
                    + (
                        co2_background
                        - (hasPeople * people_inst(tMax, t)["people"] * co2_exhRate)
                        / (V * loss_rate_co2)
                    )
                    - (co2_background * exp(-loss_rate_co2 * dt))
                )
            else:
                # account for case where loss_rate_co2 is zero and the previous equation is not defined
                XCO2.append(
                    co2_background
                    + ((hasPeople * people_inst(tMax, t)["people"] * co2_exhRate) / V)
                    * dt
                )

            # Inhaled virus
            Ninh.append(hasPeople * inhRate * dt * C[i])
            R.append(1 - exp(-Ninh[i] / risk))

    # Final result
    return (
        C,
        R,
        XCO2,
        people_over_time,
        infected_people_over_time,
        time_series,
        Vperson,
    )


def ach_required(
    area: float,
    altura: float,
    aforo: int,
    actividad: int,
    permanencia: int,
    set_risk: float = 0.03,
    mask_type: int = 1,
    inf_percent: float = 10,
    viral_load: int = 10,
    cutoff_type: int = 3,
) -> float:
    """Función que calcula los ACH necesarios para llegar a un riesgo máximo de 3% +- 0.05.
        Retorna tanto las ACH como el riesgo máximo

    Args:
        area (float): area del ambiente
        altura (float): altura del ambiente
        aforo (int): aforo al cual se hace el cálculo
        actividad (int): opción de actividad a utilizar
        permanencia (int): tiempo de permanencia en minutos
        set_risk (float): riesgo máximo determinado

    Returns:
        List: Lista con las ACH obtenidas y el riesgo máximo
    """
    max_risk = 1
    ACH_custom = 0

    while max_risk > set_risk:
        ACH_custom += 0.1
        (_, R, _, _, _, _, _) = room_calculation(
            Ar=area,
            Hr=altura,
            n_people=aforo,
            Vli=viral_load,
            mask_type=mask_type,
            mask_type_sick=mask_type,
            activity_type=actividad,
            activity_type_sick=actividad,
            permanence=permanencia,
            ACH_custom=ACH_custom,
            inf_percent=inf_percent,
            cutoff_type=cutoff_type,
        )

        max_risk = R[-1]

    return ACH_custom


def risk_calculation(
    area: float, altura: float, aforo: int, actividad: int, permanencia: int
) -> float:
    """Función que calcula las ACH necesarias para llegar a un riesgo máximo de 3% +- 0.05.
        Retorna tanto las ACH como el riesgo máximo

    Args:
        area (float): area del ambiente
        altura (float): altura del ambiente
        aforo (int): aforo al cual se hace el cálculo
        actividad (int): opción de actividad a utilizar
        permanencia (int): tiempo de permanencia en minutos

    Returns:
        List: lista con el ACH obtenido y el riesgo máximo
    """
    max_risk = 1
    ACH_custom = 0

    while max_risk > 0.03:
        ACH_custom += 0.1
        (_, R, _, _, _, _, _) = room_calculation(
            Ar=area,
            Hr=altura,
            n_people=aforo,
            activity_type=actividad,
            activity_type_sick=actividad,
            permanence=permanencia,
            ACH_custom=ACH_custom,
        )

        max_risk = R[-1]

    return max_risk


# def occupancy(area:float, altura:float, actividad:int, permanencia:int, ach:float, inf_percent=10.0) -> dict:
#     """Función que calcula el aforo para llegar a un riesgo máximo de 3% +- 0.05

#     Args:
#         area (float): area del ambiente
#         altura (float): altura del ambiente
#         actividad (int): tipo de actividad que se está realizando
#         permanencia (int): tiempo en el aeropuerto
#         ach (float): renovaciones por ambiente

#     Returns:
#         results (int): diccionario que contiene el número de personas permitidas y la data asociada
#     """

#     aforo = 0
#     max_risk = 0

#     while max_risk < 0.03:
#         aforo += 1
#         (_, R, XCO2, _,_, _, _) = room_calculation(Ar = area, Hr = altura, n_people = aforo, activity_type = actividad, activity_type_sick = actividad, permanence = permanencia, ACH_custom = ach, inf_percent = inf_percent)

#         max_risk = R[-1]

#     results = {
#         "aforo": aforo,
#         "co2_contagiosidad": XCO2[-1],
#         "riesgo_contagiosidad": R[-1]
#     }

#     return results
