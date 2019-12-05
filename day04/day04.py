import re

RANGE = range(231832,767346)
PATTERN = re.compile(r"(\d)\1")
PATTERN2 = re.compile(r"(\d)\1\1+")

part1numbers = 0
part2numbers = 0
for number in RANGE:
    ascending = True

    last_i = 0
    for i in str(number):
        if int(i) < last_i:
            ascending = False
            break
        last_i = int(i)

    matches = PATTERN.findall(str(number))

    if ascending and matches:
        part1numbers += 1

        matches2 = PATTERN2.findall(str(number))

        if set(matches).difference(matches2):
            part2numbers += 1


print(part1numbers)
print(part2numbers)
