from Exceptions import UnmatchedScopeDesignator

class Interpreter:
    """This class interprets BrainCurry code in string format, and
    performs the corresponding mutations on an internal environment."""

    def __init__(self, environment, lambdaStack, controlview):
        self.state = environment # Assign the tape and cell pointer
        self.stack = lambdaStack # Assign the lambda stack
        self.controlview = controlview # Assign the class responsible for interacting with the user (and violate MCV in the process)
        
        self.commands = {
            '>':(self.state.ChangePointer, 1), '<':(self.state.ChangePointer, -1),
            '+':(self.state.ChangeCell, 1), '-':(self.state.ChangeCell, -1),
            '[':(self.Jump, None), ']':(self.JumpBack, None),
            ',':(self.Read, None), '.':(self.Show, None),
            '\\':(self.Lambda, None), '/':(self.LambdaExecute, None), '|':(self.LambdaDiscard, None)
        }
    

    def Execute(self, code):
        self.point = 0 # Command pointer
        self.code = code # Holds the executing code
        while self.point < len(code):
            try:
                (function, argument) = self.commands[code[self.point]]
                if argument: function(argument)
                else: function()
            except KeyError: pass # If the character is not in the command character set   #TODO: rewrite to try: finally after weeding out bugs
            self.point += 1
    

    def Jump(self):
        if self.state.cell == 0:
            self.point = self.MatchingBracket(1)
    
    def JumpBack(self):
        if self.state.cell != 0:
            self.point = self.MatchingBracket(-1)
    

    def Read(self):
        self.state.SetCell(ord(self.controlview.readChar()))
    
    def Show(self):
        self.controlview.showChar(chr(self.state.cell))
    

    def Lambda(self):
        endchar = self.MatchingBracket(1)
        lambdaString = self.code[self.point+1:endchar]
        self.stack.push(lambdaString, self.state.cell) # Push the lambda to the stack n times corresponding to the value of the current cell
        self.point = endchar

    def LambdaExecute(self):
        lambdaString = self.stack.pop() # Fetch the lambda from the stack

        # Store the current states to restore to later (sandboxing the lamda)
        self.state.Stash()
        self.stack.Stash()
        point = self.point
        code = self.code

        self.stack.push(lambdaString, 1) # Push the lambda back onto the stack so it can call itself (but it has been excluded from the restored state)
        self.Execute(lambdaString) # Execute the code in the lambda

        # Restore to the pre-executed states
        self.state.Restore()
        self.stack.Restore()
        self.point = point
        self.code = code
    
    def LambdaDiscard(self):
        self.stack.pop() # Remove it from the stack
    

    def MatchingBracket(self, direction):
        i = self.point
        depth = direction
        while depth != 0 and 0 <= i + direction < len(self.code):
            i += direction
            if self.code[i] in {'[', '\\'}:
                depth += 1
            elif self.code[i] in {']'}:
                depth -= 1
        
        if depth != 0: raise UnmatchedScopeDesignator("unmatched scope designator in '{}'".format(self.code))
        
        return i