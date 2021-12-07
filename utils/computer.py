from typing import List


class Operation:
    def __init__(self, raw):
        split = raw.split(' ')

        try:
            self.opcode = int(split[0])
        except ValueError:
            self.opcode = None

        self.in_a = int(split[1])
        self.in_b = int(split[2])
        self.out = int(split[3])

    def __repr__(self):
        return f'{self.opcode}: {self.in_a} / {self.in_b} / {self.out}'


class Instruction:
    op = '??'
    a_from_register = None
    b_from_register = None

    def __init__(self, operation: Operation = None):
        self.operation = operation

    def _format_registers(self):
        names = 'ABCDEF'
        a = names[self.operation.in_a] if self.a_from_register else self.operation.in_a
        b = names[self.operation.in_b] if self.b_from_register else self.operation.in_b
        out = names[self.operation.out]
        return a, b, out

    def _format_params(self):
        a, b, out = self._format_registers()
        return f'{a} {self.op} {b} => {out}'

    def __repr__(self):
        params = ''
        if self.operation:
            params = self._format_params()
        return f'{self.__class__.__name__}({params})'

    def run_operation(self, registers):
        result = [*registers]
        self.run_on_register(
            result,
            self.operation.in_a,
            self.operation.in_b,
            self.operation.out,
        )
        return result

    def run_on_register(self, register, in_a, in_b, out):
        register[out] = self.execute(register, in_a, in_b)

    def _a(self, registers, in_a):
        if self.a_from_register:
            return registers[in_a]
        return in_a

    def _b(self, registers, in_b):
        if self.b_from_register:
            return registers[in_b]
        return in_b

    def execute(self, registers, in_a, in_b):
        raise NotImplementedError


class Add(Instruction):
    op = '+'
    a_from_register = True

    def execute(self, registers, in_a, in_b):
        return self._a(registers, in_a) + self._b(registers, in_b)


class Mul(Instruction):
    op = '*'
    a_from_register = True

    def execute(self, registers, in_a, in_b):
        return self._a(registers, in_a) * self._b(registers, in_b)


class And(Instruction):
    op = '&'
    a_from_register = True

    def execute(self, registers, in_a, in_b):
        return self._a(registers, in_a) & self._b(registers, in_b)


class Or(Instruction):
    op = '|'
    a_from_register = True

    def execute(self, registers, in_a, in_b):
        return self._a(registers, in_a) | self._b(registers, in_b)


class Set(Instruction):
    op = 'SET'

    def _format_params(self):
        a, b, out = self._format_registers()
        return f'SET {a} => {out}'

    def execute(self, registers, in_a, in_b):
        return self._a(registers, in_a)


class Greater(Instruction):
    op = '>'

    def execute(self, registers, in_a, in_b):
        return 1 if self._a(registers, in_a) > self._b(registers, in_b) else 0


class Equal(Instruction):
    op = '=='

    def execute(self, registers, in_a, in_b):
        return 1 if self._a(registers, in_a) == self._b(registers, in_b) else 0


class AddR(Add):
    b_from_register = True


class AddI(Add):
    b_from_register = False


class MulR(Mul):
    b_from_register = True


class MulI(Mul):
    b_from_register = False


class BAnR(And):
    b_from_register = True


class BAnI(And):
    b_from_register = False


class BOrR(Or):
    b_from_register = True


class BOrI(Or):
    b_from_register = False


class SetR(Set):
    a_from_register = True


class SetI(Set):
    a_from_register = False


class GTIR(Greater):
    a_from_register = False
    b_from_register = True


class GTRI(Greater):
    a_from_register = True
    b_from_register = False


class GTRR(Greater):
    a_from_register = True
    b_from_register = True


class EqIR(Equal):
    a_from_register = False
    b_from_register = True


class EqRI(Equal):
    a_from_register = True
    b_from_register = False


class EqRR(Equal):
    a_from_register = True
    b_from_register = True


class NoOp (Instruction):
    def run_operation(self, registers):
        return registers


ALL_INSTRUCTIONS = [
    AddR, AddI,
    MulR, MulI,
    BAnR, BAnI,
    BOrR, BOrI,
    SetR, SetI,
    GTIR, GTRI, GTRR,
    EqIR, EqRI, EqRR,
]


class Computer:

    def __init__(self, instructions: List[Instruction], reg_ptr):
        self.reg_ptr = reg_ptr
        self.instructions = instructions
        self.registers = [0, 0, 0, 0, 0, 0]

    def run(self):
        inst_ptr = 0

        while len(self.instructions) > inst_ptr >= 0:
            inst_ptr = self.execute_instruction(inst_ptr)

    def execute_instruction(self, inst_ptr):
        instruction = self.instructions[inst_ptr]
        self.registers[self.reg_ptr] = inst_ptr
        self.registers = instruction.run_operation(self.registers)
        inst_ptr = self.registers[self.reg_ptr]
        return inst_ptr + 1


class ComputerMixin:
    instructions_by_name = {k.__name__.lower(): k for k in ALL_INSTRUCTIONS}

    def parse_instructions(self, instructions):
        result = []
        reg_ptr = None

        for line in instructions:
            if line[0] == '#':
                value = line.split(' ')[1]
                reg_ptr = int(value)
            else:
                key = line.split(' ')[0]
                result.append(self.instructions_by_name[key](Operation(line)))

        self.optimize(result)
        return result, reg_ptr

    def optimize(self, result):
        pass

    def replace(self, result, index, end_index, new_operation):
        result[index] = new_operation()

        for i in range(index + 1, index + end_index):
            result[i] = NoOp()
