from datetime import datetime, timedelta
from typing import Tuple, Union


def generate_day_range_for_date(date: datetime) -> Tuple[datetime, datetime]:
    """Given a datetime, returns the range in which the date falls in.

    Args:
        date (datetime): Datetime object.

    Returns:
        Tuple[datetime, datetime]: Tuple containing the begining and end (gte, lte)
        of the day corresponding to the input date.
    """
    return (
        date.replace(hour=0, minute=0, second=0),
        date.replace(hour=23, minute=59, second=59),
    )


def is_between(value, right_value, left_value) -> Union[bool, None]:
    """Checks that value is between other two values

    Args:
        value (any): Value to check. Needs to support comparison with
        the other values.

        right_value (any): Value to check if it is bigger than value.
        Needs to support comparison with the other values.

        left_value (any): Value to check if it is smaller than value.
        Needs to support comparison with the other values.

    Returns:
        Union[bool, None]: Boolean value of the comparison or None if
        comparison failed due to the values not supporting comparison.
    """
    try:
        return left_value < value < right_value
    except TypeError:
        return None
