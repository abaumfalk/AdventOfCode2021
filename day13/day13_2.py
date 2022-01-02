from pathlib import Path


class Folder:
    def __init__(self, dots, folds):
        self.dots = set(dots)
        self.folds = folds

    def fold(self):
        direction, pos = self.folds.pop(0)
        if direction == 'y':
            self._fold_up(pos)
        else:
            self._fold_left(pos)

    def _fold_up(self, pos):
        dots_new = set()
        for x, y in self.dots:
            if y < pos:
                dots_new.add((x, y))
            else:
                dots_new.add((x, pos - (y - pos)))
        self.dots = dots_new

    def _fold_left(self, pos):
        dots_new = set()
        for x, y in self.dots:
            if x < pos:
                dots_new.add((x, y))
            else:
                dots_new.add((pos - (x - pos), y))
        self.dots = dots_new

    def fold_all(self):
        while self.folds:
            self.fold()


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()

    dots = []
    dots_finished = False
    folds = []
    for line in lines:
        if not dots_finished:
            if not line:
                dots_finished = True
                continue
            [x, y] = list(map(int, line.split(',')))
            dots.append((x, y))
        else:
            direction, pos = line[11:].split('=')
            folds.append((direction, int(pos)))

    folder = Folder(dots, folds)
    folder.fold_all()

    import turtle

    turtle.penup()

    for x, y in folder.dots:
        turtle.setx(x * 5)
        turtle.sety(-y * 5)
        turtle.dot()

    turtle.setx(-100)
    turtle.sety(-100)
    input()
