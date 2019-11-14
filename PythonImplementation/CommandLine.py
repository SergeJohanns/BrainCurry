"""Here we go again."""

class CommandLine:
    """A class that produces and manages a command line for the user. Acts as a View and Controller."""

    def __init__(self, main, signature):
        self.main = main # Reference to the main controller for direct instructions.
        self.killed = False
        self.signature = signature
        self.flushInput = False
        self.commandChar = ":"
        self.commands = {
            'q':self.main.Quit, 'r':self.main.Reset,
            'h':self.Help,      'i':self.main.State,
            'l':self.main.RunFile
        }
        self.help = {
            'q':("", "Exit the interpreter"),
            'r':("","Reset the interpreter environment"),
            'h':("[command]","Display information about terminal commands"),
            'i':("[verbose flag]","Display information about the state of the interpreter environment"),
            'l':("filename", "Load an external script for execution")
        }


    def Run(self):
        while not self.killed:
            self.Parse(input(('\n' if self.flushInput else '') + self.signature))

    def Parse(self, command):
        self.flushInput = False
        if command and command[0] == self.commandChar and command[1:] and command[1] in self.commands:
            self.commands[command[1]](command[2:].strip())
        else:
            self.main.Run(command)
    

    def Splash(self):
        print("Experimental BrainCurry implementation in Python\n\nEnter :h for command list")

    def Log(self, message):
        print(message)

    def LogState(self, tape, pointer, stack, args):
        print("Memory tape: {}\nMemory pointer: {}\t(on tape indices [{}, {}])\nLambda stack: {}".format(
            tape if len(tape) < 50 or '-vm' in args or '-v' in args else "Memory tape too large (size: {}), use '-vm' or '-v' to display anyways.".format(len(tape)),
            *pointer,
            stack if len(stack.stack) < 30 or '-vl' in args or '-v' in args else "Lambda stack too large (finite portion size: {}), use '-vl' or '-v' to display anyways.".format(len(stack.stack))
        ))


    def Help(self, command):
        helpString = ":{} {: <16} | {}"
        show = [arg for arg in command.split(' ') if arg in self.help]
        if not show:
            show = self.help.keys()
        for com in show:
            print(helpString.format(com, *self.help[com]))
            show = True


    def showChar(self, char):
        print(char, end = "", flush=True)
        self.flushInput = True

    def readChar(self):
        self.flushInput = True
        return "{: >1}".format(
            input("")[:1]
        )