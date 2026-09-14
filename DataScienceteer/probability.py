
import enum, random

from contourpy.array import offsets_from_lengths


#chances of 2 child that will be given birth to been  both boys, or first being a boy,.....

class Kid(enum.Enum):
    BOY = 0
    GIRL = 1

both_boys = 0
either_boys = 0
older_boy = 0

def random_kid():
    return random.choice([Kid.BOY, Kid.GIRL])

for _ in range(1000):
    younger = random_kid()
    older = random_kid()

    if older == Kid.BOY:
        older_boy += 1
    if older == Kid.BOY or younger == Kid.BOY:
        either_boys += 1
    if older == Kid.BOY and younger ==Kid.BOY:
        both_boys += 1

print(both_boys/1000)
print(either_boys/1000)
print(older_boy/1000)
print(f"probability of both child to be boys if first child is a boy: {both_boys/older_boy}")

