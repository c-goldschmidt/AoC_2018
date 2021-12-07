import re

from day import Day

rx_step = re.compile(r'Step (?P<before>[A-Z]) must be finished before step (?P<next>[A-Z])')


class Steps:
    def __init__(self):
        self.steps = {}

    def add(self, line):
        match = rx_step.search(line)

        if match.group('next') not in self.steps:
            self.steps[match.group('next')] = []

        if match.group('before') not in self.steps:
            self.steps[match.group('before')] = []

        self.steps[match.group('next')].append(match.group('before'))

    def _chain(self, step, requires):
        prev_chain = []
        for item in sorted(requires):

            for req in self._chain(item, self.steps.get(item, [])):
                if req not in prev_chain:
                    prev_chain.append(req)

        return prev_chain + [step]

    def get_chains(self):
        chains = []
        for key, value in self.steps.items():
            chains.append(self._chain(key, value))

        chains.sort(key=lambda x: len(x))
        return chains


class Worker:

    def __init__(self):
        self.elapsed = 0
        self.total = 0
        self.step = None

    def new(self, step):
        self.elapsed = 0
        self.total = (ord(step) - 64) + 60
        self.step = step

    def tick(self):
        self.elapsed += 1

    @property
    def done(self):
        return self.elapsed >= self.total


class Day07(Day):

    def parse(self, content):
        steps = Steps()
        for line in super().parse(content):
            steps.add(line)
        return steps

    def _sim_part_1(self, chains):
        next_possible = self._get_possible(chains)

        if not next_possible:
            return []

        chosen = next_possible[0]
        self._complete_step(chains, chosen)
        return [chosen] + self._sim_part_1(chains)

    @staticmethod
    def _get_possible(chains):
        return sorted(list(set(chain[0] for chain in chains if chain)))

    @staticmethod
    def _complete_step(chains, step):
        # in-place!
        for chain in chains:
            chain[:] = [item for item in chain if item != step]

    def _sim_part_2(self, chains):
        workers = [Worker() for _ in range(5)]
        second = 0

        available = self._get_possible(chains)
        assigned = set()
        done = []

        while True:
            if all([worker.done for worker in workers]) and not available:
                return second - 1

            for worker in workers:
                if worker.done:
                    if worker.step:
                        done.append(worker.step)
                        self._complete_step(chains, worker.step)
                        available = self._get_possible(chains)
                        worker.step = None

            for worker in workers:
                if worker.done:
                    can_do = [step for step in available if step not in assigned]
                    if can_do:
                        worker.new(can_do[0])
                        assigned.add(can_do[0])

                worker.tick()
            second += 1

    def part1(self):
        return ''.join(self._sim_part_1(self.input.get_chains()))

    def part2(self):
        return self._sim_part_2(self.input.get_chains())