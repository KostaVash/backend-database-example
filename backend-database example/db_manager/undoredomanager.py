"""
this class stores the set/unset and provides undo/redo functionality
using 2 lists 1 for undo opertaions and the second one is for redo operations
"""


class UndoRedoManager:
    def __init__(self):
        self.undo = list()
        self.redo = list()

    def write(self, func, name, value, prev_value):
        x = (func, name, value, prev_value)
        self.undo.append(x)

    def get_undo(self):
        if not len(self.undo):
            return None, None, None
        x = self.undo.pop()
        self.redo.append(x)
        return x[0], x[1], x[3]

    def get_redo(self):
        if not len(self.redo):
            return None, None, None
        x = self.redo.pop()
        self.undo.append(x)
        return x[0], x[1], x[2]
