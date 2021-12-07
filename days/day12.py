from collections import defaultdict

from day import Day


class Pots:
    def __init__(self, initial_state, state_map):
        self.state = defaultdict(lambda: '.')
        for i in range(len(initial_state)):
            self.state[i] = initial_state[i]
        self.state_map = state_map

    def range_string(self, pivot):
        result = self.state[pivot - 2]
        result += self.state[pivot - 1]
        result += self.state[pivot]
        result += self.state[pivot + 1]
        result += self.state[pivot + 2]
        return result

    def apply(self):
        indices = list(sorted(self.state.keys()))

        next_state = defaultdict(lambda: '.')
        for index in range(indices[0] - 2, indices[-1] + 2):
            next_state[index] = self.state_map.get(self.range_string(index), '.')

        self.state = next_state

    def get_active(self):
        return [key for key, value in self.state.items() if value == '#']

    def minmax(self):
        active = self.get_active()
        min_index = min(active)
        max_index = max(active)

        indices = list(sorted(self.state.keys()))
        for index in indices:
            if index < min_index or index > max_index:
                del self.state[index]

    def sum(self):
        return sum([key for key, value in self.state.items() if value == '#'])


class Day12(Day):

    def parse(self, content):
        lines = super().parse(content)
        init = lines[0].replace('initial state: ', '')
        changes = [line.split(' => ') for line in lines[2:]]

        return init, {cng[0]: cng[1] for cng in changes}

    def part1(self):
        pots = Pots(self.input[0], self.input[1])

        for generation in range(20):
            pots.apply()
            pots.minmax()

        return pots.sum()

    def part2(self):
        pots = Pots(self.input[0], self.input[1])
        pots.minmax()

        prev = None
        target = 50_000_000_000 - 1

        for generation in range(target):
            pots.apply()
            pots.minmax()
            active = tuple(pots.get_active())

            if self._is_stable(prev, active):
                steps_to_end = target - generation
                return pots.sum() + steps_to_end * len(active)

            prev = active
        return None

    @staticmethod
    def _is_stable(prev, active):
        if not prev or len(prev) != len(active):
            return

        return all((active[index] -1 == prev[index] for index in range(len(active))))
