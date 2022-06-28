
class Queue:
    def __init__(self):
        self._list = []
        self._size = 0
    def enqueue(self, value):
        self._list.append(value)
        self._size += 1
    def dequeue(self, value):
        item = self._list.pop(0)
        self._size -= 1
        return item
    @property
    def size(self):
        return self._size
    @property
    def empty(self):
        return self.size == 0
    