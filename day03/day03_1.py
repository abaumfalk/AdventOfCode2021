from pathlib import Path
from typing import List, Tuple


class Submarine:
    def __init__(self, data):
        self.data = data
        self.data_len = len(data)
        self.word_len = len(self.data[0])

    def gamma(self):
        result = ""
        for i in range(self.word_len):
            ones = 0
            for d in self.data:
                if d[i] == "1":
                    ones += 1
            if ones > self.data_len / 2:
                result += "1"
            else:
                result += "0"
        return result

    def power(self):
        gamma = int(self.gamma(), 2)
        epsilon = gamma ^ (2 ** self.word_len - 1)
        return gamma * epsilon


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()

    submarine = Submarine(lines)

    print(f"result: {submarine.power()}")
