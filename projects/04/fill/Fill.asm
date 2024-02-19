// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// Adapted to JCE course, 2024a edition
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.


(CHECK_INPUT)
    // Set current to first screen pixel map.
    @SCREEN
    D=A
    @current
    M=D

    
    @KBD
    D=M

    //fillvalue contain -1 if type in the keyboard (KBD not equal 0), else 0
    @fillvalue
    M=-1
    @FILL
    D;JNE
    // Otherwise, clear the screen.
    @fillvalue
    M=0


// fill the screen in black or white
(FILL)
        
        @fillvalue
        D=M
        //A contains the current pixel address
        @current
        A=M
        //M = D ,fill the current pixel in black or white 
        M=D

        // If current pixel map is last pixel map there is nothing right to draw, so
        //jump back to keyboard check.
        @current
        D=M
        @24575
        D=D-A
        @CHECK_INPUT
        D;JGE 

        // Decrement current pixel map.
        @current
        M=M+1
        // Continue filling next pixel map.
        @FILL
        0;JMP    

        











