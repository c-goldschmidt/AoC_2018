import re
from concurrent.futures import ThreadPoolExecutor

from day import Day

rx_replace = re.compile(r'^(?P<before>.*?)(?P<rep>([a-z])(?=[A-Z])(?i:\3)|(([A-Z])(?=[a-z])(?i:\5)))(?P<after>.*)')


class Day05(Day):

    def parse(self, content):
        return super().parse(content)[0]

    def part1(self):
        return len(self._replace(self.input))

    @staticmethod
    def _replace(value):
        base = value
        while True:
            match = rx_replace.search(base)
            if not match:
                break

            base = match.group('before') + match.group('after')
        return base

    @staticmethod
    def _replace_without_char(data):
        without = re.sub(data[0], '', data[1], flags=re.I)
        return len(Day05._replace(without))

    def part2(self):
        removable = set(self.input.lower())

        with ThreadPoolExecutor(max_workers=8) as executor:
            data = ((item, self.input) for item in removable)
            results = executor.map(Day05._replace_without_char, data)
            min_len = min(results)

        return min_len
