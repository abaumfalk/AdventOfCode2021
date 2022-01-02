from pathlib import Path


class Ocean:
    def __init__(self, fishes):
        self.timers = [0] * 9
        for timer in fishes:
            self.timers[timer] += 1

    def cycle(self):
        new_timers = [0] * 9

        for index, count in enumerate(self.timers[1:]):
            new_timers[index] = count

        wrap = self.timers[0]
        new_timers[8] = wrap
        new_timers[6] += wrap

        self.timers = new_timers

    def count(self):
        return sum(self.timers)


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()
    fishes = list(map(int, lines[0].split(',')))

    ocean = Ocean(fishes)

    for i in range(256):
        ocean.cycle()

    print(f"Ocean has {ocean.count()} fishes")
