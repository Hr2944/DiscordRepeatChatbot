from answer import AnswerFinder, AnswersLoader
from session import ConversationSessions


class ChatBot:
    def __init__(self, question, for_username):
        self.question = question
        self.sessions = ConversationSessions()
        self.username = for_username
        self.answer_finder = AnswerFinder(question)
        self.answers_loader = AnswersLoader()

    def should_repeat(self):
        return self.answer_finder.find_answer() is None

    def respond(self):
        if self.is_answering_after_unknown_answer():
            self.save_question_as_answer_to_next_to_last_question()

        if self.should_repeat():
            return self.repeat()
        else:
            return self.answer_memoized()

    def repeat(self):
        return self.question

    def is_answering_after_unknown_answer(self):
        last_bot_message = self.sessions.get_bot_message(self.username, -1)
        next_to_last_user_message = self.get_next_to_last_user_message()
        return last_bot_message == next_to_last_user_message and last_bot_message is not None

    def get_next_to_last_user_message(self):
        return self.sessions.get_user_message(self.username, -2)

    def save_question_as_answer_to_next_to_last_question(self):
        self.answers_loader.save_answer(
            question=self.get_next_to_last_user_message(),
            answer=self.question
        )

    def answer_memoized(self):
        return self.answer_finder.find_answer()
