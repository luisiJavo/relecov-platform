import random


def generate_random_sequences():
    sequence_list = []
    for i in range(103):
        sequence = random.randint(100, 1000)
        sequence_list.append(sequence)
    return sequence_list


def generate_weeks():
    weeks_list = []
    MAX1 = 10
    MAX2 = 3
    counter = 0

    while counter < MAX1:
        weeks_list.append(1)
        counter += 1
    counter = 0
    while counter < MAX1:
        weeks_list.append(2)
        counter += 1
    counter = 0
    while counter < MAX1:
        weeks_list.append(3)
        counter += 1
    counter = 0
    while counter < MAX1:
        weeks_list.append(4)
        counter += 1
    counter = 0
    while counter < MAX1:
        weeks_list.append(5)
        counter += 1
    counter = 0
    while counter < MAX1:
        weeks_list.append(6)
        counter += 1
    counter = 0
    while counter < MAX1:
        weeks_list.append(7)
        counter += 1
    counter = 0
    while counter < MAX1:
        weeks_list.append(8)
        counter += 1
    counter = 0
    while counter < MAX1:
        weeks_list.append(1)
        counter += 1
    counter = 0
    while counter < MAX1:
        weeks_list.append(9)
        counter += 1
    counter = 0
    while counter < MAX1:
        weeks_list.append(10)
        counter += 1
    counter = 0
    while counter < MAX2:
        weeks_list.append(11)
        counter += 1
    counter = 0

    return weeks_list
