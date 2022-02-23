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
            self.all_responses[elements[0]] = elements[1]

    def responde(self, message):
        if message not in self.all_responses:
            return None
        return self.all_responses[message]
