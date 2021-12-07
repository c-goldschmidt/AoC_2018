import sys

from days import get_days


def run_day(index=None):
    if index is None:
        index = -1

    if isinstance(index, str) and index != 'all':
        index = int(index) - 1

    days = get_days()
    days.sort(key=lambda x: x.__name__)

    if index == 'all':
        for day in days:
            day().run()
    else:
        days[index]().run()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        run_day(sys.argv[1])
    else:
        run_day()
