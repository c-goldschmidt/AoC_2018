import re
from collections import defaultdict
from datetime import datetime, timedelta

from day import Day


rx_date = re.compile(r'\[(?P<date>\d+-\d+-\d+ \d+:\d+)] (?P<entry>.+)$')
rx_id = re.compile(r'Guard #(?P<id>\d+) begins shift')


class Log:
    def __init__(self):
        self.entries = defaultdict(dict)

    def add_entry(self, entry):
        match = rx_date.search(entry)

        timestamp = datetime.strptime(match.group('date'), '%Y-%m-%d %H:%M')
        self.entries[(timestamp.month, timestamp.day)][(timestamp.hour, timestamp.minute)] = match.group('entry')

    def days(self):
        return sorted(self.entries.keys())

    def timestamps(self, day):
        return sorted(self.entries[day].keys())

    def _prev_day(self, day):
        date = datetime(year=1518, month=day[0], day=day[1])
        date = date - timedelta(days=1)
        return date.month, date.day

    def on_duty(self, day):
        today = self.timestamps(day)
        if 'begins shift' in self.entries[day][today[0]]:
            guard = self.entries[day][today[0]]
        else:
            prev_day = self._prev_day(day)
            prev = self.timestamps(prev_day)
            guard = self.entries[prev_day][prev[-1]]

        return rx_id.search(guard).group('id')

    def sleeps(self, day):

        sleep_minutes = {}
        current = False
        for minute in range(60):
            if (0, minute) in self.entries[day]:
                entry = self.entries[day][(0, minute)]

                if 'falls asleep' in entry:
                    current = True
                if 'wakes up' in entry:
                    current = False

            sleep_minutes[(0, minute)] = current

        return [k for k, v in sleep_minutes.items() if v]


class Day04(Day):

    def parse(self, content):
        log = Log()
        for line in super().parse(content):
            log.add_entry(line)
        return log

    def part1(self):
        total_sleep_by_guard = defaultdict(int)
        max_sleep_minute = defaultdict(lambda: defaultdict(int))

        for day in self.input.days():
            g = self.input.on_duty(day)
            sleeps = self.input.sleeps(day)
            total_sleep_by_guard[g] += len(sleeps)
            for sleep in sleeps:
                max_sleep_minute[g][sleep] += 1

        best_guards = sorted(total_sleep_by_guard.items(), key=lambda item: item[1], reverse=True)
        best_id = best_guards[0][0]

        best_minutes = sorted(max_sleep_minute[best_id].items(), key=lambda item: item[1], reverse=True)
        return int(best_id) * best_minutes[0][0][1]

    def part2(self):
        max_sleep_minute = defaultdict(lambda: defaultdict(int))

        for day in self.input.days():
            g = self.input.on_duty(day)
            sleeps = self.input.sleeps(day)

            for sleep in sleeps:
                max_sleep_minute[g][sleep] += 1

        best = None
        for minute in range(60):
            for g in max_sleep_minute:
                g_sleep = max_sleep_minute[g][(0, minute)]

                if not best or best[2] < g_sleep:
                    best = (g, minute, g_sleep)

        return int(best[0]) * best[1]