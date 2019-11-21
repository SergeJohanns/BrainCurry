Fibonacci following the sequence 0 1 1 2 3 5 etc where the 0 is at index 0
Implemented by storing the current and next number and repeatedly using those to construct the next fibonacci number

>>+<<   set cell 2 to be 1
\   declare a lambda to move to the next two fibonacci numbers
    >>[>+>+<<-] clone cell 2 to cell 3 and 4
    <[>+<-] add cell 1 to cell 2
    >>[<+>-] add cell 3 to cell 2
    >[<<<+>>>-] move cell 4 to cell 1
]   push the lambda infinitely many times
,   input a number
[   while there are still rounds left to go
    /   move to the next fibonacci number
-]  decrement the counter and jump back

The computation is complete