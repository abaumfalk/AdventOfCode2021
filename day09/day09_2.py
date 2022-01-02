from pathlib import Path


class Cave:
    def __init__(self, heightmap):
        self.heightmap = heightmap
        self.rows = len(heightmap)
        self.cols = len(heightmap[0])

        self.low_points = None  # list low points (row, col)
        self.basin_sizes = None

    def get_low_points(self):
        if self.low_points is None:
            self.low_points = []
            for row_index, row in enumerate(self.heightmap):
                for col_index, height in enumerate(row):
                    neighbours = self.get_neighbours((row_index, col_index))
                    if all(self.heightmap[n[0]][n[1]] > height for n in neighbours):
                        self.low_points.append((row_index, col_index))
        return self.low_points

    def get_neighbours(self, point):
        row, col = point
        ns = []
        if row > 0:
            ns.append((row-1, col))
        if col > 0:
            ns.append((row, col-1))
        if row < self.rows - 1:
            ns.append((row + 1, col))
        if col < self.cols - 1:
            ns.append((row, col + 1))
        return ns

    def get_risk(self):
        low_points = self.get_low_points()
        risk = sum([self.heightmap[row][col] + 1 for row, col in low_points])
        return risk

    def get_basin_sizes(self):
        if self.basin_sizes is None:
            self.basin_sizes = []
            for point in self.low_points:
                self.basin_sizes.append(self.get_basin_size(point))
        return self.basin_sizes

    def get_basin_size(self, point):
        points = set()

        def add(p):
            if p not in points:
                points.add(p)
                ns = self.get_neighbours(p)
                for row, col in ns:
                    if heightmap[row][col] != 9:
                        add((row, col))

        add(point)
        return len(points)

    def get_basin_factor(self):
        sizes = sorted(self.get_basin_sizes())
        result = sizes[-1] * sizes[-2] * sizes[-3]
        return result


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()
    heightmap = [list(map(int, line)) for line in lines]

    cave = Cave(heightmap)
    risk = cave.get_risk()

    print(f"risk: {risk}")

    factor = cave.get_basin_factor()
    print(f"basin factor: {factor}")
