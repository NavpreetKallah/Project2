class Cell:
    def __init__(self, data):
        self.data = data
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
