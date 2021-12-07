import os.path

from utils.timer import Timer


class Day:
    def __init__(self):
        self.input = self._load()

    def parse(self, content):
        return content.split('\n')

    def part1(self):
        raise NotImplementedError()

    def part2(self):
        return 'Not (yet) implemented'

    def run(self):
        print(f'=== {self.__class__.__name__} ===')
        with Timer():
            result = self.part1()
        print(f'Part 1 result: {result}')

        with Timer():
            result = self.part2()
        print(f'Part 2 result: {result}\n')

    def _load(self):
        file_name = f'inputs/{self.__class__.__name__.lower()}.txt'
        if not os.path.isfile(f'inputs/{self.__class__.__name__.lower()}.txt'):
            raise ValueError(f'Missing input file "{file_name}"')

        with open(file_name, 'r') as f:
            return self.parse(f.read())
