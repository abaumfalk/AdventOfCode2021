from pathlib import Path


class PathFinder:
    def __init__(self, connections):
        self.cave_to_caves = {}
        for a, b in connections:
            for origin, destination in [(a, b), (b, a)]:
                if origin in self.cave_to_caves:
                    self.cave_to_caves[origin].append(destination)
                else:
                    self.cave_to_caves[origin] = [destination]

        self.paths = None

    def get_paths(self):
        if self.paths is None:
            self.paths = self.go(['start'])
        return self.paths

    def go(self, path):
        results = []
        for step in self.cave_to_caves[path[-1]]:
            if step.islower() and step in path:
                continue
            if step == 'end':
                results.append(path + [step])
            else:
                results += self.go(path + [step])
        return results


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()
    connections = [line.split('-') for line in lines]

    path_finder = PathFinder(connections)
    paths = path_finder.get_paths()

    print(f"number of paths: {len(paths)}")