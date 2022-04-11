import random


def generate_random_sequences():
    sequence_list = []
    for i in range(3886):
        sequence = random.randint(100, 1000)
        sequence_list.append(sequence)
    return sequence_list


def generate_weeks():
    weeks_list = []

    for j in range(200):
        weeks_list.append(1)
    for k in range(300):
        weeks_list.append(2)
    for l in range(400):
        weeks_list.append(3)
    for m in range(375):
        weeks_list.append(4)
    for n in range(386):
        weeks_list.append(5)
    for o in range(400):
        weeks_list.append(6)
    for p in range(450):
        weeks_list.append(7)
    for q in range(500):
        weeks_list.append(8)
    for r in range(400):
        weeks_list.append(9)
    for s in range(350):
        weeks_list.append(10)
    for t in range(125):
        weeks_list.append(11)

    return weeks_list
