from pathlib import Path


class CrabOptimizer:
    def __init__(self, crabs):
        self.crabs = crabs
        self.opt_fuel, self.opt_pos = None, None

    def optimize(self):
        start = min(self.crabs)
        end = max(self.crabs)
        self.opt_pos, self.opt_fuel = start, self.get_fuel(start)

        for pos in range(start + 1, end + 1):
            fuel = self.get_fuel(pos)
            if fuel < self.opt_fuel:
                self.opt_pos, self.opt_fuel = pos, fuel

        return self.opt_pos, self.opt_fuel

    def get_fuel(self, pos):
        return sum(self.fuel_for_steps(abs(pos - c)) for c in self.crabs)

    @staticmethod
    def fuel_for_steps(steps):
        return steps * (steps + 1) / 2


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()
    crab_positions = list(map(int, lines[0].split(',')))

    crab_optimizer = CrabOptimizer(crab_positions)
    p, f = crab_optimizer.optimize()

    print(f"Crabs should align at {p}, using {f} fuel")
