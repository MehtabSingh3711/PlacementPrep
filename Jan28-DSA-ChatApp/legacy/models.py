import time
from datastructures import RecentChatManager

class Message:
    def __init__(self, message_id: str, sender_id: str, text: str):
        self.message_id = message_id
        self.sender_id = sender_id
        self.text = text
        self.timestamp = time.time()

    def __repr__(self):
        t_str = time.strftime('%H:%M', time.localtime(self.timestamp))
        return f"[{t_str}] <{self.sender_id}>: {self.text}"

class Conversation:
    def __init__(self, conversation_id: str, is_group: bool = False, group_name: str = None):
        self.conversation_id = conversation_id
        self.participants = set() 
        self.is_group = is_group
        self.group_name = group_name
        self.messages = [] 

    def add_message(self, message: Message):
        self.messages.append(message)

    def add_participant(self, user_id: str):
        self.participants.add(user_id)

    def get_display_name(self, current_user_id: str, all_users_dict: dict) -> str:
        if self.is_group:
            return f"Group: {self.group_name}"
        else:
            for uid in self.participants:
                if uid != current_user_id:
                    other_user = all_users_dict.get(uid)
                    return f"Chat with {other_user.username if other_user else uid}"
            return "Just You" 

class User:
    def __init__(self, user_id: str, username: str, password: str):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.recent_chat_manager = RecentChatManager()

    def update_recent_chat(self, conversation_id: str):
        self.recent_chat_manager.access_conversation(conversation_id)
