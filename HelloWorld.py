# import string
# import random
# import time

# target = "Hello World"
# letters = string.ascii_letters + " "
# result = ""

# for letter in target:
#     while True:
#         I = random.choice(letters)
#         print(f"\r{result + I}", end="")
#         if I == letter:
#             result += I
#             break
#         time.sleep(0.05)

import string
import random
import time

target = "Hello World"
letters = string.ascii_letters + " "
result = ""

for letter in target:
    while True:
        I = random.choice(letters)
        print(result + I)
        if I == letter:
            result += I
            break
        time.sleep(0.05)

