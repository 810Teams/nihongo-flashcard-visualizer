'''
    `statistics.py`
'''

from math import ceil
from math import sqrt

from random import choices

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


def progress_ratio(raw_data):
    ''' Function: Calculates progress ratio on current learned words '''
    raw_data_copy = [i + 3 for i in raw_data]
    return sum(raw_data_copy)/(15 * len(raw_data_copy))

def estimated(data, days=7, incorrect_p=0.0, learn_pattern=[0], result='flashcard'):
    ''' Function: Calculates estimated flashcards per day '''
    # Step 1: Prepare reference variable.
    level_weight = 1, 2, 3, 7, 14, 21, 30, 60, 90, 180, 270, 360, None          # Level weight

    # Step 2: Prepare dynamic variables.
    data_copy = [i for i in data] + [0] * (13 - len(data))                      # A copy of data
    current_rate = [data_copy[i] / level_weight[i] for i in range(12)] + [0]    # Current learning rates
    is_added = [False for _ in range(13)]                                       # Level status, true means the amount is added recently

    # Step 3: Prepare result container variables.
    review_list = list()    # Reviewed flashcard amount in each day
    vocab_list = list()     # Vocabulary levels in each day

    # Step 4: Algorithm, one loop cycle represents a day.
    for i in range(days):
        # Step 4.1: Create a new review list for a certain day.
        review_list.append([0 for _ in range(12)])

        # Step 4.2: Check if a certain level of word amount is added, if true, adjust the rate.
        for j in range(0, 12):
            if is_added[j]:
                current_rate[j] = data_copy[j] / level_weight[j]
                is_added[j] = False
        
        # Step 4.3: Review words of each level, raise levels.
        for j in range(12):
            # Step 4.3.1: Make a review progress, not necessarily an integer, not actual review.
            subtractor = max(min(current_rate[j], data_copy[j]), 0) # Purpose: To set bounds and prevent references.
            data_copy[j] -= subtractor

            # Step 4.3.2: Check if remaining words of a certain level reached zero, stop the review rate.
            if data_copy[j] == 0:
                current_rate[j] = 0

            # Step 4.3.3: Actual reviewed words calculation, using the integer decrement.
            if ceil(data_copy[j]) != ceil(data_copy[j] + subtractor):
                # Step 4.3.3.1: Define expected review word amount without incorrection
                reviewed = abs(ceil(data_copy[j]) - ceil(data_copy[j] + subtractor))
                review_list[-1][j] = reviewed

                # Step 4.3.3.2: Check for incorrect review possability
                incorrect_a = 0
                for _ in range(reviewed):
                    incorrect_a += choices([False, True], [1 - incorrect_p, incorrect_p])[0]
                
                # Step 4.3.3.3: Decrease the level of incorrect reviewed words
                if incorrect_a > 0:
                    data_copy[max(j - 1, 0)] += incorrect_a
                    is_added[max(j - 1, 0)] = True
                
                # Step 4.3.3.4: Increase the level of words
                if reviewed - incorrect_a > 0:
                    data_copy[j + 1] += reviewed - incorrect_a
                    is_added[j + 1] = True
        
        # Step 4.4: Learn new words, will be ready for the next day's review.
        if learn_pattern[(i - 1) % len(learn_pattern)] != 0:
            data_copy[0] += learn_pattern[(i - 1) % len(learn_pattern)]
            is_added[0] = True
        
        # Step 4.5: Record the words of each level of a day
        vocab_list.append([ceil(j) for j in data_copy])
    
    # Step 5: Return desired value
    if result == 'flashcard':
        return review_list
    elif result == 'vocabulary':
        return vocab_list
