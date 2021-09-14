
@R15 
M=0 // the temp answer
@R1 
M=1

@R13
D=M 
@R2 // temp R13
M=D

@R14 
D=M
@R3 //temp R14
M=D

@R4 //counter
M=0

(STARTLOOP) // checking if R14 is bigger then R13
	@R2
	D=M
	@R3
	D=D-M
	@END
	D;JLT

(DIVILOOP) 
	@R2
	D=M
	@R3
	D=D-M
	@NEGETIVELOOP //jump if the R2-R3 is less then 0
	D;JLE
	@R3
	M=M<<
	@R4
	M=M+1
	@DIVILOOP
	0;JMP


(NEGETIVELOOP)
	@R4
	M=M-1
	D=M
	@ENDCOUNT // jump if R4 (the counter) is 0 or less
	D;JLE
	@R1
	M=M<< //shift left
	//@R4
	@NEGETIVELOOP
	0;JMP

(ENDCOUNT)
	@R1
	D=M
	@R15
	M=M+D
	@R3
	D=M>> //shift right
	@R2
	M=M-D
	@R14
	D=M
	@R3
	M=D
	@R1
	M=1
	@STARTLOOP
	0;JMP

(END)
