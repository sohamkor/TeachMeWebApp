class Queue(object):
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return len(self.items) == 0

    def enqueue(self, itemToAdd):
        self.items.insert(0, itemToAdd)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
