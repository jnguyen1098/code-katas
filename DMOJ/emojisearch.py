import re

for result in re.findall(r"(:[\w ]+:)", input()):
    print(result[1:-1])

