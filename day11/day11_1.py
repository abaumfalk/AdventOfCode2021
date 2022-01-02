from pathlib import Path


class DumboOctopus:
    def __init__(self, grid):
        self.grid = grid
        self.size = len(grid)
        self.flashes = 0

    def step(self):
        flashes = []
        # increase all energy levels by 1
        for row, line in enumerate(self.grid):
            for col in range(len(line)):
                line[col] += 1
                if line[col] > 9:
                    flashes.append((row, col))
                    self.flashes += 1

        while flashes:
            flashes_new = []
            for row, col in flashes:
                adjacent = self.get_adjacent(row, col)
                for adj_row, adj_col in adjacent:
                    self.grid[adj_row][adj_col] += 1
                    if self.grid[adj_row][adj_col] == 10:
                        flashes_new.append((adj_row, adj_col))
                        self.flashes += 1
            flashes = flashes_new

        # set flashed to 0
        for row, line in enumerate(self.grid):
            for col in range(len(line)):
                if line[col] > 9:
                    line[col] = 0
        pass

    def steps(self, count):
        for _ in range(count):
            self.step()

    def get_adjacent(self, row, col):
        adjacent = []
        for r in range(max(row - 1, 0), min(row + 2, self.size)):
            if r > self.size:
                continue
            for c in range(max(col - 1, 0), min(col + 2, self.size)):
                if r == row and c == col:
                    continue
                adjacent.append((r, c))
        return adjacent


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()

    rows = [list(map(int, line)) for line in lines]
    dumbo_octopus = DumboOctopus(rows)
    dumbo_octopus.steps(100)

    print(f"Flashes: {dumbo_octopus.flashes}")
