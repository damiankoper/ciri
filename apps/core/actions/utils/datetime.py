from word2number import w2n
from datetime import date

def string_to_num_of_days(days_string: str):
    if 'day after tomorrow' in days_string:
        return 2
    elif 'day before yesterday' in days_string:
        return -2
    elif 'yesterday' in days_string :
        return -1
    elif 'tomorrow' in days_string:
        return 1
    elif 'today' in days_string:
        return 0
    elif days_string == 'week' or days_string == 'a week' in days_string:
        return 7
    elif 'week' in days_string:
        return 7 * w2n.word_to_num(days_string)
    else:
        return w2n.word_to_num(days_string)

def get_number_of_days(days_string):
    days_string = days_string.lower()
    possible_digits = [int(s) for s in days_string.split() if s.isdigit()]

    if possible_digits:
        return possible_digits[0]
    else:
        return string_to_num_of_days(days_string)


def next_weekday(weekday: int):
    """weekday - number from 0 to 6, where 0 is Monday and 6 is Sunday"""
    today = date.today().weekday()
    days_ahead = weekday - today
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return days_ahead


def get_relative_time(time_string: str):
    weekdays = ['monday', 'tuesday', 'wednesday',
                'thursday', 'friday', 'saturday', 'sunday']

    relative_time = time_string.lower()
    possible_digits = [int(s) for s in relative_time.split() if s.isdigit()]

    if relative_time in weekdays:
        weekday_number = weekdays.index(relative_time)
        number_of_days = next_weekday(weekday_number)
    elif possible_digits:
        number_of_days = possible_digits[0]
    else:
        number_of_days = string_to_num_of_days(relative_time)

    return number_of_days
