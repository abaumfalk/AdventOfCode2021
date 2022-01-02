from pathlib import Path


class SyntaxChecker:
    PAIRS = {
        '{': '}',
        '(': ')',
        '[': ']',
        '<': '>',
    }
    SCORE = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }

    def __init__(self, line):
        self.line = line
        self.score = None

    def check(self):
        stack = []
        for c in self.line:
            # opening char
            if c in self.PAIRS.keys():
                stack.append(c)
                continue

            # closing char
            opening = stack.pop()
            if c == self.PAIRS[opening]:
                continue

            # error
            self.score = self.SCORE[c]
            return False

        self.score = 0
        return True

    def get_score(self):
        if self.score is None:
            self.check()

        return self.score


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()

    score = 0
    for line in lines:
        checker = SyntaxChecker(line)
        score += checker.get_score()

    print(f"score: {score}")
