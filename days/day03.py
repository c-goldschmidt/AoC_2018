import re
from collections import defaultdict

from day import Day

rx_line = re.compile(r'#(?P<id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)')


class Grid:

    def __init__(self):
        self.used_cells = defaultdict(list)

    def add(self, part):
        for y in range(part.y, part.y + part.h):
            for x in range(part.x, part.x + part.w):
                self.used_cells[(x, y)].append(part.id)

    def overlap(self):
        return len([val for val in self.used_cells.values() if len(val) > 1])

    def find_intact(self):
        in_multiple = set()
        in_single = set()

        for value in self.used_cells.values():
            if len(value) == 1:
                in_single.update(set(value))
            else:
                in_multiple.update(set(value))

        return in_single - in_multiple


class Part:
    def __init__(self, line):
        match = rx_line.search(line)

        self.id = match.group('id')
        self.x = int(match.group('x'))
        self.y = int(match.group('y'))
        self.w = int(match.group('w'))
        self.h = int(match.group('h'))

    def __repr__(self):
        return f'#{self.id} => {self.x}, {self.y} / {self.w} * {self.h}'


class Day03(Day):

    def parse(self, content):
        return [Part(line) for line in super().parse(content) if line]

    def get_grid(self):
        grid = Grid()
        for part in self.input:
            grid.add(part)
        return grid

    def part1(self):
        grid = self.get_grid()
        return grid.overlap()

    def part2(self):
        grid = self.get_grid()
        return grid.find_intact()
