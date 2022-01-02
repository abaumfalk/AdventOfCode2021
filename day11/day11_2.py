from pathlib import Path


class DumboOctopus:
    def __init__(self, grid):
        self.grid = grid
        self.size = len(grid)
        self.flashes = 0
        self.counter = 0
        self.all_flash = []

    def step(self):
        self.counter += 1

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
        all_flashed = True
        for row, line in enumerate(self.grid):
            for col in range(len(line)):
                if line[col] > 9:
                    line[col] = 0
                else:
                    all_flashed = False

        return all_flashed

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

    def get_all_flush(self):
        while not self.step():
            pass
        return self.counter


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()

    rows = [list(map(int, line)) for line in lines]
    dumbo_octopus = DumboOctopus(rows)

    print(f"All flashed at: {dumbo_octopus.get_all_flush()}")
