class Stack:
    def __init__(self,capacity):
        self.capacity = capacity
        self.data = []

    def isEmpty(self):
        return len(self.data) == 0
    
    def isFull(self):
        return len(self.data) == self.capacity
    
    def push(self, val):
        if len(self.data) == self.capacity:
            raise OverflowError("Stack is Full")
        self.data.append(val)

    def pop(self):
        if not self.data:
            raise IndexError("Stack is Empty")
        return self.data.pop()
    
    def peek(self):
        if not self.data:
            raise IndexError("Stack is Empty")
        return self.data[-1]
    
    def size(self):
        return len(self.data)
    
    def reset(self,arr):
        self.data = arr[:]

ss = Stack(5)
ss.push(5)
ss.push(4)
ss.push(3)
ss.push(2)
ss.push(1)
# ss.push(0)
# ss.pop()
print(ss.peek())
print(ss.size())
ss.reset([0,1,2,3,4])
print(ss.peek())
