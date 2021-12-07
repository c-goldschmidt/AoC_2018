import re

from day import Day
from utils.grid import Grid
from utils.point import UniquePoint
from utils.timer import Timer

rx_collapsible = re.compile(r'(?P<start>[(|^])(?P<prefix>[NESW]+)\((?P<contents>[NESW|]+)\)')


class DoorGrid(Grid):
    fallback = '#'
    directions = {
        'N': UniquePoint.Y_MINUS,
        'S': UniquePoint.Y_PLUS,
        'W': UniquePoint.X_MINUS,
        'E': UniquePoint.X_PLUS,
    }

    def __init__(self):
        super().__init__()
        self.resolved = {}

    def update_bounds(self, x, y):
        self.max_x = max(self.max_x, x + 1)
        self.max_y = max(self.max_y, y + 1)
        self.min_x = x if self.min_x is None else min(self.min_x, x - 1)
        self.min_y = y if self.min_y is None else min(self.min_y, y - 1)

    def add_regex(self, rx_input):
        start = UniquePoint(1000, 1000)

        self._solve_path(start, rx_input)
        self[start] = 'X'

    def _resolve_paths(self):
        start = UniquePoint(1000, 1000)

        queue = [start]
        self.resolved = {start: 0}

        while queue:
            point = queue.pop(0)

            current_val = self.resolved.get(point)
            step_val = current_val + 1

            for next_step in self.next_possible(point):
                next_val = self.resolved.get(next_step)
                if next_step != start and (not next_val or next_val > step_val):
                    self.resolved[next_step] = step_val
                    queue.append(next_step)

        return max(self.resolved.values())

    def find_furthest_point(self):
        if not self.resolved:
            self._resolve_paths()
        return max(self.resolved.values())

    def get_all_paths_over_length(self, length):
        if not self.resolved:
            self._resolve_paths()
        return len([x for x in self.resolved.values() if x >= length])

    def next_possible(self, current):
        next_points = []
        for direction in self.directions.values():
            in_direction = current + direction
            if self[in_direction] in '|-':
                next_points.append(in_direction + direction)

        return next_points

    def _move(self, point, direction):
        self[point] = '.'
        point += self.directions[direction]
        self[point] = '|' if direction in 'WE' else '-'
        point += self.directions[direction]
        self[point] = '.'
        return point

    def _solve_path(self, start, paths):
        paths = self._collapse_paths(paths)

        t = Timer()
        print(f'checking out {len(paths)} paths')
        for path in paths:
            location = start
            for step in path:
                location = self._move(location, step)

        size_y = self.max_y - self.min_y
        size_x = self.max_x - self.min_x
        t.next(f'created {size_y} x {size_x} grid')

    @staticmethod
    def _collapse_paths(str_in):
        # at first i tried actually recursively walking the paths,
        # but resolving the subpaths first is waaay more performant
        match = rx_collapsible.search(str_in)

        while match:
            prefix = match.group('prefix')
            contents = match.group('contents').split('|')
            start = match.start()
            end = match.end()

            str_in = str_in[:start] + match.group('start') + '|'.join([prefix + c for c in contents]) + str_in[end:]
            match = rx_collapsible.search(str_in)

        return str_in[1:-1].split('|')


class Day20(Day):
    grid: DoorGrid

    def part1(self):
        self.grid = DoorGrid()
        self.grid.add_regex(self.input[0])
        return self.grid.find_furthest_point()

    def part2(self):
        return self.grid.get_all_paths_over_length(1000)
