// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.


(START)
	@SCREEN // update D to be the adress of screen
	D=A

	@adress // varible adress = D
	M=D

	@8192 // update D to be the number of register of the screen
	D=A

	@i // i = D
	M=D

	@KBD // D = the adress of the keyboard
	D=M

	@OFF // if the adress of the keyboard is 0 than off 
	D;JEQ

	(ON) 
	    @adress 
	    A=M
	    M=-1 // RAM[adress] = -1
	    
	    @adress 
	    M=M+1 // update the adress to M+1

		@i 
		M=M-1 // update i to M-1
		D=M  

		@END
	    D;JEQ // go to END if i is 0
	    
	    @ON
	    0;JMP // else go to ON

	(OFF)
	    @adress
	    A=M
	    M=0 // RAM[adress] = 0

	    @adress
	    M=M+1 // update the adress to M+1

	    @i
	    M=M-1 // update i to M-1
	    D=M

	    @END
	    D;JEQ // go to END if i is 0

	    @OFF
	    0;JMP // else go to ON

(END)
	@START //infinite loop
	0;JMP