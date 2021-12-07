import math
import re
from typing import List

from day import Day


class NanoBot:

    def __init__(self, x, y, z, range):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.range = int(range)

        self._min_x = self.x - self.range
        self._max_x = self.x + self.range
        self._min_y = self.y - self.range
        self._max_y = self.y + self.range
        self._min_z = self.z - self.range
        self._max_z = self.z + self.range

        self.hash = hash((self.x, self.y, self.z, self.range))

    def dist(self, other):
        # manhattan distance
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def p_dist(self, pos):
        x, y, z = pos
        return abs(self.x - x) + abs(self.y - y) + abs(self.z - z)

    def in_range(self, pos):
        return self.p_dist(pos) <= self.range

    def eq(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return f'{self.__class__.__name__}[{self.x},{self.y},{self.z}]'

    def __eq__(self, other):
        return self.hash == other.hash

    def __hash__(self):
        return self.hash


class Cube:
    def __init__(self, center, size):
        self.center = center
        self.size = size

    def subs(self):
        if self.size == 1:
            return self.last_cubes()

        size = math.ceil(self.size / 2)
        x, y, z = self.center

        return [
            Cube((x - size, y - size, z - size), size),
            Cube((x - size, y - size, z + size), size),
            Cube((x - size, y + size, z + size), size),
            Cube((x - size, y + size, z - size), size),
            Cube((x + size, y - size, z + size), size),
            Cube((x + size, y - size, z - size), size),
            Cube((x + size, y + size, z - size), size),
            Cube((x + size, y + size, z + size), size),
        ]

    def last_cubes(self):
        x, y, z = self.center

        results = []
        for _x in range(x - 1, x + 2):
            for _y in range(y - 1, y + 2):
                for _z in range(z - 1, z + 2):
                    results.append(Cube((_x, _y, _z), 0))

        return results

    def p_dist(self, pos):
        x1, y1, z1 = pos
        x2, y2, z2 = self.center
        return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)

    def points(self):
        x, y, z = self.center

        if self.size == 0:
            return [(x, y, z)]

        return [
            (x - self.size, y - self.size, z - self.size),
            (x - self.size, y - self.size, z + self.size),
            (x - self.size, y + self.size, z + self.size),
            (x - self.size, y + self.size, z - self.size),
            (x + self.size, y - self.size, z + self.size),
            (x + self.size, y - self.size, z - self.size),
            (x + self.size, y + self.size, z - self.size),
            (x + self.size, y + self.size, z + self.size),
        ]


class Day23(Day):
    input: List[NanoBot]

    def parse(self, content):
        bots = []
        rx_match = re.compile(r'^pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(-?\d+)$')

        for line in super().parse(content):
            match = rx_match.match(line)
            bots.append(NanoBot(*match.groups()))

        return bots

    def part1(self):
        strongest = sorted(self.input, key=lambda b: b.range)[-1]
        in_range = [bot for bot in self.input if bot.dist(strongest) < strongest.range]
        return len(in_range)

    def in_range(self, cube):
        total_in_range = 0
        for bot in self.input:
            for point in cube.points():
                if bot.in_range(point):
                    total_in_range += 1
                    break
        return total_in_range

    def check_cubes(self, cubes):
        max_in_range = 0

        while True:
            cube = None
            at_max = []

            while cubes:
                cube = cubes.pop()

                in_range = self.in_range(cube)
                if in_range > max_in_range:
                    at_max = [cube]
                    max_in_range = in_range
                elif in_range == max_in_range:
                    at_max.append(cube)

            if cube and cube.size == 0:
                return at_max

            cubes = [subcube for cube in at_max for subcube in cube.subs()]

    def part2(self):
        min_x = min([bot.x - bot.range for bot in self.input])
        max_x = max([bot.x + bot.range for bot in self.input])
        min_y = min([bot.y - bot.range for bot in self.input])
        max_y = max([bot.y + bot.range for bot in self.input])
        min_z = min([bot.y - bot.range for bot in self.input])
        max_z = max([bot.y + bot.range for bot in self.input])
        max_dist_x = max_x - min_x
        max_dist_y = max_y - min_y
        max_dist_z = max_z - min_z

        initial_size = max(max_dist_x, max_dist_y, max_dist_z)
        initial_size += initial_size % 2

        main_cube = Cube((0, 0, 0), initial_size)
        best_subs = self.check_cubes(main_cube.subs())

        return min([cube.p_dist((0, 0, 0)) for cube in best_subs])
