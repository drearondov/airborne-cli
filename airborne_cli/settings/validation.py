"""
CLI input validation for options
"""
from typer import BadParameter


def validate_occupancy_percentages(occupancy_list: list[float]) -> list[float]:
    """Validates input list of occupancy percentages. Only return the list of all have succeded.

    Args:
        occupancy_list (list[float]): List of percentages to be evaluated

    Returns:
        list[float]: Evaluated percentages
    """
    for occupancy_percentage in occupancy_list:
        if occupancy_percentage < 0:
            raise BadParameter(
                "Occupancy percentage cannot be less than 0%. Check you input."
            )
        elif occupancy_percentage > 100:
            raise BadParameter(
                "Occupancy percentage cannot be over 100%. Check your input."
            )

    return occupancy_list


def validate_infected_percentages(infected_list: list[float]) -> list[float]:
    """Validates input list of infected percentages. Only return the list of all have succeded.

    Args:
        infected_list (list[float]): List of percentages to be evaluated

    Returns:
        list[float]: Evaluated percentages
    """
    for infected_percentage in infected_list:
        if infected_percentage < 0:
            raise BadParameter(
                "Percentage of people infected cannot be less than 0%. Check you input."
            )
        elif infected_percentage > 100:
            raise BadParameter(
                "Percentage of people infected cannot be over 100%. Check your input."
            )

    return infected_list


def validate_hex_colors(color_list: list[str]) -> list[str]:
    """Validate if the list provided has all hex numbers

    Args:
        color_list (list[str]): List of colors in input

    Returns:
        list[str]): Validated color list
    """

    def ishex(s: str) -> bool:
        """Checks if number is hex

        Args:
            s (str): String to check

        Returns:
            bool: Result of the evaluation
        """
        try:
            int(s, 16)
            return True
        except ValueError:
            return False

    for color in color_list:
        if color[0] != "#":
            raise BadParameter("All colors must start with '#'")

        if not ishex(color[1:]):
            raise BadParameter("Invalid hex color code")

    return color_list
