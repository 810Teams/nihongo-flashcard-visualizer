'''
    `statistics.py`
'''

from src.objects import FlashcardData
from src.objects import FlashcardError

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


def progress_coverage(raw_data):
    ''' Function: Calculates progress coverage on current learned words '''
    raw_data_copy = [i + 3 for i in raw_data]
    return sum(raw_data_copy)/(15 * len(raw_data_copy))


def estimated(data, days=7, incorrect_p=0.0, learn_pattern=[0], result='flashcard'):
    ''' Function: Calculates estimated flashcards per day '''
    # Step 1: Data preparation
    data_copy = [i for i in data] + [0] * (13 - len(data))
    review_list = list()
    vocab_list = list()
    flashcards = list()

    # Step 2: Data generation
    for i in range(len(data_copy)):
        for j in range(data_copy[i]):
            flashcards.append(
                FlashcardData(
                    progress=i,
                    days=ceil(FlashcardData.progress_days[i] - FlashcardData.progress_days[i]/data_copy[i] * j),
                    auto_replace_error=['days']
                ) 
            )
    
    # Step 3: Iteration (Days)
    for i in range(days):
        # Step 3.1
        review_list.append([0 for _ in range(12)])

        # Step 3.2
        for j in range(len(flashcards)):
            if flashcards[j].progress < 12:
                flashcards[j].count()
        
        # Step 3.3
        for j in range(len(flashcards)):
            if flashcards[j].days == 0:
                review_list[-1][flashcards[j].progress] += 1
                flashcards[j].review(correct_p=1 - incorrect_p)

        # Step 3.4
        for i in range(learn_pattern[i % len(learn_pattern)]):
            flashcards.append(FlashcardData(progress=0))
        
        # Step 3.5
        if result == 'vocabulary':
            vocab_list.append([[k.progress for k in flashcards].count(j) for j in range(13)])

    # Step 4: Return
    if result == 'flashcard':
        return review_list
    elif result == 'vocabulary':
        return vocab_list

