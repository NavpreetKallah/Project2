from typing import Any, Optional


class Cell:
    def __init__(self, data: Any) -> None:
        self.data: Any = data
        self.prev: Optional[Cell] = None
        self.next: Optional[Cell] = None


class LinkedList:
    def __init__(self) -> None:
        self.head: Optional[Cell] = None

    def add(self, data: Any) -> None:
        new_cell: Cell = Cell(data)
        if not self.head:
            self.head = new_cell
            return

        current_cell: Cell = self.head
        while current_cell.next:
            current_cell = current_cell.next

        current_cell.next = new_cell
        new_cell.prev = current_cell


class Queue:
    def __init__(self) -> None:
        self.items: list[Any] = []

    def add(self, item: Any) -> None:
        self.items.append(item)

    def remove(self) -> Any:
        return self.items.pop(0)

    def look(self, position: int) -> Any:
        return self.items[position]

    def __len__(self) -> int:
        return len(self.items)
