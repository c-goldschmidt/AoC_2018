from collections import defaultdict

from day import Day


class Day02(Day):
    def part1(self):
        twos = 0
        threes = 0

        for line in self.input:
            count = self.count_charts(line)
            if 2 in count:
                twos += 1
            if 3 in count:
                threes += 1

        return twos * threes

    def part2(self):
        for line1 in self.input:
            for line2 in self.input:
                if line1 == line2:
                    continue

                result = self.diff(line1, line2)
                if result:
                    return result

    @staticmethod
    def count_charts(line):
        result = defaultdict(int)
        for char in line:
            result[char] += 1
        return set(result.values())

    @staticmethod
    def diff(line1, line2):
        result = ''
        diffs = 0

        for chr1, chr2 in zip(line1, line2):
            if chr1 == chr2:
                result += chr1
            else:
                diffs += 1

        return result if diffs == 1 else None
