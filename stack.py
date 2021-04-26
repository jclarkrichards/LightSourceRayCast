class Stack(object):
    def __init__(self):
        self.items = []  #You should not deal with items directly.  Use push and pop.
        
    def isEmpty(self):
        if len(self.items) > 0:
            return False
        return True
    
    def clear(self):
        self.items = []
        
    def push(self, item):
        self.items.append(item)
        
    def pop(self):
        if not self.isEmpty():
            removedItem = self.items.pop(len(self.items)-1)
            return removedItem
        return None
    
    def peek(self):
        if not self.isEmpty():
            return self.items[len(self.items)-1]
        return None

    def swap(self):
        '''Swap the top 2 items around'''
        if len(self.items) >= 2:
            item0 = self.pop()
            item1 = self.pop()
            self.push(item0)
            self.push(item1)

    
