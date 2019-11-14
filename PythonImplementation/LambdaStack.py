class LambdaStack:
    """This iterator class implements an infinite stack of function objects stored by the
    BrainCurry program. It is initialised as an infinite stack of identity functions. """

    def __init__(self):
        self.stack = [] # The finite head of the stack
        self.base = "" # The infinite tail of the stack

        self.stash = [] # A stack to stash state data on for state reversion
    
    def __str__(self):
        return ','.join(
            ["'{}'".format(x) for x in (
                list(reversed(self.stack)) + [self.base]
            )]
        ) + "..."

    # Stashes and restores the head and tail to prevent lambdas from changing them globally
    def Stash(self): self.stash.append((self.stack[::], self.base))
    def Restore(self): (self.stack, self.base) = self.stash.pop()


    def pop(self):
        """Pop the top element off of the stack."""
        return self.stack.pop() if self.stack else self.base

    def push(self, target, amount):
        """Push an element onto the stack a given amount of times."""
        if amount > 0:
            self.stack += [target]*amount
        else: # Infinite times
            self.stack = []
            self.base = target