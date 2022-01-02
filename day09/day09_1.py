from pathlib import Path


class Cave:
    def __init__(self, heightmap):
        self.heightmap = heightmap
        self.rows = len(heightmap)
        self.cols = len(heightmap[0])

    def get_low_points(self):
        lows = []
        for row_index, row in enumerate(self.heightmap):
            for col_index, height in enumerate(row):
                neighbours = self.get_neighbours(row_index, col_index)
                if all(n > height for n in neighbours):
                    lows.append(height)
        return lows

    def get_neighbours(self, row, col):
        ns = []
        if row > 0:
            ns.append(self.heightmap[row - 1][col])
        if col > 0:
            ns.append(self.heightmap[row][col-1])
        if row < self.rows - 1:
            ns.append(self.heightmap[row + 1][col])
        if col < self.cols - 1:
            ns.append(self.heightmap[row][col + 1])
        return ns

    def get_risk(self):
        low_points = self.get_low_points()
        risk = sum([p + 1 for p in low_points])
        return risk


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()
    heightmap = [list(map(int, line)) for line in lines]

    cave = Cave(heightmap)
    risk = cave.get_risk()

    print(f"result: {risk}")
