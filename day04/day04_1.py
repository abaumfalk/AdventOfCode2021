import itertools
import sys
from pathlib import Path


class Bingo:
    def __init__(self, board):
        self.board = board
        assert len(board) == len(board[0])

        self.grid_length = len(board)
        self.numbers = []

    def draw(self, number):
        self.numbers.append(number)

    def has_bingo(self):
        return any(all(n in self.numbers for n in line) for line in self.board) or \
               any(all(l[pos] in self.numbers for l in self.board) for pos in range(self.grid_length))

    def score(self):
        return sum(n for n in itertools.chain(*self.board) if n not in self.numbers) * self.numbers[-1]


def get_boards(lines):
    boards = []

    data = []
    for line in lines:
        if line == "" and data:
            boards.append(Bingo(data))
            data = []
        else:
            data.append(list(map(int, line.split())))

    if data:
        boards.append(Bingo(data))

    return boards


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()
    numbers = list(map(int, lines[0].split(',')))
    boards = get_boards(lines[2:])

    for n in numbers:
        for b in boards:
            b.draw(n)
            if b.has_bingo():
                print(f"BINGO! Score: {b.score()}")
                sys.exit(0)
