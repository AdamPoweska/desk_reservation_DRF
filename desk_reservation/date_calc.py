from datetime import date, timedelta

def deduction_func(arg_one, arg_two):
    date_list = []
    dummy_date = arg_one
    while dummy_date <= arg_two:
        date_list.append(dummy_date)
        dummy_date += timedelta(days=1)
    # result = arg_two - arg_one
    return date_list

start_date = date(2025, 1, 1)
end_date = date(2025, 1, 31)

print(deduction_func(start_date, end_date))