// file Sort.asm
@R15
D=M

@i // the counter of the loop1
M=D-1

@j // the counter of the loop2
M=D

@counter // the counter of the pointer in the array
M=0

(LOOP1) // the external loop of the bubble sort 
    
    @R15
    D=M

    @i // to set the i counter every loop2
    M=D-1

    @counter //to set the pointer to zero 
    M=0

    @j // to incres the j counter of loop2
    M=M-1
    D=M

    @END // to end the program if j is zero
    D;JEQ


(LOOP2) // the inner loop of the bubble sort
    @counter 
    D=M

    @R15
    D=D-M

    @LOOP1 // to end the loop if the pointer point to the end of the array 
    D;JEQ

    @counter
    D=M

    @R14
    D=D+M
    A=D
    D=M

    @sum1 // set the value in the array[counter]
    M=D
    
    @counter
    D=M

    @R14
    D=D+M
    D=D+1
    A=D
    D=M

    @sum2 // set the value un the array[counter+1]
    M=D

    @sum2
    D=M

    @sum1
    D=D-M

    @REPLACE // if sum1 > sum2 we replace them
    D;JGT

    (CON)

    @counter
    M=M+1

    @i
    M=M-1
    D=M

    @LOOP2 // check in need more iterations for LOOP1
    D;JGT

    @LOOP1 // start loop1 again
    0;JMP


(REPLACE) // replace twe value if needed

    @counter
    D=M

    @R14
    D=D+M

    @address_a
    M=D

    @address_b
    M=D+1
    A=M
    D=M

    @temp // temp for b
    M=D

    @address_a
    A=M
    D=M

    @address_b // put the value of a in the b place
    A=M
    M=D

    @temp
    D=M

    @address_a // put the value of b in a place
    A=M
    M=D

    @CON
    0;JMP

(END)

