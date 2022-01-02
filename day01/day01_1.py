from pathlib import Path
from typing import List, Tuple


class Depth:
    def __init__(self, depths):
        self.depths = list(depths)

    def get_increased(self):
        result = 0
        for i in range(len(self.depths) - 1):
            if self.depths[i + 1] > self.depths[i]:
                result += 1

        return result


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()
    data = map(int, lines)

    depth = Depth(data)

    print(f"number of increases: {depth.get_increased()}")
