from datetime import datetime


TIME_FORMAT_STRING = "%Y-%m-%dT%H:%M:%SZ" 

# util for centralised place of time formatting, 


def get_time_in_string(date_time = datetime.utcnow()):
    """
    Time in RFC String format.

    Args:
    - date_time (datetime): datetime object or current time for default.

    Returns:
    - string: formatted date time.
    """
    return date_time.strftime(TIME_FORMAT_STRING)

def get_time_from_string(date_time_string):
    """
    Time in RFC String format.

    Args:
    - date_time_string (string): string formatted date time.

    Returns:
    - datetime object: derived from given string.
    """
    return datetime.strptime(date_time_string, TIME_FORMAT_STRING)