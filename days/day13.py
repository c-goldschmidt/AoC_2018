from day import Day
from utils.point import Point


class Cart(Point):
    turns = ['left', 'straight', 'right']

    def __init__(self, x, y, direction):
        super().__init__(x, y)

        self._last_turn = 0
        self.direction = direction

    @property
    def direction_name(self):
        if self.direction == (0, -1):
            return 'up'
        elif self.direction == (1, 0):
            return 'right'
        elif self.direction == (0, 1):
            return 'down'
        elif self.direction == (-1, 0):
            return 'left'
        else:
            raise ValueError('i should not be here')

    def turn_left(self):
        self.direction = (self.direction[1], -self.direction[0])

    def turn_right(self):
        self.direction = (-self.direction[1], self.direction[0])

    def turn_cross(self):
        turn = self.turns[self._last_turn % 3]

        if turn == 'left':
            self.turn_left()
        elif turn == 'right':
            self.turn_right()

        self._last_turn += 1
        return self.direction

    def move(self):
        self.x += self.direction[0]
        self.y += self.direction[1]

    def move_for_tile(self, tile_below):
        if tile_below == '\\':
            if self.direction_name in ('left', 'right'):
                self.turn_right()
            else:
                self.turn_left()
        elif tile_below == '/':
            if self.direction_name in ('left', 'right'):
                self.turn_left()
            else:
                self.turn_right()

        elif tile_below == '+':
            self.turn_cross()

        self.move()


class CartTrack:
    DIRECTIONS = {
        'v': (0, 1),
        '^': (0, -1),
        '<': (-1, 0),
        '>': (1, 0),
    }

    def __init__(self, lines):
        self.matrix = [[tile for tile in line] for line in lines]
        self.carts = self._load_carts()

    def _load_carts(self):
        carts = []
        for y, line in enumerate(self.matrix):
            for x, tile in enumerate(line):
                if tile in self.DIRECTIONS:
                    carts.append(Cart(x, y, self.DIRECTIONS[tile]))

                if tile in ('v', '^'):
                    self.matrix[y][x] = '|'

                if tile in ('<', '>'):
                    self.matrix[y][x] = '-'

        return carts

    def tick(self, remove_crashed=False):
        for cart in sorted(self.carts, key=lambda item: item.y * 1000 + item.x):
            tile = self.matrix[cart.y][cart.x]
            cart.move_for_tile(tile)

            if remove_crashed:
                self.remove_crashed()

    def get_crash(self):
        for cart in self.carts:
            for other in self.carts:
                if cart is other:
                    continue

                if cart.dist(other) == 0:
                    return cart.x, cart.y

        return None

    def remove_crashed(self):
        for cart in self.carts:
            for other in self.carts:
                if cart is other:
                    continue

                if cart.dist(other) == 0:
                    self.carts.remove(cart)
                    self.carts.remove(other)
                    break


class Day13(Day):
    def part1(self):
        track = CartTrack(self.input)

        while True:
            track.tick()

            crashed = track.get_crash()
            if crashed:
                return f'{crashed[0]},{crashed[1]}'

    def part2(self):
        track = CartTrack(self.input)

        while True:
            track.tick(True)

            if len(track.carts) == 1:
                return f'{track.carts[0].x},{track.carts[0].y}'
