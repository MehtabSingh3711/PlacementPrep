import sys
import time
import pickle
import os

from datastructures import RecentChatManager
from models import User, Conversation, Message

class ChatApp:
    def __init__(self):
        self.users = {}             
        self.conversations = {}     
        self.usernames_map = {}     
        
        self.private_chat_map = {} 
        self.current_user = None
        self.user_id_counter = 1
        self.conversation_id_counter = 1
        self.message_id_counter = 1
        
        self.load_data()

    def _generate_user_id(self):
        uid = f"u{self.user_id_counter}"
        self.user_id_counter += 1
        return uid

    def _generate_conversation_id(self):
        cid = f"c{self.conversation_id_counter}"
        self.conversation_id_counter += 1
        return cid

    def _generate_message_id(self):
        mid = f"m{self.message_id_counter}"
        self.message_id_counter += 1
        return mid

    def save_data(self):
        data = {
            'users': self.users,
            'conversations': self.conversations,
            'usernames_map': self.usernames_map,
            'private_chat_map': self.private_chat_map,
            'counters': {
                'user': self.user_id_counter,
                'conversation': self.conversation_id_counter,
                'message': self.message_id_counter
            }
        }
        try:
            with open('chitchat_data.pkl', 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self):
        if os.path.exists('chitchat_data.pkl'):
            try:
                with open('chitchat_data.pkl', 'rb') as f:
                    data = pickle.load(f)
                    self.users = data.get('users', {})
                    self.conversations = data.get('conversations', {})
                    self.usernames_map = data.get('usernames_map', {})
                    self.private_chat_map = data.get('private_chat_map', {})
                    
                    counters = data.get('counters', {})
                    self.user_id_counter = counters.get('user', 1)
                    self.conversation_id_counter = counters.get('conversation', 1)
                    self.message_id_counter = counters.get('message', 1)
                print("Previous session data loaded.")
            except Exception as e:
                print(f"Error loading data: {e}")
        
        if self.current_user:
            if self.current_user.user_id in self.users:
                self.current_user = self.users[self.current_user.user_id]
            else:
                self.current_user = None

    def register(self):
        print("\n--- REGISTER ---")
        username = input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty.")
            return
        if username in self.usernames_map:
            print("Username already taken.")
            return
        
        password = input("Enter password: ").strip()
        if not password:
            print("Password cannot be empty.")
            return
        
        user_id = self._generate_user_id()
        new_user = User(user_id, username, password)
        self.users[user_id] = new_user
        self.usernames_map[username] = user_id
        print(f"User registered successfully! ID: {user_id}")
        self.save_data()

    def login(self):
        self.load_data() 
        print("\n--- LOGIN ---")
        username = input("Enter username: ").strip()
        if username not in self.usernames_map:
            print("User not found.")
            return

        password = input("Enter password: ").strip()
        user_id = self.usernames_map[username]
        user = self.users[user_id]

        if user.password == password:
            self.current_user = user
            print(f"Welcome back, {user.username}!")
        else:
            print("Invalid password.")

    def logout(self):
        if self.current_user:
            print(f"Goodbye, {self.current_user.username}!")
            self.current_user = None

    def view_all_users(self):
        print("\n--- ALL USERS ---")
        for uid, u in self.users.items():
            if self.current_user and uid == self.current_user.user_id:
                print(f"{u.username} (You)")
            else:
                print(f"{u.username}")

    def start_one_to_one(self):
        self.load_data()
        print("\n--- START 1-ON-1 CHAT ---")
        potential_users = [u for u in self.users.values() if u.user_id != self.current_user.user_id]
        if not potential_users:
            print("No other users registered yet.")
            return

        print("Select a user to chat with:")
        for i, user in enumerate(potential_users):
            print(f"{i+1}. {user.username}")
        
        choice = input("\nEnter number (or 0 to cancel): ").strip()
        if not choice.isdigit():
            print("Invalid input.")
            return
            
        idx = int(choice)
        if idx == 0:
            return
        if not (1 <= idx <= len(potential_users)):
            print("Invalid selection.")
            return

        target_user = potential_users[idx-1]
        target_uid = target_user.user_id
        target_username = target_user.username

        pair_key = frozenset({self.current_user.user_id, target_uid})
        if pair_key in self.private_chat_map:
            cid = self.private_chat_map[pair_key]
            self._open_chat(cid)
        else:
            cid = self._generate_conversation_id()
            conv = Conversation(cid, is_group=False)
            conv.add_participant(self.current_user.user_id)
            conv.add_participant(target_uid)
            
            self.conversations[cid] = conv
            self.private_chat_map[pair_key] = cid
            
            self.users[self.current_user.user_id].update_recent_chat(cid)
            self.users[target_uid].update_recent_chat(cid)
            
            print(f"New chat created with {target_username}.")
            self._open_chat(cid)
            self.save_data()

    def create_group_chat(self):
        self.load_data()
        print("\n--- CREATE GROUP CHAT ---")
        group_name = input("Enter group name: ").strip()
        if not group_name:
            print("Group name required.")
            return

        potential_users = [u for u in self.users.values() if u.user_id != self.current_user.user_id]
        
        if not potential_users:
            print("No other users to add.")
            return

        print("Select users to include (comma separated numbers, e.g., 1,3):")
        for i, user in enumerate(potential_users):
            print(f"{i+1}. {user.username}")
            
        choice_str = input("\nEnter numbers: ").strip()
        if not choice_str:
            print("No users selected.")
            return

        choices = choice_str.split(',')
        selected_uids = {self.current_user.user_id}
        selected_names = []

        for c in choices:
            c = c.strip()
            if c.isdigit():
                idx = int(c)
                if 1 <= idx <= len(potential_users):
                    user = potential_users[idx-1]
                    selected_uids.add(user.user_id)
                    selected_names.append(user.username)
        
        if len(selected_uids) < 2:
            print("Need at least 2 participants (including yourself).")
            return

        cid = self._generate_conversation_id()
        conv = Conversation(cid, is_group=True, group_name=group_name)
        for uid in selected_uids:
            conv.add_participant(uid)
            self.users[uid].update_recent_chat(cid)

        self.conversations[cid] = conv
        print(f"Group '{group_name}' created with members: {', '.join(selected_names)} and You.")
        self.save_data()

    def view_recent_chats(self):
        self.load_data()
        print("\n--- RECENT CHATS ---")
        recent_cids = self.current_user.recent_chat_manager.get_recent_conversation_ids()
        
        if not recent_cids:
            print("No recent conversations.")
            return

        print(f"Found {len(recent_cids)} recent chats.")
        indexed_cids = []
        for i, cid in enumerate(recent_cids):
            conv = self.conversations.get(cid)
            if conv:
                name = conv.get_display_name(self.current_user.user_id, self.users)
                print(f"{i+1}. {name}")
                indexed_cids.append(cid)
            else:
                print(f"{i+1}. [Unknown Conversation]") 

        choice = input("\nEnter number to open chat (or 0 to go back): ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(indexed_cids):
                self._open_chat(indexed_cids[idx-1])

    def _open_chat(self, conversation_id: str):

        while True:
            conv = self.conversations.get(conversation_id)
            if not conv:
                print("Error: Conversation not found.")
                return

            print(f"\n<<< {conv.get_display_name(self.current_user.user_id, self.users)} >>>")
            
            if not conv.messages:
                print("[No messages yet]")
            else:
                for msg in conv.messages:
                    sender = self.users.get(msg.sender_id)
                    sender_name = sender.username if sender else "Unknown"
                    t_str = time.strftime('%H:%M:%S', time.localtime(msg.timestamp))
                    print(f"[{t_str}] {sender_name}: {msg.text}")

            print("\nOptions: [S]end message, [R]efresh, [B]ack")
            action = input("> ").strip().upper()
            
            if action == 'S':
                text = input("Message: ").strip()
                if text:
                    self._send_message(conv, text)
            elif action == 'R':
                self.load_data()
                continue
            elif action == 'B':
                break
            else:
                print("Invalid option.")

    def _send_message(self, conversation: Conversation, text: str):
        mid = self._generate_message_id()
        msg = Message(mid, self.current_user.user_id, text)
        conversation.add_message(msg)
        
        for participant_id in conversation.participants:
            if participant_id in self.users:
                self.users[participant_id].update_recent_chat(conversation.conversation_id)
        
        print("Message sent.")
        self.save_data()

    def run(self):
        print("Initializing CHITCHAT v1.0...")
        while True:
            if not self.current_user:
                print("\n=== CHITCHAT LOGIN MENU ===")
                print("1. Register")
                print("2. Login")
                print("3. View All Users (Debug)")
                print("4. Exit")
                
                choice = input("Select: ").strip()
                if choice == '1':
                    self.register()
                elif choice == '2':
                    self.login()
                elif choice == '3':
                    self.view_all_users()
                elif choice == '4':
                    print("Exiting...")
                    self.save_data()
                    sys.exit()
                else:
                    print("Invalid choice.")
            else:
                print(f"\n=== HOME: {self.current_user.username} ===")
                print("1. View Recent Chats")
                print("2. Start One-to-One Chat")
                print("3. Create Group Chat")
                print("4. View All Users")
                print("5. Logout")
                
                choice = input("Select: ").strip()
                if choice == '1':
                    self.view_recent_chats()
                elif choice == '2':
                    self.start_one_to_one()
                elif choice == '3':
                    self.create_group_chat()
                elif choice == '4':
                    self.view_all_users()
                elif choice == '5':
                    self.logout()
                else:
                    print("Invalid choice.")

if __name__ == "__main__":
    app = ChatApp()
    app.run()
