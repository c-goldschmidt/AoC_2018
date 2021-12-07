from day import Day


class PowerGrid(dict):

    def __init__(self, input_value):
        super().__init__()
        self.input = input_value
        self._cache = {}
        self._cached_sizes = []

    def __getitem__(self, item):
        result = super().get(item)
        if result is None:
            result = self._power_level(*item)
            self[item] = result
        return result

    def _power_level(self, x, y):
        rack_id = x + 10
        power_level = rack_id * y

        power_level += self.input
        power_level = power_level * rack_id

        result = int(str(power_level)[-3]) - 5
        return result

    def _total(self, start_x, start_y, size=3):
        cached = self._cache.get((start_x, start_y, size - 1))
        if cached is not None:
            result = cached
            size_off = size - 1
            for offset in range(size_off):
                result += self[(start_x + size_off, start_y + offset)]
                result += self[(start_x + offset, start_y + size_off)]

            result += self[(start_x + size_off, start_y + size_off)]

            self._cache[(start_x, start_y, size)] = result
            return result

        sum = 0
        for y in range(start_y, start_y + size):
            for x in range(start_x, start_x + size):
                sum += self[(x, y)]

        self._cache[(start_x, start_y, size)] = sum
        return sum

    # for bigger sizes, we sum up the biggest sub-grids
    def _total_mod(self, start_x, start_y, size):
        checker_size = self._find_checker_size(size)
        if not checker_size and ((size - 1) // 2 not in self._cached_sizes):
            return self._total(start_x, start_y, size)
        elif not checker_size:
            return self._total_prime(start_x, start_y, size)

        checkers = size // checker_size
        result = 0
        for x_chk in range(checkers):
            for y_chk in range(checkers):
                x = start_x + x_chk * checker_size
                y = start_y + y_chk * checker_size
                result += self._cache[(x, y, checker_size)]

        self._cache[(start_x, start_y, size)] = result
        return result

    # ...which doesn't work for primes...
    def _total_prime(self, start_x, start_y, size):
        part_a = (size - 1) // 2
        part_b = part_a + 1

        result = self._cache[(start_x, start_y, part_a)]
        result += self._cache[(start_x + part_a, start_y, part_b)]
        result += self._cache[(start_x, start_y + part_a, part_b)]
        result += self._cache[(start_x + part_b, start_y + part_b, part_a)]
        result -= self._cache[(start_x + part_a, start_y + part_a, 1)]

        self._cache[(start_x, start_y, size)] = result
        return result

    def _find_checker_size(self, size):
        for cached in reversed(self._cached_sizes):
            if cached == 1:
                continue

            if size % cached == 0:
                return cached

        return None

    def find_square(self, size):
        totals = {}

        for y in range(1, 301 - size):
            for x in range(1, 301 - size):
                totals[(x, y)] = self._total_mod(x, y, size)

        self._cached_sizes.append(size)
        totals = sorted(totals.items(), key=lambda item: item[1], reverse=True)
        return totals[0]


class Day11(Day):

    def parse(self, content):
        return int(content)

    def part1(self):
        grid = PowerGrid(self.input)
        coord, value = grid.find_square(3)
        return ','.join([str(i) for i in coord])

    def part2(self):
        grid = PowerGrid(self.input)

        best_value = 0
        best_coord = None
        best_size = None

        for size in range(1, 300):
            coord, value = grid.find_square(size)
            if value > best_value:
                best_value = value
                best_coord = coord
                best_size = size

        return ','.join([str(i) for i in best_coord] + [str(best_size)])
