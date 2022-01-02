from pathlib import Path

"""
7 segment display

0 - abc.efg  6  3-fold
1 - ..c..f.  2  unique
2 - a.cde.g  5  3-fold
3 - a.cd.fg  5  3-fold
4 - .bcd.f.  4  unique
5 - ab.d.fg  5  3-fold
6 - ab.defg  6  3-fold
7 - a.c..f.  3  unique
8 - abcdefg  7  unique
9 - abcd.fg  6  3-fold

2
"""
if __name__ == "__main__":
    lines = Path('input').read_text().splitlines()

    count = 0
    for line in lines:
        _, out_val = line.split('|')
        values = out_val.split()
        count += len([v for v in values if len(v) in [2, 3, 4, 7]])

    print(f"result: {count}")
