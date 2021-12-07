from day import Day


class TreeNode:
    def __init__(self, data):
        self.num_child = data[0]
        self.num_meta = data[1]

        data[:] = data[2:]
        self.children = []
        for _ in range(self.num_child):
            self.children.append(TreeNode(data))

        self.meta = data[:self.num_meta]
        data[:] = data[self.num_meta:]

    def meta_sum(self):
        return sum([*self.meta, *[child.meta_sum() for child in self.children]])

    @property
    def value(self):
        if self.children:
            result = 0
            for item in self.meta:
                if item - 1 < len(self.children):
                    result += self.children[item - 1].value
            return result
        return sum(self.meta)


class Day08(Day):
    def parse(self, content):
        return TreeNode([int(d) for d in content.split(' ')])

    def part1(self):
        return self.input.meta_sum()

    def part2(self):
        return self.input.value
