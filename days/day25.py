from day import Day


class Day25(Day):
    def parse(self, content):
        return [tuple(int(i) for i in line.split(',')) for line in super().parse(content)]

    def dist(self, a, b):
        return sum([abs(point - b[i]) for i, point in enumerate(a)])

    def in_cluster(self, point, cluster):
        for other_point in cluster:
            if self.dist(point, other_point) <= 3:
                return True
        return False

    def build_clusters(self):
        clusters = []

        for point in self.input:
            added = False
            for cluster in clusters:
                if self.in_cluster(point, cluster):
                    cluster.append(point)
                    added = True
                    break

            if not added:
                clusters.append([point])
                continue

        return self.join(clusters)

    def can_join_clusters(self, a, b):
        for point_a in a:
            for point_b in b:
                if self.dist(point_a, point_b) <= 3:
                    return True
        return False

    def join(self, clusters):
        clusters = set(tuple(cluster) for cluster in clusters)
        results = []

        while clusters:
            cluster = clusters.pop()

            found = False
            for other in clusters:
                if self.can_join_clusters(cluster, other):
                    clusters.remove(other)
                    clusters.add((*cluster, *other))
                    found = True
                    break

            if not found:
                results.append(cluster)

        return results

    def part1(self):
        return len(self.build_clusters())

    def part2(self):
        return 'Merry X-Mas'
