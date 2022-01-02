from pathlib import Path


class Depth:
    @staticmethod
    def count_increased(data):
        result = 0
        for i in range(len(data) - 1):
            if data[i + 1] > data[i]:
                result += 1

        return result

    @staticmethod
    def to_window(data, length):
        result = []
        for i in range(0, len(data) - length + 1):
            slice = data[i: length + i]
            result.append(sum(slice))
        return result


if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()
    data = list(map(int, lines))

    data = Depth.to_window(data, 3)
    increased = Depth.count_increased(data)

    print(f"number of increases: {increased}")
