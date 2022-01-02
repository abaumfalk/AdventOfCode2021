from copy import copy
from pathlib import Path
from typing import List, Tuple


class Submarine:
    def __init__(self, data):
        self.data = data
        self.data_len = len(data)
        self.word_len = len(self.data[0])

    def get_one_bits(self, data):
        result = [0] * self.word_len
        for word in data:
            for pos in range(self.word_len):
                if word[pos] == '1':
                    result[pos] += 1

        return result

    def get_oxygen_rating(self):
        result = copy(self.data)
        pos = 0
        while len(result) > 1:
            one_bits = self.get_one_bits(result)
            result = list(filter(lambda x: x[pos] == ('1' if one_bits[pos] >= len(result) / 2 else '0'), result))
            pos += 1

        return int(result[0], 2)

    def get_co2_rating(self):
        result = copy(self.data)
        pos = 0
        while len(result) > 1:
            one_bits = self.get_one_bits(result)
            result = list(filter(lambda x: x[pos] == ('1' if one_bits[pos] < len(result) / 2 else '0'), result))
            pos += 1

        return int(result[0], 2)

    def life_support_rating(self):
        oxygen_rating = self.get_oxygen_rating()
        co2_rating = self.get_co2_rating()
        return oxygen_rating * co2_rating


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()

    submarine = Submarine(lines)

    print(f"result: {submarine.life_support_rating()}")
