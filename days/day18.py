from day import Day
from utils.grid import Grid


class Orchard(Grid):

    def tick(self):
        copy = self.clone()

        for point in self.iter_points():
            num_trees = 0
            num_yards = 0

            for other in point.neighbors(True):
                symbol = copy[other]
                num_trees += int(symbol == '|')
                num_yards += int(symbol == '#')

            symbol = copy[point]
            if symbol == '.' and num_trees >= 3:
                self[point] = '|'

            if symbol == '|' and num_yards >= 3:
                self[point] = '#'

            if symbol == '#' and (num_yards < 1 or num_trees < 1):
                self[point] = '.'

    def hash(self):
        return hash(tuple(self[point] for point in self.iter_points()))

    def count(self, symbol):
        return len([p for p in self.iter_points() if self[p] == symbol])

    def value(self):
        yard = tree = 0
        for val in self.iter_values():
            yard += int(val == '#')
            tree += int(val == '|')
        return yard * tree


class Day18(Day):
    input: Orchard

    def parse(self, content):
        parsed = Orchard()

        for y, line in enumerate(super().parse(content)):
            for x, col in enumerate(line):
                parsed[(x, y)] = col

        return parsed

    def part1(self):
        copy = self.input.clone()

        for i in range(1, 11):
            copy.tick()

        return copy.count('#') * copy.count('|')

    def part2(self):
        copy = self.input.clone()
        hashes = set()
        value_at = {}
        index_by_hash = {}

        target = 1_000_000_000
        repeat_at = 0
        seq_start = 0

        for i in range(target):
            if i > 0:
                # just in case the sequence starts at 0, we add the hash of the 0 frame to our collection
                # not that this is at all likely...
                copy.tick()

            state_hash = copy.hash()

            value_at[i] = copy.value()

            if state_hash in hashes:
                repeat_at = i
                seq_start = index_by_hash[state_hash]
                break

            index_by_hash[state_hash] = i
            hashes.add(state_hash)

        seq_len = repeat_at - seq_start
        fill_len = (target - seq_start) // seq_len
        fill_to = seq_start + fill_len * seq_len
        remaining = target - fill_to
        return value_at[seq_start + remaining]
