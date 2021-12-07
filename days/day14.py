from day import Day


class Day14(Day):
    def parse(self, content):
        return content

    @staticmethod
    def _next(results, elves_at):
        e1 = results[elves_at[0]]
        e2 = results[elves_at[1]]
        added = str(e1 + e2)
        results += [int(x) for x in added]
        elves_at[0] = (elves_at[0] + 1 + e1) % len(results)
        elves_at[1] = (elves_at[1] + 1 + e2) % len(results)
        return len(added)

    def part1(self):
        results = [3, 7]
        elves_at = [0, 1]
        as_int = int(self.input)
        for i in range(as_int + 10):
            self._next(results, elves_at)

        return ''.join([str(results[(as_int + i) % len(results)]) for i in range(10)])

    def part2(self):
        results = [3, 7]
        elves_at = [0, 1]

        # note: for my input this was 15mio loops...
        while True:
            added = self._next(results, elves_at)

            res = ''.join([str(x) for x in results[-(len(self.input) + (-1 + added)):]])
            if self.input in res:
                if res.endswith(self.input):
                    return len(results) - len(self.input)
                else:
                    return len(results) - (len(self.input) + 1)
