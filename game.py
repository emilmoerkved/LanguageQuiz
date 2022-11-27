import csv
import random


class Quiz:

    def __init__(self, file):
        self.file = file
        self.dictionary = dict()
        self.read_csv_file()
        self.random_key_list = list(self.dictionary.items())
        random.shuffle(self.random_key_list)
        self.index = 0
        self.question = ''
        self.answer = ''
        self.alternatives = ['', '', '']
        self.questions_left = -1

    def read_csv_file(self):
        with open(self.file) as f:
            csv_reader = csv.reader(f, delimiter=';')
            for row in csv_reader:
                self.dictionary[row[0]] = row[1]

    def next_question(self):
        if self.more_questions():
            self._set_questions_left()
            self._set_question()
            self._set_answer()
            self._set_alternatives()

    def _set_questions_left(self):
        self.questions_left = len(self.dictionary) - self.index

    def _set_question(self):
        self.question = self.random_key_list[self.index][0]
        self.index += 1

    def _set_answer(self):
        self.answer = self.dictionary[self.question]

    def _set_alternatives(self):
        alt1, alt2 = self.answer, self.answer
        while alt1 == self.answer or alt2 == self.answer or alt1 == alt2:
            alt1 = self.dictionary[self.random_key_list[random.randrange(len(self.dictionary))][0]]
            alt2 = self.dictionary[self.random_key_list[random.randrange(len(self.dictionary))][0]]
        self.alternatives = [self.answer, alt1, alt2]
        random.shuffle(self.alternatives)

    def more_questions(self):
        if self.index < len(self.dictionary):
            return True
        else:
            return False


