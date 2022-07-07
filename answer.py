import json


class AnswerFinder:
    def __init__(self, question):
        self.question = question
        self.answers_loader = AnswersLoader()
        self.answer_sets = self.answers_loader.load_all_answers()

    def find_all_answer(self):
        return [answer_set['answer'] for answer_set in self.answer_sets if answer_set['question'] == self.question]

    def find_answer(self):
        all_answers = self.find_all_answer()
        if len(all_answers) > 0:
            return all_answers[0]
        else:
            return None


class AnswersLoader:
    def __init__(self):
        self.save_filename = "answers.json"

    def load_all_answers(self):
        with open(self.save_filename, "r") as save_file:
            return json.load(save_file)

    def save_answer(self, question, answer):
        all_answers = self.load_all_answers()
        all_answers.append({"question": question, "answer": answer})
        with open(self.save_filename, "w") as save_file:
            json.dump(all_answers, save_file)
