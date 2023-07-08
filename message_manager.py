# message_manager.py

class MessageManager:
    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({
            "role": role,
            "content": content,
        })

    def get_messages(self):
        return self.messages
