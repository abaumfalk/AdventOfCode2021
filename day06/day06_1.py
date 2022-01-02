from pathlib import Path


class Ocean:
    def __init__(self, fishes):
        self.fishes = fishes

    def cycle(self):
        new_fishes = []
        for fish in self.fishes:
            new = fish.cycle()
            if new is not None:
                new_fishes.append(new)
        self.fishes += new_fishes


class LanternFish:
    def __init__(self, initial_timer):
        self.timer = initial_timer

    def cycle(self):
        if self.timer == 0:
            self.timer = 6
            return LanternFish(8)
        self.timer -= 1


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()
    initials = map(int, lines[0].split(','))

    fishes = [LanternFish(i) for i in initials]
    ocean = Ocean(fishes)

    for _ in range(80):
        ocean.cycle()

    print(f"Ocean has {len(ocean.fishes)} fishes")

