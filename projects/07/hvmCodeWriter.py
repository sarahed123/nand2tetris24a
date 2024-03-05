"""
hvmCodeWriter.py -- Emits assembly language code for the Hack VM translator.
Skeletonized by Janet Davis March 2016
Refactored by John Stratton April 2017
Refactored by Janet Davis March 2019
Adapted to JCE course, 2020-2024a
"""

import os
from hvmCommands import *

# If debug is True,
# then the VM commands will be written as comments into the output ASM file.
debug = True


class CodeWriter(object):

    def __init__(self, outputName):
        """
        Opens 'outputName' and gets ready to write it.
        """
        self.file = open(outputName, 'w')
        self.setFileName(outputName)

        # used to generate unique labels
        self.labelNumber = 0
        self.functionName = ""

    def close(self):
        """
        Writes the terminal loop and closes the output file.
        """
        label = self._uniqueLabel()
        self._writeComment("Infinite loop")
        self._writeCode('(%s), @%s, 0;JMP' % (label, label))
        self.file.close()

    def setFileName(self, fileName):
        """
        Sets the current file name to 'fileName'.
        Restarts the local label counter.

        Strips the path and extension.  The resulting name must be a
        legal Hack Assembler identifier.
        """
        self.fileName = os.path.basename(fileName)
        self.fileName = os.path.splitext(self.fileName)[0]
        self.labelNumber = 0


    def _uniqueLabel(self):
        self.labelNumber += 1
        return "label" + str(self.labelNumber)

    def write(self, text):
        """
        Write directly to the file.
        """
        self.file.write(text)

    def _writeCode(self, code):
        """
        Writes Hack assembly code to the output file.
        code should be a string containing ASM commands separated by commas,
        e.g., "@10, D=D+A, @0, M=D"
        """
        
        code = code.replace(',', '\n').replace(' ', '')
        self.file.write(code + '\n')


    def _writeComment(self, comment):
        """
        Writes a comment to the output ASM file.
        """
        if (debug):
            self.file.write('    // %s\n' % comment)

    def _pushD(self):
        """
        Prepares Hack assembly code to push the value from the D register
        onto the stack.
        TODO - Stage I - see Figure 7.2
        """
        asm_code = "@SP, A=M, M=D, @SP, M=M+1"
        self._writeCode(asm_code)
        return asm_code
        # self.write('@SP') # Get current stack pointer
        # self.write('A=M') # Set address to current stack pointer
        # self.write('M=D') # Write data to top of stack
        # self.write('@SP') # Increment SP
        # self.write('M=M+1')

    def _popD(self):
        """"
        Prepares Hack assembly code to pop a value from the stack
        into the D register.
        TODO - Stage I - see Figure 7.2
        """
        asm_code = "@SP, M=M-1, A=M, D=M"
        self._writeCode(asm_code)
        return asm_code
        # self.write('@SP')
        # self.write('M=M-1') # Decrement SP
        # self.write('A=M') # Set address to current stack pointer
        # self.write('D=M') # Get data from top of stack

    
        '''Resolve address to A register'''
        addresses={
            'local': 'LCL', # Base R1
            'argument': 'ARG', # Base R2
            'this': 'THIS', # Base R3
            'that': 'THAT', # Base R4
            'pointer': 3, # Edit R3, R4
            'temp': 5, # Edit R5-12
            # R13-15 are free
            'static': 16, # Edit R16-255
        }
        address = addresses.get(segment)
        if segment == 'constant':
            self._writeCode('@' + str(index))
        elif segment == 'static':
            self._writeCode('@' + self.curr_file + '.' + str(index))
        elif segment in ['pointer', 'temp']:
            self._writeCode('@R' + str(address + int(index))) # Address is an int
        elif segment in ['local', 'argument', 'this', 'that']:
            self._writeCode('@' + address) # Address is a string
            self._writeCode('D=M')
            self._writeCode('@' + str(index))
            self._writeCode('A=D+A') # D is segment base
        else:
            raise ValueError('{} is an invalid argument'.format(segment))
  
    def writeArithmetic(self, command):
        """
        Writes Hack assembly code for the given command.
        """
        self._writeComment(command)

        if command in [T_ADD, T_SUB, T_AND, T_OR]:
            op = "+" if command == T_ADD else "-" if command == T_SUB else "&" if command == T_AND else "|"
            self._writeCode("@SP")
            self._writeCode("AM=M-1")
            self._writeCode("D=M")
            self._writeCode("A=A-1")
            self._writeCode(f"M=M{op}D")
        elif command in [T_NEG, T_NOT]:
            op = "-" if command == T_NEG else "!"
            self._writeCode("@SP")
            self._writeCode("A=M-1")
            self._writeCode(f"M={op}M")
        elif command in [T_EQ, T_GT, T_LT]:
            jump = "JEQ" if command == T_EQ else "JGT" if command == T_GT else "JLT"
            true_label = self._uniqueLabel()
            end_label = self._uniqueLabel()
            self._writeCode("@SP")
            self._writeCode("AM=M-1")
            self._writeCode("D=M")
            self._writeCode("A=A-1")
            self._writeCode("D=M-D")
            self._writeCode(f"@{true_label}")
            self._writeCode(f"D;{jump}")
            self._writeCode("D=0")
            self._writeCode(f"@{end_label}")
            self._writeCode("0;JMP")
            self._writeCode(f"({true_label})")
            self._writeCode("D=-1")
            self._writeCode(f"({end_label})")
            self._writeCode("@SP")
            self._writeCode("A=M-1")
            self._writeCode("M=D")
        else:
            raise ValueError('Bad arithmetic command')
             
    def writePushPop(self, commandType, segment, index):
        """
        Write Hack code for 'commandType' (C_PUSH or C_POP).
        'segment' (string) is the segment name.
        'index' (int) is the offset in the segment.
        """
        segmentMap = {
            "argument": "ARG",
            "local": "LCL",
            "this": "THIS",
            "that": "THAT"
        }
        if commandType == C_PUSH:
            self._writeComment("push %s %d" % (segment, index))
            if segment == T_CONSTANT:
                self._writeCode("@" + str(index))   # Load constant value
                self._writeCode("D=A")              # Set D to the constant value
            elif segment == T_STATIC:
                self._writeCode("@" + self.fileName + "." + str(index))  # Load static variable address
                self._writeCode("D=M")              # Set D to the value at that address
            elif segment == T_POINTER:
                self._writeCode("@" + str(3 + index))  # Load base address of THIS or THAT
                self._writeCode("D=M")              # Set D to the value at that address
            elif segment == T_TEMP:
                self._writeCode("@" + str(5 + index))  # Load base address of temp segment
                self._writeCode("D=M")              # Set D to the value at that address   
            else:  # argument, local, this, that
                self._writeCode("@" + segmentMap[segment])  # Load base address of segment
                self._writeCode("D=M")              # Set D to the value at that address
                self._writeCode("@" + str(index))   # Load index
                self._writeCode("A=D+A")            # Add index to base address
                self._writeCode("D=M")              # Set D to the value at that address
            self._pushD()    
        elif commandType == C_POP:
            self._writeComment("pop %s %d" % (segment, index))
            if segment == T_STATIC:
                self._popD()                        # Pop value from stack to D
                self._writeCode("@" + self.fileName + "." + str(index))  # Load static variable address
                self._writeCode("M=D")              # Set the value at that address to the value in D
            elif segment == T_POINTER:
                self._popD()                        # Pop value from stack to D
                self._writeCode("@" + str(3 + index))  # Load base address of THIS or THAT
                self._writeCode("M=D")              # Set the value at that address to the value in D
            elif segment == T_TEMP:
                self._popD()                        # Pop value from stack to D
                self._writeCode("@" + str(5 + index))  # Load base address of temp segment
                self._writeCode("M=D")              # Set the value at that address to the value in D
            else:  # argument, local, this, that
                self._writeCode("@" + segmentMap[segment])  # Load base address of segment
                self._writeCode("D=M")              # Set D to the value at that address
                self._writeCode("@" + str(index))   # Load index
                self._writeCode("D=D+A")            # Add index to base address
                self._writeCode("@R13")             # Load R13 (general-purpose register)
                self._writeCode("M=D")              # Store the calculated address in R13
                self._popD()                        # Pop value from stack to D
                self._writeCode("@R13")             # Load R13
                self._writeCode("A=M")              # Go to the address stored in R13
                self._writeCode("M=D")              # Set the value at that address to the value in D
        else:
            raise ValueError('Bad push/pop command')




    # Functions below this comment are for Project 08. Ignore for Project 07.
    def writeInit(self):
        """
        Writes assembly code that effects the VM initialization,
        also called bootstrap code. This code must be placed
        at the beginning of the output file.
        See p. 165, "Bootstrap Code"
        TODO - Stage IV
        """
        self._writeComment("Init")
        pass

    def writeLabel(self, label):
        """
        Writes assembly code that effects the label command.
        See section 8.2.1 and Figure 8.6.
        TODO - Stage III
        """
        self._writeComment("label %s" % (label))
        pass

    def writeGoto(self, label):
        """
        Writes assembly code that effects the goto command.
        See section 8.2.1 and Figure 8.6.
        TODO - Stage III
        """
        self._writeComment("goto %s" % (label))
        pass

    def writeIf(self, label):
        """
        Writes assembly code that effects the if-goto command.
        See section 8.2.1 and Figure 8.6.
        TODO - Stage III
        """
        self._writeComment("if-goto %s" % (label))
        pass

    def writeCall(self, functionName, numArgs):
        """
        Writes assembly code that effects the call command.
        See Figures 8.5 and 8.6.
        TODO - Stage IV
        """
        self._writeComment("call %s %d" % (functionName, numArgs))
        pass

    def writeReturn(self):
        """
        Writes assembly code that effects the return command.
        See Figure 8.5.
        TODO - Stage IV
        """
        self._writeComment("return")
        pass

    def writeFunction(self, functionName, numLocals):
        """
        Writes assembly code that effects the call command.
        See Figures 8.5 and 8.6.
        TODO - Stage IV
        """
        self._writeComment("function %s %d" % (functionName, numLocals))
        self.functionName = functionName  # For local labels
        pass


   