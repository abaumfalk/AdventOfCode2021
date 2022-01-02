from pathlib import Path
from typing import List, Tuple


class Submarine:
    def __init__(self, position=0, depth=0, aim=0):
        self.position = position
        self.depth = depth
        self.aim = aim

    def move(self, command, value):
        if command == "forward":
            self.position += value
            self.depth += self.aim * value
        elif command == "down":
            self.aim += value
        elif command == "up":
            self.aim -= value

    def product(self):
        return self.depth * self.position


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()

    submarine = Submarine()
    for line in lines:
        command, value = line.split()
        submarine.move(command, int(value))

    print(f"result: {submarine.product()}")
