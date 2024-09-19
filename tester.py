from math import factorial
def PossibleArrangements(x: int, y: int):
    return factorial(x) // (factorial(x-y) * factorial(y))

x = 13
y = 3

prb1 = PossibleArrangements(x, y)

prb2 = PossibleArrangements(x-1, y-1)
print(prb1)
print(prb2)

print(y / x)
prb2 = prb2 - 10

print(prb2 / prb1)