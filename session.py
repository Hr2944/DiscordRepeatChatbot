from singleton import singleton


@singleton
class ConversationSessions:
    def __init__(self):
        self.sessions: dict[str, UserAndBotConversation] = {}

    def add_session_message(self, username, user_message=None, bot_message=None):
        session = self.get_or_create_session(username)
        if user_message:
            session.push_user(user_message)
        if bot_message:
            session.push_bot(bot_message)

    def get_user_message(self, username, message_index):
        session = self.get_session(username)
        if not session:
            return None
        return session.get_user(message_index)

    def get_bot_message(self, username, message_index):
        session = self.get_session(username)
        if not session:
            return None
        return session.get_bot(message_index)

    def get_session(self, username):
        return self.sessions.get(username)

    def create_session(self, username):
        self.sessions[username] = UserAndBotConversation()
        return self.sessions[username]

    def get_or_create_session(self, username):
        session = self.get_session(username)
        if not session:
            return self.create_session(username)
        return session


class UserAndBotConversation:
    def __init__(self, history_size=10):
        self.user_session = MessageHistory(history_size)
        self.bot_session = MessageHistory(history_size)
        self.stack = ConversationHistory(history_size * 2)

    def push_user(self, message):
        self.user_session.push(message)
        self.stack.push_user(message)

    def push_bot(self, message):
        self.bot_session.push(message)
        self.stack.push_bot(message)

    def get_user(self, message_index):
        return self.user_session.get(message_index)

    def get_bot(self, message_index):
        return self.bot_session.get(message_index)


class ConversationHistory:
    def __init__(self, max_size=20):
        self.history = []
        self.max_size = max_size

    def push_user(self, message):
        self._push({"user": message})

    def push_bot(self, message):
        self._push({"bot": message})

    def _push(self, typed_message):
        if len(self.history) == self.max_size:
            self.history.pop(0)
        self.history.append(typed_message)


class MessageHistory:
    def __init__(self, max_size=10):
        self.history = []
        self.max_size = max_size

    def push(self, message):
        if len(self.history) == self.max_size:
            self.history.pop(0)
        self.history.append(message)

    def get(self, message_index):
        return self.history[message_index] if len(self.history) > abs(message_index) else None
