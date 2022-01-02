from pathlib import Path


class SyntaxChecker:
    PAIRS = {
        '{': '}',
        '(': ')',
        '[': ']',
        '<': '>',
    }
    ERROR_SCORE = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }
    AUTOCOMPLETE_SCORE = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }

    def __init__(self, line):
        self.line = line
        self.error_score = 0
        self.autocomplete_score = 0

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
            return True, c

        return False, stack

    def run(self):
        error, value = self.check()
        if error:
            self.error_score = self.ERROR_SCORE[value]
        else:
            for c in reversed(value):
                self.autocomplete_score *= 5
                self.autocomplete_score += self.AUTOCOMPLETE_SCORE[self.PAIRS[c]]


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()

    error_score = 0
    autocomplete_scores = []
    for line in lines:
        checker = SyntaxChecker(line)
        checker.run()
        error_score += checker.error_score
        if checker.autocomplete_score:
            autocomplete_scores.append(checker.autocomplete_score)

    autocomplete_scores = sorted(autocomplete_scores)
    center_index = (len(autocomplete_scores) - 1) >> 1
    autocomplete_center = autocomplete_scores[center_index]
    print(f"error score: {error_score}")
    print(f"autocomplete scores: {autocomplete_scores}")
    print(f"autocomplete center: {autocomplete_center}")
