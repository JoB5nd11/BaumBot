import random

class RandomClient:
    def __init__(self):
        pass

    def get_random_number(self, lower, higher):
        higher = int(higher)
        lower = int(lower)
        if higher <= lower:
            higher = lower + 1
        return str(random.randint(int(lower), int(higher)))
