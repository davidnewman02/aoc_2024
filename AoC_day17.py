import re


def parse_input(in_file):
    with open(in_file, "r") as fh:
        in_lines = fh.read().split('\n')
    A = int(re.findall(r"\d+", in_lines[0])[0])
    B = int(re.findall(r"\d+", in_lines[1])[0])
    C = int(re.findall(r"\d+", in_lines[2])[0])
    ops = [int(i) for i in re.findall(r"\d+", in_lines[4])]
    return A, B, C, ops


class Computer:

    def __init__(self, a, b, c, ops):
        self.pos = 0
        self.a = a
        self.b = b
        self.c = c
        self.ops = ops
        self.out_codes = []

        self.op_map = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            #            6: self.bdv,
            7: self.cdv,
        }

        self.combo_map = {
            0: lambda: 0,
            1: lambda: 1,
            2: lambda: 2,
            3: lambda: 3,
            4: lambda: self.a,
            5: lambda: self.b,
            6: lambda: self.c,
        }

    def run(self):
        # print("Running: ", self.a, self.b, self.c, self.ops)
        while self.pos < len(self.ops):
            # print(
            #     oct(self.a)[2:],
            #     oct(self.b)[2:],
            #     oct(self.c)[2:],
            #     oct(self.pos)[2:],
            #     "--", self.ops[self.pos], self.ops[self.pos+1], [self.a] + self.out_codes if self.ops[self.pos]==5 else "")
            self.op_map[self.ops[self.pos]](self.ops[self.pos + 1])
            self.pos += 2

        return self.out_codes

    def adv(self, combo):
        self.a = self.a // (2 ** self.combo_map[combo]())

    def bxl(self, lit):
        self.b = self.b ^ lit

    def bst(self, combo):
        self.b = self.combo_map[combo]() % 8

    def jnz(self, lit):
        if self.a == 0:
            return
        self.pos = lit - 2

    def bxc(self, _):
        self.b = self.b ^ self.c

    def out(self, combo):
        self.out_codes.append(self.combo_map[combo]() % 8)

    def bdv(self, combo):
        self.b = self.a // 2 ** self.combo_map[combo]()

    def cdv(self, combo):
        self.c = self.a // 2 ** self.combo_map[combo]()


def run_tests():
    comp = Computer(0, 0, 9, [2, 6])
    _ = comp.run()
    assert comp.b == 1

    comp = Computer(10, 0, 0, [5, 0, 5, 1, 5, 4])
    output = comp.run()
    assert output == [0, 1, 2]

    comp = Computer(2024, 0, 0, [0, 1, 5, 4, 3, 0])
    output = comp.run()
    assert comp.a == 0
    assert output == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]

    comp = Computer(0, 29, 0, [1, 7])
    _ = comp.run()
    assert comp.b == 26

    comp = Computer(0, 2024, 43690, [4, 0])
    _ = comp.run()
    assert comp.b == 44354



## run_tests()

A, B, C, ops = parse_input("AoC_input/day17.txt")
comp = Computer(A, B, C, ops)
output = comp.run()
print("Part.1: ", ",".join([str(i) for i in output]))

def solve(ops, a, pos):
    """
    Solution adapted based on other solutions seen online.

    The input number is a len(ops)-base8. Each previous digit is independent
    since the mod operations clear out any remainder.
    We work backwards through the digits of the oct-number, when we find
    something that matches the tail of the output we lock that number in.
    """
    if Computer(a, 0, 0, ops).run() == ops:
        return a
    for i in range(8):
        if Computer(a * 8 + i, 0, 0, ops).run()[0] == ops[-pos]:
            if solution := solve(ops, a * 8 + i, pos + 1):
                return solution

solution = solve(ops, 0, 1)
print("Part.2 (oct): ", oct(solution))
print("Part.2: ", solution)

## Pt.2 - Brute force - nope

# class Corruptor(Computer):
#
#     def out(self, combo):
#         super().out(combo)
#         if self.out_codes != self.ops[:len(self.out_codes)]:
#             raise ValueError
#
#     def run(self):
#         try:
#             super().run()
#         except ValueError:
#             return self.out_codes
#
# i = 0
# while i < A:
#     if not i % 10000: print(i)
#     i += 1
#     try:
#         out = Corruptor(i, 0, 0, ops).run()
#         if out == ops:
#             print("self val: ", i, out, ops)
#             break
#     except ValueError:
#         continue
#
# #
# # comp = Corruptor(2024, 0, 0, [0,3,5,4,3,0])
# # print(comp.run())
