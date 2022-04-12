import random


def generate_random_sequences():
    sequence_list = []
    for i in range(103):
        sequence = random.randint(100, 1000)
        sequence_list.append(sequence)
    return sequence_list


def generate_weeks():
    weeks_list = []

    for j in range(10):
        weeks_list.append(1)
    for k in range(10):
        weeks_list.append(2)
    for l in range(10):
        weeks_list.append(3)
    for m in range(10):
        weeks_list.append(4)
    for n in range(10):
        weeks_list.append(5)
    for o in range(10):
        weeks_list.append(6)
    for p in range(10):
        weeks_list.append(7)
    for q in range(10):
        weeks_list.append(8)
    for r in range(10):
        weeks_list.append(9)
    for s in range(10):
        weeks_list.append(10)
    for t in range(3):
        weeks_list.append(11)

    return weeks_list
