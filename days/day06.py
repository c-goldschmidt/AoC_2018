import sys
from collections import defaultdict

from day import Day
from utils.point import Point


class Day06(Day):
    def parse(self, content):
        return [Point(*line.split(', '), name=index) for index, line in enumerate(super().parse(content)) if line]

    def _get_closest(self, point):
        min_dist = sys.maxsize
        at_min_dist = []
        for other in self.input:
            dist = other.dist(point)
            if dist < min_dist:
                at_min_dist = [other]
                min_dist = dist
            elif dist == min_dist:
                at_min_dist.append(other)
        return at_min_dist

    def _total_dist(self, point):
        total = 0

        for other in self.input:
            total += point.dist(other)

        return total

    def _is_extreme(self, point, min_x, max_x, min_y, max_y):
        return point.x in (min_x, max_x) or point.y in (min_y, max_y)

    def _minmax(self):
        min_x = min([point.x for point in self.input])
        max_x = max([point.x for point in self.input])
        min_y = min([point.y for point in self.input])
        max_y = max([point.y for point in self.input])
        return min_x, max_x, min_y, max_y

    def part1(self):
        min_x, max_x, min_y, max_y = self._minmax()

        areas = defaultdict(int)
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                point = Point(x, y)

                closest = self._get_closest(point)
                if len(closest) == 1 and not self._is_extreme(closest[0], min_x, max_x, min_y, max_y):
                    areas[closest[0].name] += 1

        return max(areas.values())

    def part2(self):
        min_x, max_x, min_y, max_y = self._minmax()

        result = 0
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                point = Point(x, y)
                total = self._total_dist(point)

                if total < 10000:
                    result += 1

        return result
