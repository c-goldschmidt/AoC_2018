from typing import List, Tuple

from day import Day
from utils.computer import ALL_INSTRUCTIONS, Operation, Instruction, Computer, ComputerMixin


class AddIfModulo(Instruction):
    def _run_operation_original(self, registers):
        # this is what the loop identified in the assembler code does.
        a, b, c, d, e, f = registers

        while c <= e:
            if f * c == e:
                a += f
            c += 1

        return [a, b, c, d, e, f]

    def run_operation(self, registers):
        # ...and this is the same, just without the loop...
        a, b, c, d, e, f = registers

        if e % f == 0:
            a += f

        return [a, b, c, d, e, f]


class Day19(ComputerMixin, Day):
    input: Tuple[List[Instruction], int]

    def parse(self, content):
        return self.parse_instructions(super().parse(content))

    def optimize(self, result):
        # replace that modulo operation with a custom one to save a ton of time
        # i guess there could be more optimization by finding out what the outer loop does
        # ...i suspect it's calculating prime numbers? no idea tbh, as the results aren't primes...
        self.replace(result, 3, 9, AddIfModulo)

    def part1(self):
        computer = Computer([*self.input[0]], self.input[1])
        computer.run()

        return computer.registers[0]

    def part2(self):
        computer = Computer([*self.input[0]], self.input[1])
        computer.registers[0] = 1
        computer.run()

        return computer.registers[0]
