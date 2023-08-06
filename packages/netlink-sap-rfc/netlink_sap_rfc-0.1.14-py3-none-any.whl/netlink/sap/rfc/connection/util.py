import datetime


DATE_CONVERTERS = {'1': "%d.%m.%Y",
                   '2': "%m/%d/%Y",
                   '3': "%m-%d-%Y",
                   '4': "%Y.%m.%d",
                   '5': "%Y/%m.%d",
                   '6': "%Y-%m-%d"}

TIME_CONVERTERS = {'0': "%H:%M:%S",
                   '1': "%I:%M:%S %p",
                   '2': "%I:%M:%S %p",
                   '3': "%H:%M:%S %p",
                   '4': "%H:%M:%S %p"}


def make_date_time_converters(date_format, time_format):
    if date_format not in DATE_CONVERTERS or time_format not in TIME_CONVERTERS:
        raise NotImplementedError

    def date_converter(value):
        return datetime.datetime.strptime(value, DATE_CONVERTERS[date_format]).date()

    def time_converter(value):
        return datetime.datetime.strptime(value, TIME_CONVERTERS[time_format]).time()

    return date_converter, time_converter
