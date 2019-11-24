+\[>++>++<<-]]  triple the current cell into the next two cells
++\[>++<-]>|/]  double the current cell into the next cell and call the next lambda
/   Load the value 48 into cell 4 and 5
>>>,    take an input into cell 3
>[<->-]< subtract cell 4 from cell 3
[   while the value of cell 0 is non zero
    >>+.-<<   output the char at cell 5 plus 1 (1)
]
>>.    output the char at cell 5 (0)
