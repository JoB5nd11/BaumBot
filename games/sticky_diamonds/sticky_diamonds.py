import random
import json
import math
import os

from sklearn.utils import resample

class StickyDiamonds():
    def __init__(self):
        self._cwd = os.getcwd() + '\\games\\sticky_diamonds\\'

        self.value_table = self._get_value_table()
        self._generate_real_frequencies()

    def roll(self, stake):
        current_screen = self._generate_screen()
        print(" ".join(current_screen[0:5]))
        print(" ".join(current_screen[5:10]))
        print(" ".join(current_screen[10:15]))

    def test_roll(self):
        current_screen = self._generate_screen()
        result = " ".join(current_screen[0:5]) + "\n"
        result += " ".join(current_screen[5:10]) + "\n"
        result += " ".join(current_screen[10:15])
        return result

    def _get_value_table(self):
        with open(self._cwd + 'value_table.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    def _generate_real_frequencies(self):
        #Using Bandii's Formula for normalized Rarity-Probability
        raw_freqs = [self.value_table[el]['frequency'] for el in self.value_table]
        freqs = []
        for r in raw_freqs:
            a = 100 / r
            numerator = sum(raw_freqs)
            denominator = sum([(1 / r_inner) * sum(raw_freqs) for r_inner in raw_freqs])
            result = a * (numerator / denominator)
            freqs.append(result)

        freq_pos_sum = 0
        for i, el in enumerate(self.value_table):
            self.value_table[el]['real_frequency'] = freqs[i]
            self.value_table[el]['real_frequency_sum'] = freqs[i] + freq_pos_sum
            freq_pos_sum += freqs[i]


    def _get_weighted_random(self):
        random_number = 100 * random.random()
        current_shortest = 100
        current_element = None
        for el in self.value_table:
            # print("Random Number: ", random_number)
            # print("Current Element: ", self.value_table[el]['real_frequency_sum'])
            # print("Difference: ", abs(random_number - self.value_table[el]['real_frequency_sum']))
            # print("Curr. Min. Diff: ", current_shortest)
            # print()

            if abs(random_number - self.value_table[el]['real_frequency_sum']) < current_shortest:
                current_shortest = abs(random_number - self.value_table[el]['real_frequency_sum'])
                current_element = self.value_table[el]['emoji']
        return current_element

    
    def _generate_screen(self):
        return [self._get_weighted_random() for _ in range(15)]



if __name__ == '__main__':
    slot = StickyDiamonds()
    slot.test_roll()