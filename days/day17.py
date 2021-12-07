import re
import sys
from collections import defaultdict

from day import Day
from utils.grid import Grid
from utils.point import UniquePoint, Point

rx_scan_x = re.compile(r'x=(?P<start>\d+)(?:\.\.(?P<end>\d+))?')
rx_scan_y = re.compile(r'y=(?P<start>\d+)(?:\.\.(?P<end>\d+))?')


class FluidGrid(Grid):
    def __init__(self):
        super().__init__()
        self.wet = set()

    def update_bounds(self, x, y):
        self.max_x = max(self.max_x, x + 1)
        self.max_y = max(self.max_y, y)
        self.min_x = x if self.min_x is None else min(self.min_x, x - 1)
        self.min_y = y if self.min_y is None else min(self.min_y, y)

    def fill(self, start, direction=UniquePoint.Y_PLUS):
        self.wet.add(start)

        below = start + UniquePoint.Y_PLUS
        left = start + UniquePoint.X_MINUS
        right = start + UniquePoint.X_PLUS

        if self[below] != '#':
            if below not in self.wet and below.y <= self.max_y:
                self.fill(below)
            if self[below] != '~':
                return False

        left_filled = self[left] == '#'  # no need to touch clay, so we assume filled
        if not left_filled and left not in self.wet:
            left_filled = self.fill(left, direction=UniquePoint.X_MINUS)

        right_filled = self[right] == '#'
        if not right_filled and right not in self.wet:
            right_filled = self.fill(right, direction=UniquePoint.X_PLUS)

        if direction == UniquePoint.Y_PLUS and left_filled and right_filled:
            self[start] = '~'
            self._fill(left, UniquePoint.X_MINUS)
            self._fill(right, UniquePoint.X_PLUS)
        elif direction == UniquePoint.X_MINUS:
            return left_filled or self[left] == '#'
        elif direction == UniquePoint.X_PLUS:
            return right_filled or self[left] == '#'

        return False

    def _fill(self, start, direction):
        while start in self.wet:
            self[start] = '~'
            start = start + direction

    def print(self, marker=None):
        # debug, but i left it in because it looks cool
        for y in self.iter_y():
            line = ''
            marker_in_line = False
            for x in self.iter_x():
                point = UniquePoint(x, y)
                item = self[point]

                if item == '.' and point in self.wet:
                    item = '|'

                if marker and point == marker:
                    marker_in_line = True
                    item = 'X'

                if point in self.wet:
                    item = f'\033[94m{item}\033[0m'

                line += item
            if marker_in_line:
                line += f'  =>  {marker}'

            print(line)

    def count_wet(self):
        count = 0
        for y, x in self.iter():
            point = UniquePoint(x, y)
            count += 1 if point in self.wet or self[point] == '~' else 0
        return count

    def count_filled(self):
        count = 0
        for y, x in self.iter():
            point = UniquePoint(x, y)
            count += 1 if self[point] == '~' else 0
        return count


class Day17(Day):
    input: FluidGrid

    def __init__(self):
        super().__init__()

        # we're going deep here...
        sys.setrecursionlimit(10000)

    def get_value(self, in_str, coord):
        if coord == 'x':
            return rx_scan_x.search(in_str)
        return rx_scan_y.search(in_str)

    @staticmethod
    def range(match):
        return range(int(match.group('start')), int(match.group('end') or match.group('start')) + 1)

    def iter(self, match_x, match_y):
        for y in self.range(match_y):
            for x in self.range(match_x):
                yield x, y

    def parse(self, content):
        grid = FluidGrid()
        for line in super().parse(content):
            match_x = self.get_value(line, 'x')
            match_y = self.get_value(line, 'y')

            for x, y in self.iter(match_x, match_y):
                grid.set(x, y, '#')

        return grid

    def part1(self):
        self.input.fill(UniquePoint(500, self.input.min_y))
        return self.input.count_wet()

    def part2(self):
        return self.input.count_filled()
