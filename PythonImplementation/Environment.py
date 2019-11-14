class Environment:
    """This class emulates an infinite BrainCurry environment,
    including a memory tape and a pointer to the current cell."""

    def __init__(self, max):
        self.max = max
        self.tape = Tape()
        self.pointer = 0

        self.stash = [] # A stack to stash state data on for reversion

    # Stashes the cell pointer to prevent lambdas from changing it globally
    def Stash(self): self.stash.append(self.pointer)
    def Restore(self): self.pointer = self.stash.pop()


    def ChangeCell(self, delta):
        self.cell += delta

    def SetCell(self, value):
        self.cell = value

    def ChangePointer(self, delta):
        self.pointer += delta
        if self.pointer < self.tape.leftMost:
            self.tape.extendleft([0]*(self.tape.leftMost - self.pointer))
        elif self.pointer > self.tape.rightMost:
            self.tape.extend([0]*(self.pointer - self.tape.rightMost))

    @property
    def cell(self):
        return self.tape[self.pointer]
    @cell.setter
    def cell(self, value):
        self.tape[self.pointer] = value % self.max


class Tape:
    """This iterable class mimics infinite memory tape
    for the environment class to use internally."""

    def __init__(self):
        self.left = []
        self.right = [0]

    def __getitem__(self, index):
        return self.right[index] if index >= 0 else self.left[abs(index)-1]

    def __setitem__(self, index, value):
        (self.right if index >= 0 else self.left)[index if index >= 0 else abs(index)-1] = value

    def __len__(self):
        return len(self.right) + len(self.left)

    def __str__(self):
        return str(
            list(reversed(self.left)) + self.right
        )
    

    @property
    def leftMost(self):
        """Return the leftmost (lowest) index still on the generated tape."""
        return -len(self.left)
    @property
    def rightMost(self):
        """Return the rightmost (highest) index still on the generated tape."""
        return len(self.right) - 1
    

    def extend(self, iterable):
        self.right += iterable

    def extendleft(self, iterable):
        self.left += iterable