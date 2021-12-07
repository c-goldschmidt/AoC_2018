from collections import defaultdict
from typing import List

from day import Day
from utils.computer import Instruction, ALL_INSTRUCTIONS, Operation


class Computer:
    def __init__(self, instructions: List[Instruction]):
        self.registers = [0, 0, 0, 0]
        self.instructions = instructions

    def run(self):
        for inst in self.instructions:
            self.registers = inst.run_operation(self.registers)
        return self.registers

    def get_candidates(self, operation, before, after):
        candidates = []

        for instruction in self.instructions:
            result = [*before]
            instruction.run_on_register(
                result,
                operation.in_a,
                operation.in_b,
                operation.out,
            )

            if result == after:
                candidates.append(instruction.__class__)

        return candidates


class Day16(Day):

    def parse(self, content):
        split = content.split('\n\n\n\n')
        return split

    def iter_tests(self):
        lines = self.input[0].split('\n')

        for i in range(0, len(lines), 4):
            before = [int(x) for x in lines[i][9:-1].split(', ')]
            after = [int(x) for x in lines[i + 2][9:-1].split(', ')]
            op = Operation(lines[i + 1])
            yield op, before, after

    def iter_run(self):
        lines = self.input[1].split('\n')
        for line in lines:
            yield Operation(line)

    def part1(self):
        computer = Computer([inst() for inst in ALL_INSTRUCTIONS])

        over_three = 0
        for op, before, after in self.iter_tests():
            candidates = computer.get_candidates(op, before, after)
            over_three += 1 if len(candidates) >= 3 else 0

        return over_three

    def part2(self):
        computer = Computer([inst() for inst in ALL_INSTRUCTIONS])
        candidates = defaultdict(set)

        for op, before, after in self.iter_tests():
            candidates[op.opcode].update(computer.get_candidates(op, before, after))

        available = [*ALL_INSTRUCTIONS]
        accepted = {}
        for _ in range(len(ALL_INSTRUCTIONS)):
            if not available:
                # maybe we could determine more than one opcode in a loop and were done sooner...
                break

            for code, classes in candidates.items():
                avail_for_code = [c for c in classes if c in available]
                if len(avail_for_code) == 1:
                    accepted[code] = avail_for_code[0]
                    available.remove(avail_for_code[0])

        runner = Computer([accepted.get(op.opcode)(op) for op in self.iter_run()])
        return runner.run()[0]
