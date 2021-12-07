from functools import lru_cache

from day import Day
from utils.colors import color, BLUE, RED, YELLOW, MAGENTA, GREEN
from utils.grid import Grid
from utils.point import UniquePoint, ZERO
from utils.timer import Timer

TOOL_NONE = 0
TOOL_TORCH = 1
TOOL_CLIMB = 2

TERRAIN_ROCK = 0
TERRAIN_WET = 1
TERRAIN_NARROW = 2

class ErosionGrid(Grid):
    fallback = -1

    def __init__(self, depth, target):
        super().__init__()
        self.depth = depth
        self.target = target

        self._debug_travel = None

    def _get_erosion_level(self, point):
        if point == ZERO or point == self.target:
            index = 0
        elif point.y == 0:
            index = point.x * 16807
        elif point.x == 0:
            index = point.y * 48271
        else:
            index = self[point + UniquePoint.X_MINUS] * self[point + UniquePoint.Y_MINUS]

        return (index + self.depth) % 20183

    def risk_level(self):
        return sum(value % 3 for value in self.iter_values())

    def get(self, x, y):
        value = super().get(x, y)
        if value == self.fallback:
            point = UniquePoint(x, y)
            value = self._get_erosion_level(point)
            self[point] = value
        return value

    def print(self):
        visited = set([p[0] for p in self._debug_travel.keys()]) if self._debug_travel else set()

        for y in self.iter_y():
            line = ''
            for x in self.iter_x():
                point = UniquePoint(x, y)
                value = self[point] % 3

                if point == ZERO:
                    line += color('M', BLUE)
                elif point == self.target:
                    line += color('T', RED)
                elif point in visited:
                    if self._debug_travel.get((point, TOOL_CLIMB)):
                        use_color = MAGENTA
                        use_tool = TOOL_CLIMB
                    elif self._debug_travel.get((point, TOOL_TORCH)):
                        use_color = YELLOW
                        use_tool = TOOL_TORCH
                    else:
                        use_color = GREEN
                        use_tool = TOOL_NONE

                    line += color(self._debug_travel[(point, use_tool)], use_color)

                elif value == 0:
                    line += '.'
                elif value == 1:
                    line += '='
                elif value == 2:
                    line += '|'
                else:
                    line += '?'

            print(line)

    def fill(self):
        for y in range(self.target.y + 1):
            for x in range(self.target.x + 1):
                point = UniquePoint(x, y)
                self[point] = self._get_erosion_level(point)

    @lru_cache
    def _type(self, point):
        return self[point] % 3

    def _rollback(self, prev, end, result=None):
        if not result:
            result = {}

        if end not in prev:
            result[end] = 'o'
            return result

        result = self._rollback(prev, prev[end])
        result[end] = 'o'
        return result

    def find_path_to_target(self):
        prev = {}
        g_score = {}
        f_score = {}
        queue = [(0, ZERO, TOOL_TORCH)]

        g_score[(ZERO, TOOL_TORCH)] = 0
        f_score[(ZERO, TOOL_TORCH)] = ZERO.dist(self.target)

        while len(queue) > 0:
            current_item = list(sorted(queue, key=lambda p: f_score[(p[1], p[2])]))[0]
            _, location, tool = current_item

            if location == self.target and tool == TOOL_TORCH:
                self._debug_travel = self._rollback(prev, (location, tool))
                return g_score[(location, tool)]

            queue.remove(current_item)
            for next_item in self.next_possible(location, tool):
                next_cost, next_point, next_tool = next_item

                next_score = g_score[(location, tool)] + next_cost
                next_combo = (next_point, next_tool)

                if next_combo not in g_score or next_score < g_score[next_combo]:
                    prev[next_combo] = (location, tool)
                    g_score[next_combo] = next_score
                    f_score[next_combo] = g_score[next_combo] + next_point.dist(self.target)

                    if next_item not in queue:
                        queue.append(next_item)

        return None

    def next_possible(self, point, current_tool):
        results = []
        for neighbor in point.neighbors():
            if neighbor.x < 0 or neighbor.y < 0:
                continue

            terrain = self._type(neighbor)

            if terrain == TERRAIN_ROCK and current_tool in (TOOL_TORCH, TOOL_CLIMB):
                results.append((1, neighbor, current_tool))

            if terrain == TERRAIN_WET and current_tool in (TOOL_NONE, TOOL_CLIMB):
                results.append((1, neighbor, current_tool))

            if terrain == TERRAIN_NARROW and current_tool in (TOOL_NONE, TOOL_TORCH):
                results.append((1, neighbor, current_tool))

        current_terrain = self._type(point)
        if current_terrain == TERRAIN_ROCK:
            results += [(7, point, TOOL_TORCH), (7, point, TOOL_CLIMB)]

        if current_terrain == TERRAIN_WET:
            results += [(7, point, TOOL_NONE), (7, point, TOOL_CLIMB)]

        if current_terrain == TERRAIN_NARROW:
            results += [(7, point, TOOL_NONE), (7, point, TOOL_TORCH)]

        return [res for res in results if res[0] == 1 or res[2] != current_tool]


class Day22(Day):
    input: ErosionGrid

    def parse(self, content):
        lines = super().parse(content)
        depth = int(lines[0].split(': ')[1])

        target_coords = lines[1].split(': ')[1].split(',')
        target = UniquePoint(*target_coords)
        return ErosionGrid(depth, target)

    def part1(self):
        self.input.fill()
        return self.input.risk_level()

    def part2(self):
        result = self.input.find_path_to_target()
        self.input.print()  # i left it in cause it looks cool
        return result
