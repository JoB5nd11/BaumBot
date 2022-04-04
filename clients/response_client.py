import random
from collections import OrderedDict

class ResponseClient:
    def __init__(self, filepath='documents/responses.txt'):
        self.filepath = filepath
        self.all_responses = {}

        self.read_responses_from_file()

    def read_responses_from_file(self):
        response_file = open(self.filepath, 'r', encoding='utf-8')
        lines = response_file.readlines()
        for line in lines:
            elements = line.split(' -> ')
            elements[1] = elements[1].split('\n')[0]

            if elements[0] not in self.all_responses.keys():
                self.all_responses[elements[0]] = []
            self.all_responses[elements[0]].append(elements[1])

        response_file.close()

    def print_responses(self):
        answer = ""
        for key in self.get_alphabet_copy():
            for a in self.all_responses[key]:
                answer += f'{key} -> {a}\n'
        return answer

    def responde(self, message):
        for r in self.all_responses:
            if r in message:
                return random.choice(self.all_responses[r])
        return None

    def add_response(self, trigger, answer):
        with open(self.filepath, 'a', encoding='utf-8') as file:
            file.write(f'{trigger} -> {answer}\n')
        self.read_responses_from_file()

    def delete_all_reponses(self, trigger):
        counter = 0
        new_lines = []
        with open(self.filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            elements = line.split(' -> ')
            elements[1] = elements[1].split('\n')[0]

            if elements[0] != trigger:
                new_lines.append(line)
            else:
                counter += 1

        with open(self.filepath, 'w', encoding='utf-8') as file:
            for line in new_lines:
                file.write(line)

        self.read_responses_from_file()

        if counter > 0:
            return f'Deleted {counter} answers'
        return f'{trigger} not found. Try `/printresponses`'


    def delete_response(self, trigger, answer):
        new_lines = []
        fin_answer = ""

        with open(self.filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            elements = line.split(' -> ')
            elements[1] = elements[1].split('\n')[0]

            #is there a better way? yes but idk
            if elements[0] == trigger and elements[1] == answer:
                fin_answer = f'Deleted: `{trigger} -> {answer}`'
            else:
                new_lines.append(line)

        with open(self.filepath, 'w', encoding='utf-8') as file:
            for line in new_lines:
                file.write(line)

        self.read_responses_from_file()

        if fin_answer == "":
            return f'{trigger} -> {answer} not found. Try `/printresponses`'
        return fin_answer

    def get_alphabet_copy(self):
        copy = self.all_responses.copy()
        return sorted(copy.keys(), key=lambda x:x.lower())


if __name__ == '__main__':
    rc = ResponseClient(filepath=r'D:\Users\User\Desktop\Prgrammieren\Python\Discord Bots\BaumBot\documents\responses.txt')
    #print(rc.responde('test_multiple xyz'))
    print(rc.delete_response('testtest', '12321'))
