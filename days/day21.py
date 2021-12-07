from day import Day
from days.day19 import Computer
from utils.computer import ComputerMixin, Instruction


class TheBigOne(Instruction):
    """
    coded instructions derived from input. i'd guess that there are magic numbers in the input
    so if you try to run this with your input you will probably get a wrong result (!)

    ...but i guess it's just a matter of changing the magic numbers that are used to calculate f below...
    """

    def run_operation(self, registers):
        a, b, c, d, e, f = registers

        while True:
            b = d & 255
            f = f + b
            f = f & 16777215
            f = f * 65899
            f = f & 16777215

            b = int(256 > d)
            if b:
                break

            d = d // 256

        return [a, b, c, d, e, f]


class CountComputer(Computer):
    def find_exit_condition(self):
        # since we only control registers[0], we need to find the earliest exit condition in the code
        # ...which happens to be registers[5] == registers[1]. so we can check what the first value of
        # this register is. As assembler, this has horrible performance, so the above optimization is needed.
        inst_ptr = 0

        while len(self.instructions) > inst_ptr >= 0:
            inst_ptr = self.execute_instruction(inst_ptr)
            if inst_ptr == 10:  # directly after the code block above that i called TheBigOne
                return self.registers[5]
        return None

    def find_max_loop_condition(self):
        inst_ptr = 0

        values = set()
        prev_value = None
        while len(self.instructions) > inst_ptr >= 0:
            inst_ptr = self.execute_instruction(inst_ptr)

            if inst_ptr == 9:  # directly after the code block above that i called TheBigOne
                if self.registers[5] in values:
                    return prev_value

                prev_value = self.registers[5]
                values.add(self.registers[5])

        return None


class Day21(ComputerMixin, Day):

    def parse(self, content):
        return self.parse_instructions(super().parse(content))

    def optimize(self, result):
        self.replace(result, 8, 20, TheBigOne)

    def part1(self):
        computer = CountComputer([*self.input[0]], self.input[1])
        return computer.find_exit_condition()

    def part2(self):
        computer = CountComputer([*self.input[0]], self.input[1])
        return computer.find_max_loop_condition()
