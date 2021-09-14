// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@R2 //set RAM[2] = 0
M=0

@R1 //set D = RAM[1]
D=M 

@END // if RAM[1] = 0, end the program
D;JEQ 

@R0 //set D = RAM[0]
D=M

@END // if RAM[0] = 0, end the program
D;JEQ 

//@R0 set D = RAM[0]
//D=M 

@R00 //set new varible
M=D


(LOOP)
	@R2 //set D = RAM[2]
	D=M

	@R1 // add RAM[1] to D
	D=D+M

	@R2 // update D to RAM[2]
	M=D

	@R00 //reduce 1 from the varible
	M=M-1

	@R00 // set D = varible
	D=M

	@END // if the varible = 0, end the program
	D;JEQ

	@LOOP // else go to the loop again
	0;JMP

(END)
//	@END
//	0;JMP
