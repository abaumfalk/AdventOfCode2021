import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class Visitable(ABC):
    @abstractmethod
    def _get_elements(self):
        pass

    def visit(self, visitor):
        cont = True

        for element in self._get_elements():
            cont = visitor.enter(element)
            if cont:
                cont = element.visit(visitor)
            visitor.exit(element)

        visitor.finalize(self)
        return cont


class SnailfishNumber(Visitable):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.parent = None

    def __repr__(self):
        return f"[{self.left}, {self.right}]"

    def _get_elements(self):
        yield from [self.left, self.right]

    def reduce(self):
        while self._explode() or self._split():
            pass

    def _explode(self):
        return self._visit(SnailfishExplodeVisitor)

    def _split(self):
        return self._visit(SnailfishSplitVisitor)

    def _visit(self, visitor_class):
        visitor = visitor_class()
        self.visit(visitor)
        return visitor.result

    def __add__(self, other):
        result = SnailfishNumber(self, other)

        self.parent = result
        other.parent = result

        result.reduce()
        return result

    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    @classmethod
    def from_string(cls, string: str):
        lst = json.loads(string)
        return cls.from_list(lst)

    @classmethod
    def from_list(cls, lst: list):
        [left, right] = (
            cls.from_list(item) if isinstance(item, list) else SnailfishValue(item)
            for index, item in enumerate(lst)
        )
        result = SnailfishNumber(left, right)

        for item in [left, right]:
            item.parent = result

        return result


class SnailfishValue(Visitable):
    def __init__(self, value):
        self.value = value
        self.parent = None

    def _get_elements(self):
        yield from []

    def __repr__(self):
        return f"{self.value}"

    def magnitude(self):
        return self.value


class Visitor(ABC):
    @property
    @abstractmethod
    def result(self):
        pass

    @abstractmethod
    def enter(self, element) -> bool:
        pass

    @abstractmethod
    def exit(self, element):
        pass

    @abstractmethod
    def finalize(self, element):
        pass


class SnailfishExplodeVisitor(Visitor):
    STATE_INITIAL = 0
    STATE_FOUND_ELEMENT = 1
    STATE_EXPLODE_FINISHED = 2

    def __init__(self):
        super().__init__()
        self.state = self.STATE_INITIAL

        self.depth: int = 0
        self.left_value: Optional[SnailfishValue] = None
        self.right_value = None

    @property
    def result(self):
        return self.state != self.STATE_INITIAL

    def enter(self, element) -> bool:
        self.depth += 1

        if self.state == self.STATE_EXPLODE_FINISHED:
            return False

        if self.state == self.STATE_INITIAL:
            # we are searching for a SnailFishNumber to-be-expanded
            if self.depth == 4 and isinstance(element, SnailfishNumber):
                # found the element to-be-expanded
                self.state = self.STATE_FOUND_ELEMENT

                left_val, self.right_value = element.left.value, element.right.value
                new_element = SnailfishValue(0)
                new_element.parent = element.parent
                if element == element.parent.left:
                    element.parent.left = new_element
                else:
                    element.parent.right = new_element

                # modify left literal, if recorded previously
                if self.left_value is not None:
                    self.left_value.value += left_val

                return False  # do not enter the deleted element

            elif isinstance(element, SnailfishValue):
                self.left_value = element

            return True

        # we are searching for the next number to the right
        if isinstance(element, SnailfishValue):
            element.value += self.right_value
            self.state = self.STATE_EXPLODE_FINISHED
            return False

        return True

    def exit(self, element):
        self.depth -= 1

    def finalize(self, element):
        pass


class SnailfishSplitVisitor(Visitor):
    def __init__(self):
        self.found = False

    @property
    def result(self):
        return self.found

    def enter(self, element) -> bool:
        if self.found:
            return False

        if isinstance(element, SnailfishValue) and element.value >= 10:
            val = element.value // 2
            new_element = SnailfishNumber(SnailfishValue(val), SnailfishValue(val + element.value % 2))
            new_element.parent = element.parent
            new_element.left.parent = new_element
            new_element.right.parent = new_element
            if element == element.parent.left:
                element.parent.left = new_element
            else:
                element.parent.right = new_element

            self.found = True
            return False

        return True

    def exit(self, element):
        pass

    def finalize(self, element):
        pass


if __name__ == "__main__":
    lines = Path('input.txt').read_text().splitlines()

    result = None
    for line in lines:
        snailfish_number = SnailfishNumber.from_string(line)
        if result is None:
            result = snailfish_number
        else:
            result += snailfish_number

    print(f"result:{result}")
    print(f"magnitude: {result.magnitude()}")
