from collections import defaultdict

from day import Day
from utils.point import UniquePoint
from utils.timer import Timer

WALL = 'wall'


class CombatEnd(Exception):
    def __init__(self, unit):
        self.unit = unit


class DeadElf(Exception):
    pass


class Unit(UniquePoint):

    def __init__(self, x, y, is_good, battlefield):
        super().__init__(x, y)

        self.is_good = is_good
        self.name = 'Elf' if is_good else 'Gob'
        self.battlefield = battlefield
        self.atk = 3
        self.hp = 200

    def run_turn(self):
        targets = self.find_targets()
        if not targets:
            raise CombatEnd(self)

        if self.try_attack(targets):
            return

        spots_in_range = self.in_range(targets)
        if not spots_in_range or not self.battlefield.next_possible(self):
            return

        nearest = self.nearest(spots_in_range)
        if not nearest:
            return

        chosen_step = self.choose_step(nearest)
        if not chosen_step:
            return

        self.move_to(chosen_step)
        self.try_attack(targets)

    def try_attack(self, targets):
        can_attack = self.can_attack(targets)
        if can_attack:
            can_attack[0].hp -= self.atk
            if can_attack[0].hp <= 0:
                self.battlefield.kill(can_attack[0])
        return bool(can_attack)

    def move_to(self, target):
        self.battlefield.field[target.y][target.x] = self
        self.battlefield.field[self.y][self.x] = None
        self.y = target.y
        self.x = target.x

    def find_targets(self):
        return [unit for unit in self.battlefield.units if unit.is_good != self.is_good]

    def can_attack(self, targets):
        possible = [target for target in targets if target.dist(self) == 1]
        if not possible:
            return

        return sorted(
            [target for target in targets if target.dist(self) == 1],
            key=lambda target: (target.hp, target.y, target.x)
        )

    def in_range(self, targets):
        result = []
        for target in targets:
            result += target.range()
        return set(result)

    def nearest(self, points):
        paths = defaultdict(list)
        for point in points:
            path = self.battlefield.find_shortest_path(self, point)
            if not path:
                continue
            paths[len(path)].append(point)

        if not paths:
            return []

        paths = sorted(paths.items(), key=lambda item: item[0])
        return self.battlefield.reading_order(paths[0][1])[0]

    def choose_step(self, point):
        at_min_dist = defaultdict(list)
        for option in self.battlefield.next_possible(self):
            path = self.battlefield.find_shortest_path(option, point)
            if not path:
                continue

            at_min_dist[len(path)].append(option)

        if not at_min_dist:
            return None

        at_min_dist = sorted(at_min_dist.items(), key=lambda item: item[0])
        return self.battlefield.reading_order(at_min_dist[0][1])[0]

    def range(self):
        return self.battlefield.next_possible(self)


class Battlefield:
    def __init__(self, data, elf_attack=3):
        self._data = data
        self.units = []
        self.field = []
        self.elf_attack = elf_attack
        self.raise_on_dead_elf = False
        self.parse(data)

    def clone(self, elf_attack=3):
        return Battlefield(self._data, elf_attack)

    def parse(self, data):
        for y, line in enumerate(data):
            self.field.append([])
            for x, tile in enumerate(line):
                if tile in ('G', 'E'):
                    parsed = Unit(x, y, tile == 'E', self)
                    if parsed.is_good:
                        parsed.atk = self.elf_attack

                    self.units.append(parsed)
                elif tile == '#':
                    parsed = WALL
                elif tile == '.':
                    parsed = None
                else:
                    raise ValueError(f'WTF is "{tile}"??')

                self.field[-1].append(parsed)

    def print(self):
        frame = ''
        for line in self.field:
            rep = ''
            units = ''
            for col in line:
                rep += self._symbol(col)
                if isinstance(col, Unit):
                    units += f'{self._symbol(col)} ({col.hp})   '
            frame += rep + '  => ' + units + '\n'
        return frame

    def kill(self, unit):
        self.units.remove(unit)
        self.field[unit.y][unit.x] = None

        if unit.is_good and self.raise_on_dead_elf:
            raise DeadElf

    def _symbol(self, col):
        if isinstance(col, Unit):
            return 'E' if col.is_good else 'G'
        elif col == WALL:
            return '#'
        else:
            return '.'

    @property
    def stats(self):
        elfs = [u for u in self.units if u.is_good]
        goblins = [u for u in self.units if not u.is_good]

        elf_hp = sum([u.hp for u in elfs])
        gob_hp = sum([u.hp for u in goblins])

        return f'Elfs: {len(elfs)} @ {elf_hp}, Goblins: {len(goblins)} @ {gob_hp}'

    @property
    def survivor_hp(self):
        return sum(u.hp for u in self.units)

    def tick(self):
        order = list(self.reading_order(self.units))
        for unit in order:
            if unit.hp <= 0:
                # already died before they had the chance to fight and they aren't zombies
                continue
            unit.run_turn()

    def next_possible(self, start):
        points = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        free = []
        for x, y in points:
            result = self.field[start.y + y][start.x + x]
            if result is None:
                free.append(UniquePoint(start.x + x, start.y + y))
        return free

    @staticmethod
    def reading_order(points):
        return sorted(points, key=lambda point: (point.y, point.x))

    def _rollback(self, prev, end):
        if end not in prev:
            return [end]
        return self._rollback(prev, prev[end]) + [end]

    def find_shortest_path(self, start, end):
        prev = {}
        g_score = {}
        f_score = {}
        queue = [start]

        g_score[start] = 0
        f_score[start] = start.dist(end)

        while len(queue) > 0:
            current = list(sorted(queue, key=lambda p: f_score[p]))[0]

            if current == end:
                return self._rollback(prev, end)

            queue.remove(current)
            for next_point in self.next_possible(current):
                next_score = g_score[current] + 1
                if next_point not in g_score or next_score < g_score[next_point]:
                    prev[next_point] = current
                    g_score[next_point] = next_score
                    f_score[next_point] = g_score[next_point] + next_point.dist(end)

                    if next_point not in queue:
                        queue.append(next_point)

        return None


class Day15(Day):
    input: Battlefield

    def parse(self, content):
        return Battlefield(super().parse(content))

    def run_combat(self, board=None):
        if not board:
            board = self.input

        completed_rounds = 0
        try:
            while True:
                board.tick()
                completed_rounds += 1
        except DeadElf:
            return None
        except CombatEnd:
            return board.survivor_hp * completed_rounds

    def part1(self):
        return self.run_combat()

    def part2(self):
        # takes forever, because my search algo isn't quite optimal
        elf_atk = 4

        while True:
            new_board = self.input.clone(elf_atk)
            new_board.raise_on_dead_elf = True
            result = self.run_combat(new_board)
            if result:
                return result
            elf_atk += 1
