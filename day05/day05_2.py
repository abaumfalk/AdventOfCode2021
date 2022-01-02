import itertools
import sys
from pathlib import Path
from typing import List, Tuple


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Line:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __repr__(self):
        return f"({self.start.__repr__()} -> {self.stop.__repr__()}"


class Vents:
    def __init__(self, lines):
        self.lines = lines

    @staticmethod
    def is_horizontal(line):
        return line.start.y == line.stop.y

    @staticmethod
    def is_vertical(line):
        return line.start.x == line.stop.x

    def get_coverage_hv(self):
        coverage = {}
        for line in self.lines:
            if self.is_horizontal(line):
                start = min(line.start.x, line.stop.x)
                stop = max(line.start.x, line.stop.x)
                for x in range(start, stop + 1):
                    point = Point(x, line.start.y)
                    if point in coverage:
                        coverage[point] += 1
                    else:
                        coverage[point] = 1
            elif self.is_vertical(line):
                start = min(line.start.y, line.stop.y)
                stop = max(line.start.y, line.stop.y)
                for y in range(start, stop + 1):
                    point = Point(line.start.x, y)
                    if point in coverage:
                        coverage[point] += 1
                    else:
                        coverage[point] = 1
            else:
                xrange = line.stop.x - line.start.x
                yrange = line.stop.y - line.start.y
                # only 45 degrees allowed
                assert abs(xrange) == abs(yrange)

                for d in range(abs(xrange) + 1):
                    dx = d if xrange > 0 else -d
                    dy = d if yrange > 0 else -d
                    point = Point(line.start.x + dx, line.start.y + dy)
                    if point in coverage:
                        coverage[point] += 1
                    else:
                        coverage[point] = 1

        return coverage


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()
    vent_lines = []
    for line in lines:
        start, stop = line.split('->')
        start = tuple(map(int, start.split(',')))
        start_point = Point(start[0], start[1])

        stop = tuple(map(int, stop.split(',')))
        stop_point = Point(stop[0], stop[1])

        vent_lines.append(Line(start_point, stop_point))

    vents = Vents(vent_lines)
    coverage = vents.get_coverage_hv()

    cov2_count = len([c for c in coverage.values() if c >= 2])
    print(f"coverage is >= 2 at {cov2_count} points")