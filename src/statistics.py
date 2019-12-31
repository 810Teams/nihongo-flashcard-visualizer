from math import ceil
from math import sqrt

def median(raw_data):
    ''' Function: Calculates median '''
    raw_data_copy = sorted([i for i in raw_data])
    if len(raw_data_copy) % 2 == 0:
        return (raw_data_copy[len(raw_data_copy) // 2 - 1] + raw_data_copy[len(raw_data_copy) // 2]) / 2
    return raw_data_copy[len(raw_data_copy) // 2]


def average(raw_data):
    ''' Function: Calculates average '''
    return sum(raw_data) / len(raw_data)


def standard_dev(raw_data):
    ''' Function: Calculates standard deviation '''
    return sqrt(sum([(i - average(raw_data)) ** 2 for i in raw_data])/len(raw_data))


def estimated(data, days=7, learn_pattern=[0], result='flashcard'):
    ''' Function: Calculates estimated flashcards per day '''
    level_weight = 1, 2, 3, 7, 14, 21, 30, 60, 90, 180, 270, 360, None          # Level weight
    data_copy = [i for i in data] + [0] * (13 - len(data))                      # A copy of data
    last_subtractor = [data_copy[i] / level_weight[i] for i in range(12)] + [0] # Lastest subtractor
    is_added = [False for _ in range(13)]                                       # Is added

    vocab_size = list()
    reviewed = list()

    for i in range(days):
        reviewed.append([0 for _ in range(12)])

        if i != 0:
            data_copy[0] += learn_pattern[(i - 1) % len(learn_pattern)]
            is_added[0] = True

        for j in range(0, 12):
            if is_added[j]:
                last_subtractor[j] = data_copy[j] / level_weight[j]
                is_added[j] = False
        
        for j in range(12):
            subtractor = max(min(last_subtractor[j], data_copy[j]), 0) # Purpose: To limit the subtractor and prevent references
            data_copy[j] -= subtractor

            # Condition: Check if a cell reaches zero
            if data_copy[j] == 0:
                last_subtractor[j] = 0

            # Condition: Check if a cell is actually reduced to the lower integer completely
            if ceil(data_copy[j]) != ceil(data_copy[j] + subtractor):
                reviewed[-1][j] = abs(ceil(data_copy[j]) - ceil(data_copy[j] + subtractor))
                data_copy[j + 1] += abs(ceil(data_copy[j]) - ceil(data_copy[j] + subtractor))
                is_added[j + 1] = True
        
        vocab_size.append([ceil(j) for j in data_copy])
    
    if result == 'flashcard':
        return reviewed
    elif result == 'vocabulary':
        return vocab_size