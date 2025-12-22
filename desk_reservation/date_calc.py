from datetime import date, timedelta

def days_calc(arg_one, arg_two):
    """
    Returns list of days (datetime) between given arguments.
    """
    date_list = []
    dummy_date = arg_one
    while dummy_date <= arg_two:
        date_list.append(dummy_date)
        dummy_date += timedelta(days=1)
    return date_list

"""
funkcja działa tu ok ale jest problem w tym że 'DateField" z django != timedelta, nie mogę tego w ten sposób dodać

"""


# start_date = date(2025, 1, 1)
# end_date = date(2025, 1, 31)

# print(days_calc(start_date, end_date))
