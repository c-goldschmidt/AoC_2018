import copy
import re

from day import Day
from utils.timer import Timer

rx_units = r''

rx_groups = re.compile(
    r'(?P<unit_count>\d+) units.+?(?P<hit_points>\d+) hit[^(\n]+'
    r'(?:\((?P<modifiers>[^)]+)\))? '
    r'with.+?(?P<attack_damage>\d+) (?P<damage_type>.+) damage at initiative (?P<initiative>\d+)'
)

rx_weak = re.compile('weak to (?P<weaknesses>[^;]+)')
rx_immune = re.compile('immune to (?P<immunities>[^;]+)')


class BattleGroup:
    def __init__(self, army, line):
        self.units = 0
        self.hit_points = 0
        self.immunities = []
        self.weaknesses = []
        self._attack_damage = 0
        self.damage_type = ''
        self.initiative = 0
        self.from_line(line)

        self.army = army
        self.boost = 0
        self.line = line
        self.id = self.army.id
        self.target = None

    @property
    def attack_damage(self):
        return self._attack_damage + self.boost

    def clone(self, army):
        return BattleGroup(army, self.line)

    def from_line(self, line):
        match = rx_groups.match(line)
        if not match:
            print(line)
            raise ValueError('could not match group')

        self.units = int(match.group('unit_count'))
        self.hit_points = int(match.group('hit_points'))
        self._attack_damage = int(match.group('attack_damage'))
        self.damage_type = match.group('damage_type')
        self.initiative = int(match.group('initiative'))

        modifiers = match.group('modifiers')
        if modifiers:
            match = rx_immune.search(modifiers)
            if match:
                self.immunities = match.group('immunities').split(', ')

            match = rx_weak.search(modifiers)
            if match:
                self.weaknesses = match.group('weaknesses').split(', ')

    def __repr__(self):
        return (
            f'BattleGroup ({self.id} {self.units} @ {self.hit_points}'
            f' immune={self.immunities} weak={self.weaknesses} dmg={self.attack_damage} ({self.damage_type})'
            f' init={self.initiative}'
            f' effective={self.effective_power}, boost={self.boost})'
        )

    def select_target(self, available):
        self.target = None

        can_attack = [avail for avail in available if avail.army != self.army]
        if not can_attack:
            return

        candidates = sorted(
            can_attack,
            key=lambda x: (x.calc_damage(self.effective_power, self.damage_type), x.effective_power, x.initiative),
            reverse=True,
        )

        if not candidates[0].calc_damage(self.effective_power, self.damage_type):
            return

        self.target = candidates[0]
        available.remove(candidates[0])

    def attack(self):
        if not self.target or self.units <= 0:
            return 0

        return self.target.receive_damage(self.effective_power, self.damage_type)

    @property
    def effective_power(self):
        return self.units * self.attack_damage

    def calc_damage(self, damage, dmg_type):
        if dmg_type in self.immunities:
            return 0

        if dmg_type in self.weaknesses:
            return damage * 2

        return damage

    def receive_damage(self, damage, dmg_type):
        damage = self.calc_damage(damage, dmg_type)
        if not damage or not self.units:
            return 0

        kills = min(damage // self.hit_points, self.units)
        self.units -= kills
        return kills


class Army:
    def __init__(self, content=None):
        self.name = ''
        self.groups = []
        self._groups = []
        self._id = 0

        if content:
            self.from_content(content)

    @property
    def id(self):
        self._id += 1
        return f'{self.name}.{self._id}'

    def boost(self, boost):
        for group in self.groups:
            group.boost = boost

    def clone(self):
        new_army = Army()
        new_army.name = self.name
        new_army.groups = [g.clone(new_army) for g in self._groups]
        return new_army

    def __repr__(self):
        groups = '\n '.join([repr(g) for g in self.groups])
        return f'{self.name} \n {groups}'

    def from_content(self, content):
        self.name = content[0][:-1]
        self.groups = []

        for line in content[1:]:
            self.groups.append(BattleGroup(self, line))

        self._groups = [*self.groups]

    @property
    def unit_count(self):
        return sum([g.units for g in self.groups])

    def fight(self, other: 'Army'):
        all_groups = [*self.groups, *other.groups]

        # find targets
        select_order = sorted(all_groups, key=lambda g: (g.effective_power, g.initiative), reverse=True)
        # print([(g.effective_power, g.initiative, g.hit_points) for g in select_order])

        available = set(all_groups)
        for group in select_order:
            group.select_target(available)

        # attack
        attack_order = sorted(all_groups, key=lambda g: g.initiative, reverse=True)

        total_deaths = 0
        for group in attack_order:
            total_deaths += group.attack()

        # clean up
        self.groups = [group for group in self.groups if group.units > 0]
        other.groups = [group for group in other.groups if group.units > 0]

        return total_deaths


class BattleSimulation:
    def __init__(self, armies):
        self.armies = [*armies]

    def __repr__(self):
        armies = '\n\n'.join([repr(army) for army in self.armies])
        return f'BattleSim: \n\n{armies}'

    def reset(self):
        self.armies = [
            self.armies[0].clone(),
            self.armies[1].clone(),
        ]

    def run(self):
        while True:
            deaths = self.armies[0].fight(self.armies[1])

            if deaths == 0:
                # draw
                return None

            if not self.armies[0].groups:
                return self.armies[1]

            if not self.armies[1].groups:
                return self.armies[0]

            #print(self)


class Day24(Day):

    def parse(self, content):
        armies = content.split('\n\n')

        result = []
        for army in armies:
            result.append(Army(army.split('\n')))

        return result

    def part1(self):
        sim = BattleSimulation(copy.deepcopy(self.input))
        winner = sim.run()
        print(f'{winner.name} wins')
        return winner.unit_count

    def part2(self):
        boost = 0

        while True:
            sim = BattleSimulation(copy.deepcopy(self.input))
            sim.armies[0].boost(boost)
            winner = sim.run()

            if winner and winner.name != 'Infection':
                return winner.unit_count

            boost += 1
