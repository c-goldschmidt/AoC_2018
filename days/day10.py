import re

from day import Day
from utils.point import Point

rx_point = re.compile(r'position=< ?(?P<x>-?\d+),  ?(?P<y>-?\d+)> velocity=< ?(?P<vx>-?\d+),  ?(?P<vy>-?\d+)>')


class MovingPoint(Point):
    def __init__(self, x, y, vx, vy):
        super().__init__(x, y)

        self.vx = int(vx)
        self.vy = int(vy)

        self.curr_x = self.x
        self.curr_y = self.y

    def reset(self):
        self.curr_x = self.x
        self.curr_y = self.y

    def tick(self):
        self.curr_x += self.vx
        self.curr_y += self.vy

    def is_at(self, x, y):
        return self.curr_x == x and self.curr_y == y


class Grid:
    def __init__(self):
        self.points = []

    def add(self, point):
        self.points.append(point)

    def tick(self):
        for point in self.points:
            point.tick()

    def reset(self):
        for point in self.points:
            point.reset()

    def print(self):
        min_x = min(point.curr_x for point in self.points)
        max_x = max(point.curr_x for point in self.points)
        min_y = min(point.curr_y for point in self.points)
        max_y = max(point.curr_y for point in self.points)

        if max_y - min_y > 9:
            # the correct image is always 10 lines high (basically the "font size")
            return False, []

        positions = {(point.curr_x, point.curr_y) for point in self.points}

        result = True
        lines = []
        for y in range(min_y, max_y + 1):
            line = ''
            for x in range(min_x, max_x + 1):
                chr = '#' if (x, y) in positions else '.'
                line += chr

            lines.append(line)
            if '#####' in line:
                result = True
        return result, lines


class Day10(Day):
    def parse(self, content):
        grid = Grid()

        for line in super().parse(content):
            match = rx_point.search(line)
            grid.add(MovingPoint(
                match.group('x'),
                match.group('y'),
                match.group('vx'),
                match.group('vy'),
            ))
        return grid

    def part1(self):
        iterations = 0
        while True:
            iterations += 1
            self.input.tick()
            result, lines = self.input.print()

            if result:
                print('\n'.join(lines))
                break

        return iterations

    def part2(self):
        return 'see part1 result'
