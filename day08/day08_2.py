import itertools
from pathlib import Path


class Decoder:
    CODE = {
        "abcefg": 0,
        "cf": 1,  # singular 2
        "acdeg": 2,
        "acdfg": 3,
        "bcdf": 4,  # singular 4
        "abdfg": 5,
        "abdefg": 6,
        "acf": 7,  # singular 3
        "abcdefg": 8,  # useless
        "abcdfg": 9,
    }

    def __init__(self, mapping=None):
        self.mapping = mapping

    def _unmap(self, segments):
        if self.mapping is None:
            return segments
        else:
            return [self.mapping[ord(s) - 97] for s in segments]

    @staticmethod
    def unmap(code, mapping):
        return {mapping[ord(c) - 97] for c in code}

    def decode(self, code: str) -> int:
        code = "".join(sorted(self._unmap(code)))
        return self.CODE[code]


class CodeBreaker:
    def __init__(self, patterns):
        self.patterns = list(map(lambda x: set(x), sorted(patterns, key=len)))

    def test(self, mapping, code, expected):
        result = Decoder.unmap(code, mapping)
        return result == expected

    def get_decoder(self):
        # first, we filter the simple cases (digits 1, 7 and 4)
        filters = [
            "cf",  # digit 1
            "acf",  # digit 7
            "bcdf"  # digit 4
        ]
        candidates = itertools.permutations("abcdefg")
        for index, filter in enumerate(filters):
            candidates = [m for m in candidates if self.test(m, self.patterns[index], set(filter))]

        # now only a few candidates should be left, so let's try them all
        for mapping in candidates:
            decoder = Decoder(mapping)
            for pattern in self.patterns[3:]:
                try:
                    decoder.decode(pattern)
                except KeyError:
                    break
            else:
                return decoder

        return None


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()
    decoder = Decoder()
    num = decoder.decode("cf")
    pass

    result = 0
    for line in lines:
        patterns, output = line.split('|')

        code_breaker = CodeBreaker(patterns.split())
        decoder = code_breaker.get_decoder()

        output = output.split()
        number = ""
        for o in output:
            number += str(decoder.decode(o))

        result += int("".join(number))

    print(f"result: {result}")
