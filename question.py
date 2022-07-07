class QuestionSanitizeError(Exception):
    pass


class QuestionSanitizer:

    def __init__(self, message):
        self.question_prefix = "$question:"
        self.original_message = message
        self.sanitized_message = None

    def sanitize(self):
        if self.is_question():
            return self.get_question()
        raise QuestionSanitizeError(f"${self.original_message} is not a question")

    def is_sanitize_safe(self):
        try:
            self.sanitize()
            return True
        except QuestionSanitizeError:
            return False

    def is_question(self):
        return self.original_message.startswith(self.question_prefix)

    def get_question(self):
        if not self.sanitized_message:
            self.sanitized_message = self.original_message[len(self.question_prefix):]
        return self.sanitized_message
