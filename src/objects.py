'''
    `objects.py`
'''

from random import choices


class FlashcardData:
    progress_days = (1, 2, 3, 7, 14, 21, 30, 60, 90, 180, 270, 360, None)

    def __init__(self, progress=0, days=None, auto_replace_error=[]):
        if 0 <= progress <= 12:
            self.progress = int(progress)
        elif 'progress' in auto_replace_error:
            self.progress = min(max(int(progress), 0), 12)
        else:
            raise FlashcardError

        if days == None:
            self.days = FlashcardData.progress_days[progress]
        elif 'days' in auto_replace_error:
            if days <= 1:
                self.days = 1
            elif progress == 12:
                self.days = None
            else:
                self.days = int(days)
        else:
            if days <= 1 or progress == 12:
                raise FlashcardError
            self.days = int(days)

    def count(self):
        if self.progress == 12:
            raise FlashcardError

        if self.days >= 1:
            self.days -= 1

    def review(self, correct_p=1.0):
        is_correct = choices([False, True], [1 - correct_p, correct_p])[0]

        if self.days == 0 and self.progress < 12:
            if is_correct:
                self.progress += 1
            elif not is_correct and self.progress > 0:
                self.progress -= 1
            self.days = FlashcardData.progress_days[self.progress]
        else:
            raise FlashcardError


class FlashcardError(Exception):
    pass
