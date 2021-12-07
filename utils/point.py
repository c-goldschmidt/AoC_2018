class Point:
    X_PLUS = (1, 0)
    X_MINUS = (-1, 0)
    Y_PLUS = (0, 1)
    Y_MINUS = (0, -1)

    X_PLUS_Y_MINUS = (1, -1)
    Y_PLUS_X_MINUS = (-1, 1)
    XY_PLUS = (1, 1)
    XY_MINUS = (-1, -1)

    def __init__(self, x, y, name=None):
        self.x = int(x)
        self.y = int(y)
        self.name = name

    def dist(self, other):
        # manhattan distance
        return abs(self.x - other.x) + abs(self.y - other.y)

    def eq(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        name = f'({self.name})' if self.name else ''
        return f'{self.__class__.__name__}[{self.x},{self.y}]{name}'

    def __add__(self, other):
        x = y = 0

        if isinstance(other, Point):
            x, y = other.x, other.y

        if isinstance(other, tuple):
            x, y = other

        return self.__class__(self.x + x, self.y + y)

    def neighbors(self, include_corners=False):
        directions = [
            self.X_PLUS,
            self.X_MINUS,
            self.Y_PLUS,
            self.Y_MINUS,
        ]
        if include_corners:
            directions += [
                self.X_PLUS_Y_MINUS,
                self.Y_PLUS_X_MINUS,
                self.XY_PLUS,
                self.XY_MINUS,
            ]

        for direction in directions:
            yield self + direction


class UniquePoint(Point):
    def __init__(self, x, y, name=None):
        super().__init__(x, y)
        self.hash = hash((self.x, self.y, name))

    def __eq__(self, other):
        return self.hash == other.hash

    def __hash__(self):
        return self.hash


ZERO = UniquePoint(0, 0)