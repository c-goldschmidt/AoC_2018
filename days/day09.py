import re
from collections import defaultdict

from day import Day


rx_input = re.compile(r'(?P<players>\d+) players; last marble is worth (?P<max_marble>\d+) points')


class Marble:
    def __init__(self, value):
        self.value = value
        self.prev = self
        self.next = self

    def search_next(self, steps):
        if steps == 0:
            return self

        return self.next.search_next(steps - 1)

    def search_prev(self, steps):
        if steps == 0:
            return self

        return self.prev.search_prev(steps - 1)

    def insert_after(self, marble):
        marble.next = self.next
        marble.prev = self

        self.next.prev = marble
        self.next = marble

    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev

    def print(self, start=None):
        if start and self.value == start.value:
            return ''

        if not start:
            start = self

        return str(self.value) + ' ' + self.next.print(start)


class Day09(Day):

    def parse(self, content):
        result = rx_input.search(content)
        return int(result.group('players')), int(result.group('max_marble'))

    def run_for(self, players, marbles):
        current = Marble(0)
        current_val = 0

        player_accounts = defaultdict(int)
        player = 0

        while current_val < marbles:
            current_val += 1
            player += 1
            if player > players:
                player = 1

            new = Marble(current_val)
            if current_val and current_val % 23 == 0:
                player_accounts[player] += current_val

                remove = current.search_prev(7)
                player_accounts[player] += remove.value
                current = remove.next
                remove.remove()
            else:
                current.next.insert_after(new)
                current = new

        return max(player_accounts.values())

    def part1(self):
        players, max_marbles = self.input
        return self.run_for(players, max_marbles)

    def part2(self):
        players, max_marbles = self.input
        return self.run_for(players, max_marbles * 100)
