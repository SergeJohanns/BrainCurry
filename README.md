# BrainCurry | A BrainFamily language with lambdas

BrainCurry is a Brainf\*ck derivative named after Haskell Curry. The idea is to make a semi-functional variant of Brainf\*ck by introducing lambdas. These lambdas are function objects that themselves hold BrainCurry code, and they can be defined and called in the middle of regular code as needed.

## Lambdas are not subroutines
The reason I refer to these function objects as lambdas, and not as functions, methods or subroutines, is that they do not behave as functions in imperative languages do. Although they are not pure expressions as the functional paradigm requires, they are as close as seemed reasonable given the structure of Brainf*ck.

The idea of a lambda is that it returns a tape state, that then becomes the new global tape state. Although a lambda can change the tape state and perform IO globally, all other variables are constrained in scope. A lambda can move its cell pointer, but not the *global* cell pointer. Lambdas can be defined inside of a lambda, but this new inner lambda will not be available in the global scope.

This constraint in side-effects does not make BrainCurry a purely functional language by far, since imperative design is strongly inherent to the structure of the parent language Brainf\*ck. However, BrainCurry is meant to be a sensible interpretation of functional programming in the context of Brainf\*ck.

## Inside of a lambda
The behaviour of the language inside of a lambda definition is the same as outside of one. The only changed behaviour when compared to simply inserting the lambda code manually is the previously mentioned change of scope.

Although the previous section compared the scope of the global program and a defined lambda, the same difference in scope applies to an arbitrary lambda and a lambda nested inside of it. A lambda defined in an inner lambda will not be available in the outer lambda, and the cell pointer in the outer lambda cannot be moved by the inner lambda. An inner lambda does, however, change the memory tape of the outer lambda. In this sense, a defined lambda as a contained system behaves as a regular BrainCurry program.

## Syntax differences
All existing Brainf\*ck characters are present and their existing functionality remains. This means all valid Brainf\*ck code is also valid BrainCurry code. To support the lambda functionality, three new characters have been added and one has been extended.

- `\` signifies the start of a lambda definition.
- `]` has been extended to signify the end of a lambda definition.
- `/` calls the currently indicated lambda.
- `|` discards the currently indicated lambda.

How to indicate lambdas is discussed in the next section.

## The lambda stack
When a lambda is defined, it is pushed onto the 'lambda stack'. This is a infinite stack datastructure holding all available lambdas. The lambda can be pushed onto the stack a variable amount of times, however. the number of  copies of the lambda end up on the stack is equal to the value of the currently indicated memory cell, unless that value is 0. If the value of the cell is 0, the lambda is pushed onto the stack an infinite number of times, effectively erasing all other lambdas.

The stack is initialised with an infinite number of instances of the identity function `\]`. This guarantees the stack will never be empty. The identity functions can be 'cleared' with an infinite push, replacing any finitely accessible instances by some other lambda.

When the `/` character is used and a lambda is called, the top lambda is popped off of the stack and executed. This means the next call will execute the lambda below that, etc. There is an exception to this: the lambda recieves its own, local lambda stack to work with. This stack is a copy of the global lambda stack *before* the lambda was called, meaning the called lambda has itself as a top lambda in the stack. This facilitates arbitrary recursion.

A lambda can still call previous lambdas without calling itself first (which would cause infinite recursion) by first discarding itself. This is one of the reasons for the inclusion of a discarding operator. Discarding a lambda simply pops that lambda off of the stack without calling it.

## Code examples
One useful advantage of lambda definitions is shared with regular subroutines: simply reusing code. Altough Brainf\*ck loops help with this, lambdas add a simple way to repeat a block of code *n* times for an arbitrary *n*. They also allow repeating code with more abstraction.

An example is a way to increment *n* following cells. Assuming the current cell has value *n*, the code
`\>+|/]/` will create *n* instances of a lambda that increments the cell pointer by one, increments that cell by one, discards the current lambda then calls the next lambda. After this, it will call the top lambda. This lambda will increment the next cell, then call the next lambda which increments the cell after that, etc. The final instance of the lambda will call the lambda after that, which can be set to the identity function `\]` if it is not already.

Another interesting possibility is to move *n* spaces to the right across a series of non-empty cells. This can be shortened through the recursive nature of lambdas. Although lambdas cannot move the cell pointer directly, they can set a 'flag' remotely, that can then be used to move to the cell. Thus, the code `\[-]]\>|/]/[>]` first defines a lambda that clears a cell, then defines a lambda that moves to the next cell and calls the next lambda, then calls the top lambda and finally moves to the next cleared cell. This sets a cleared cell 'flag' *n* cells away, which allows the pointer to move to it with only 14 characters of code.

Note that the construct `\>_|/]`, although used somewhat mundanely here, essentially allows the mapping of the function at `_` over the *n* following cells.

## Implementation
Although this repository is mostly meant to show the language itself, I have provided a Python-written interpreter to give a demonstration of BrainCurry as a language. It implements all aspects of the language, and it *should* do so in a stable manner. Of course, In an ideal world I would have delivered an implementation in Haskell, but that can come later.

Meanwhile, I invite everyone interested in the language to make their own inplementation in whatever language they fancy. It should not be hard to produce something faster than my implementation, because my implementation is a Python-written interpreter that handles *everything* at runtime, without any preprocessing at all.