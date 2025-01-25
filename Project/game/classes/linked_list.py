class Cell:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, data):
        new_cell = Cell(data)
        if not self.head:
            self.head = new_cell
            return

        current_cell = self.head
        while current_cell.next:
            current_cell = current_cell.next

        current_cell.next = new_cell
        new_cell.prev = current_cell


class Queue:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def remove(self):
        return self.items.pop(0)

    def look(self, position):
        return self.items[position]

    def __len__(self):
        return len(self.items)