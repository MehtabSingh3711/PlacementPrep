class Array:
    def __init__(self,capacity):
        self.data = [None] * capacity
        self.capacity = capacity
        self.size = 0
    
    def traverse(self):
        for i in range(self.size):
            print(f"Index: {i} -> Element: {self.data[i]}")
    
    def search(self, target):
        for i in range(self.size):
            if target == self.data[i]:
                return i
        return -1
    
    def insert(self,index,value):
        if index < 0 or index > self.size:
            raise IndexError("Invalid Index")
        if self.size >= self.capacity:
            raise OverflowError("Array is Full")
        
        for i in range(self.size,index,-1):
            self.data[i] = self.data[i-1]
        
        self.data[index] = value
        self.size += 1

    def delete(self, index):
        if index < 0 or index > self.size:
            raise IndexError("Invalid Index")
        
        deleted = self.data[index]

        for i in range(index,self.size-1):
            self.data[i] = self.data[i+1]
        
        self.size -= 1
        return deleted
    
    def get(self, index):
        if index < 0 or index > self.size:
            raise IndexError("Invalid Index")
        return self.data[index]
    
    def set(self, index,value):
        if index < 0 or index > self.size:
            raise IndexError("Invalid Index")
        self.data[index] = value


arr = Array(5)
arr.insert(0,1)
arr.insert(1,2)
arr.insert(2,3)
arr.insert(3,4)
arr.insert(4,5)
arr.delete(2)
arr.traverse()
