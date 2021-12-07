from day import Day


class Day01(Day):

    def part1(self):
        total = 0
        for line in self.input:
            mul = 1 if line[0] == '+' else -1
            total += mul * int(line[1:])
        return total

    def part2(self):
        encountered = {0}
        current = 0

        while True:
            for line in self.input:
                mul = 1 if line[0] == '+' else -1
                current += mul * int(line[1:])

                if current in encountered:
                    return current

                encountered.add(current)
