from word2number import w2n
from datetime import date


def string_to_num_of_days(days_string: str):
    if days_string == 'tomorrow':
        return 1
    elif days_string == 'week' or days_string == 'a week' in days_string:
        return 7
    elif 'week' in days_string:
        return 7 * w2n.word_to_num(days_string)
    else:
        return w2n.word_to_num(days_string)


def next_weekday(weekday: int):
    """weekday - number from 0 to 6, where 0 is Monday and 6 is Sunday"""
    today = date.today().weekday()
    days_ahead = weekday - today
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return days_ahead
