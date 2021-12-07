import copy
from collections import defaultdict

from utils.point import Point, UniquePoint


class Grid:
    fallback = '.'

    def __init__(self):
        self.grid = defaultdict(dict)
        self.max_x = 0
        self.max_y = 0
        self.min_x = None
        self.min_y = None

    def clone(self):
        new_grid = self.__class__()
        new_grid.grid = copy.deepcopy(self.grid)
        new_grid.min_x = self.min_x
        new_grid.min_y = self.min_y
        new_grid.max_x = self.max_x
        new_grid.max_y = self.max_y
        return new_grid

    def print(self):
        for y in self.iter_y():
            line = ''
            for x in self.iter_x():
                line += self[(x, y)]
            print(line)

    def set(self, x, y, item):
        self.grid[y][x] = item
        self.update_bounds(x, y)

    def get(self, x, y):
        return self.grid[y].get(x, self.fallback)

    def update_bounds(self, x, y):
        self.max_x = max(self.max_x, x)
        self.max_y = max(self.max_y, y)
        self.min_x = x if self.min_x is None else min(self.min_x, x)
        self.min_y = y if self.min_y is None else min(self.min_y, y)

    def iter_y(self):
        for y in range(self.min_y, self.max_y + 1):
            yield y

    def iter_x(self):
        for x in range(self.min_x, self.max_x + 1):
            yield x

    def iter(self):
        for y in self.iter_y():
            for x in self.iter_x():
                yield y, x

    def iter_points(self):
        for y in self.iter_y():
            for x in self.iter_x():
                yield UniquePoint(x, y)

    def iter_values(self):
        for y in self.iter_y():
            for x in self.iter_x():
                yield self.grid[y][x]

    def __getitem__(self, item):
        if isinstance(item, Point):
            x, y = item.x, item.y
        else:
            x, y = item

        return self.get(x, y)

    def __setitem__(self, key, value):
        if isinstance(key, Point):
            x, y = key.x, key.y
        else:
            x, y = key

        self.set(x, y, value)