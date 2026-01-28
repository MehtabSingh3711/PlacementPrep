
class DLLNode:
    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id
        self.prev = None
        self.next = None

class RecentChatManager:
    def __init__(self):
        self.node_map = {} 
        self.head = None
        self.tail = None

    def access_conversation(self, conversation_id: str):
        if conversation_id in self.node_map:
            self._move_to_head(self.node_map[conversation_id])
        else:
            new_node = DLLNode(conversation_id)
            self.node_map[conversation_id] = new_node
            self._add_to_head(new_node)

    def _add_to_head(self, node: DLLNode):
        if not self.head:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

    def _move_to_head(self, node: DLLNode):
        if node == self.head:
            return
        
        if node == self.tail:
            self.tail = node.prev
            self.tail.next = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
        
        node.next = self.head
        node.prev = None
        if self.head:
            self.head.prev = node
        self.head = node

    def get_recent_conversation_ids(self) -> list:
        ids = []
        curr = self.head
        while curr:
            ids.append(curr.conversation_id)
            curr = curr.next
        return ids
