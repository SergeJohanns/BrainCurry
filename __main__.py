#!/usr/bin/env python3

# I did not plan this out at all and it is the most satisfying thing I've ever seen.
from Environment import Environment
from LambdaStack import LambdaStack
from CommandLine import CommandLine
from Interpreter import Interpreter

class Main:
    """Main execution class. Also servers as a bridge between the View and Controller and the Model."""

    def Main(self):
        """Initialise the system."""
        self.commandLine = CommandLine(self, "> ")
        self.interpreter = self.MakeInterpreter()
        self.commandLine.Splash()
        self.commandLine.Run()

    def MakeInterpreter(self):
        return Interpreter(
            Environment(256), # Initialise the environment with 8-bit cells
            LambdaStack(),
            self.commandLine
        )


    def Quit(self, command):
        raise SystemExit

    def Reset(self, command):
        del self.interpreter
        self.interpreter = self.MakeInterpreter()
        self.commandLine.Log("Sucessfully reset interpreter.")
    
    def State(self, command):
        self.commandLine.LogState(
            self.interpreter.state.tape,
            (self.interpreter.state.pointer, self.interpreter.state.tape.leftMost, self.interpreter.state.tape.rightMost),
            self.interpreter.stack,
            command.split(' ')
        )
    
    def RunFile(self, command):
        files = command.split(' ')
        for file in files:
            try:
                with open(file, 'r') as scriptFile:
                    script = scriptFile.read()
            except:
                self.commandLine.Log("Could not open file '{}'".format(file))
            else:
                self.Run(script)
    
    def Run(self, code):
        try:
            self.interpreter.Execute(code)
        except Exception as e:
            self.commandLine.Log(e)


if __name__ == "__main__":
    main = Main()
    main.Main()