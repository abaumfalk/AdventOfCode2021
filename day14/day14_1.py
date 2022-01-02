from pathlib import Path


class PolymerGenerator:
    def __init__(self, template, rules):
        self.polymer = template
        self.length = len(self.polymer)
        self.rules = rules

    def step(self):
        new_polymer = []
        for key, value in enumerate(self.polymer):
            new_polymer.append(value)
            if key < self.length - 1:
                pair = "".join(self.polymer[key:key + 2])
                insertion = self.rules.get(pair)
                if insertion is not None:
                    new_polymer.append(insertion)

        self.polymer = new_polymer
        self.length = len(new_polymer)


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()

    template = lines[0]

    rules = dict(line.split(' -> ') for line in lines[2:])
    polymer_generator = PolymerGenerator(template, rules)

    for _ in range(10):
        polymer_generator.step()

    count = {e: polymer_generator.polymer.count(e) for e in set(polymer_generator.polymer)}
    result = max(count.values()) - min(count.values())

    print(f"result: {result}")
