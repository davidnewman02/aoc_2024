import re


class Machine:

    def __init__(self, a, b, target):
        self.a = a
        self.b = b
        self.tar = target

    @property
    def cramer(self):
        det = self.a[0] * self.b[1] - self.a[1] * self.b[0]
        det_a = self.tar[0] * self.b[1] - self.tar[1] * self.b[0]
        det_b = self.a[0] * self.tar[1] - self.a[1] * self.tar[0]
        return det_a / det, det_b / det

    def cost(self):
        if self.cramer[0].is_integer() and self.cramer[1].is_integer():
            return self.cramer[0] * 3 + self.cramer[1]
        return 0

    @classmethod
    def from_str(cls, mach_str):
        a_str, b_str, tar_str = mach_str.split('\n')
        a = [int(i) for i in re.findall('\d+', a_str)]
        b = [int(i) for i in re.findall('\d+', b_str)]
        target = [int(i) for i in re.findall('\d+', tar_str)]
        return cls(a, b, target)

    @classmethod
    def from_str2(cls, mach_str):
        a_str, b_str, tar_str = mach_str.split('\n')
        a = [int(i) for i in re.findall('\d+', a_str)]
        b = [int(i) for i in re.findall('\d+', b_str)]
        offset = 10000000000000
        target = [int(i) + offset for i in re.findall('\d+', tar_str)]
        return cls(a, b, target)

    def __repr__(self):
        return f"Machine: A={self.a} B={self.b} Target={self.tar}"


def part_1(in_str):
    return sum(Machine.from_str(mach).cost() for mach in in_str.split("\n\n"))


def part_2(in_str):
    return sum(Machine.from_str2(mach).cost() for mach in in_str.split("\n\n"))


in_file = "AoC_input/day13.txt"
with open(in_file, "r") as fh:
    in_str = fh.read()

print("Part.1: ", part_1(in_str))
print("Part.2: ", part_2(in_str))
