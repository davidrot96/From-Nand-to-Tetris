# david96,nataliy
import os
import sys

ARITHMETIC = "C_ARITHMETIC"
POP = "C_POP"
PUSH = "C_PUSH"
LABEL = "C_LABEL"
GOTO = "C_GOTO"
IF = "C_IF"
FUNCTION = "C_FUNCTION"
RETURN = "C_RETURN"
CALL = "C_CALL"
START_TEMP = 5
NAMES_OF_FILES = []


# x = "hi my name is {0} and i {1} yeas old".format("david", 24)
# print(x)

class parser:
    """
    the class is preparing the file/files to the translation
    """
    lineStrArray = []
    tempLineStrArray = []
    numLines = 0
    directory = ''
    folderName = ''
    commandTypes = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]

    def __init__(self, directory):
        """
        the constructor Initializing the files into the data base
        :param directory: the directory with the file/files to translate
        """
        self.directory = directory
        if (os.path.isfile(directory)):  # if the directory is a file
            self.folderName = os.path.splitext(self.directory)[0]
            with open(self.directory, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    addLine = line.split("\n")
                    self.tempLineStrArray.append(addLine[0])
            self.tempLineStrArray.append("ENDFILE")
            file.close()
        else:  # if the directory is not a file
            if os.path.isfile(os.path.basename(os.path.normpath(
                    directory))):  # if we are given the name of the file
                self.folderName = os.path.basename(os.path.normpath(directory))
            else:  # if we given the name of folder
                self.folderName = os.path.basename(os.path.normpath(directory))
            for filename in os.listdir(directory):
                if filename.endswith(".vm"):
                    with open(directory + "/" + filename, 'r') as file:
                        NAMES_OF_FILES.append(filename)
                        lines = file.readlines()
                        for line in lines:
                            addLine = line.split("\n")
                            self.tempLineStrArray.append(addLine[0])
                    self.tempLineStrArray.append("ENDFILE")
                    file.close()

    def cleanLines(self):
        """
        the function is cleaning the remarks from the file/files
        :return: update a new list with the commands
        """
        for line in self.tempLineStrArray:
            tempLine = line.split("//")
            if tempLine[0] != "":
                tempLine = tempLine[0].replace("\t", "")
                tempLine = tempLine.split(' ')
                temp2 = ''
                for word in tempLine:
                    if word != '':
                        temp2 += word
                        temp2 += ' '

                if temp2 != '':
                    temp2 = temp2[:-1]
                    lineTuple = (temp2, self.commandType(temp2))
                    self.lineStrArray.append(lineTuple)

    def commandType(self, line):
        """

        :param line: checks what type of command
        :return: the type command
        """
        cleanLine = line.split(' ')
        if cleanLine[0] in self.commandTypes:
            return ARITHMETIC
        if cleanLine[0] == "pop":
            return POP
        if cleanLine[0] == "push":
            return PUSH
        if cleanLine[0] == "label":
            return LABEL
        if cleanLine[0] == "goto":
            return GOTO
        if cleanLine[0] == "if-goto":
            return IF
        if cleanLine[0] == "function":
            return FUNCTION
        if cleanLine[0] == "return":
            return RETURN
        if cleanLine[0] == "call":
            return CALL
        if cleanLine[0] == "ENDFILE":
            return "ENDFILE"


class codeWriter:
    """
    the class translate from vm file and write to a asm file
    """
    sum = 0
    directory = ""
    DS_commands = []
    fileObject = ''
    name_of_file = ""
    counter = 0

    def __init__(self, directory, DS, name):
        """
        the constructor opens new file
        :param directory: the file/folder directory
        :param DS: the lines that needed to be translate
        :param name: the name of the file we need to write
        """
        self.directory = directory
        self.DS_commands = DS
        self.name_of_file = name
        if os.path.isfile(self.directory):
            self.fileObject = open(self.name_of_file + ".asm", 'w')
        else:
            self.fileObject = open(self.directory + "/" + self.name_of_file +
                                   ".asm", 'w')

        self.loop()
        self.close()

    def loop(self):

        self.fileObject.write("@256" + '\n')  # set SP=256
        self.fileObject.write("D=A" + '\n')
        self.fileObject.write("@SP" + '\n')
        self.fileObject.write("M=D" + '\n')

        coom = ('call Sys.init 0', 0)
        self.branchingCall(coom)

        for command in self.DS_commands:
            if command[1] == ARITHMETIC:
                self.writeArithmetic(command[0])
            elif command[1] == POP or command[1] == PUSH:
                self.writePushPop(command[0])
            elif command[1] == LABEL:
                self.brancing_label(command)
            elif command[1] == GOTO:
                self.brancing_goto(command)
            elif command[1] == IF:
                self.brancing_if(command)
            elif command[1] == CALL:
                self.branchingCall(command)
            elif command[1] == FUNCTION:
                self.branchingFuncion(command)
            elif command[1] == RETURN:
                self.branchingReturn(command)
            elif command[1] == "ENDFILE":
                self.counter += 1

    def writeArithmetic(self, command):
        """
        writing to the file according to the arithmetic command
        :param command: command to translate
        """
        self.fileObject.write("//" + command + '\n')
        if command == "add":
            self.fileObject.write("@SP" + '\n')
            self.fileObject.write("D=M-1" + '\n')
            self.fileObject.write("@y" + str(self.sum) + '\n')
            self.fileObject.write("M=D" + '\n')
            self.fileObject.write("D=D-1" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("M=D" + '\n')
            self.fileObject.write("@y" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=M" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("M=D+M" + '\n')
            self.fileObject.write("@SP" + '\n')
            self.fileObject.write("M=M-1" + '\n')
            self.sum += 1
        elif command == "sub":
            self.fileObject.write("@SP" + '\n')
            self.fileObject.write("D=M-1" + '\n')
            self.fileObject.write("@y" + str(self.sum) + '\n')
            self.fileObject.write("M=D" + '\n')
            self.fileObject.write("D=D-1" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("M=D" + '\n')
            self.fileObject.write("@y" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=M" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("M=M-D" + '\n')
            self.fileObject.write("@SP" + '\n')
            self.fileObject.write("M=M-1" + '\n')
            self.sum += 1
        elif command == "neg":
            self.fileObject.write("@SP" + '\n')
            self.fileObject.write("A=M-1" + '\n')
            self.fileObject.write("M=-M" + '\n')
        elif command == "eq":
            self.fileObject.write("@SP" + '\n')
            self.fileObject.write("D=M-1" + '\n')
            self.fileObject.write("@y" + str(self.sum) + '\n')
            self.fileObject.write("M=D" + '\n')
            self.fileObject.write("D=D-1" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("M=D" + '\n')

            self.fileObject.write("@y" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=M" + '\n')
            self.fileObject.write("@NEGY" + str(self.sum) + '\n')
            self.fileObject.write("D;JLT" + '\n')

            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=M" + '\n')
            self.fileObject.write("@CHECK" + str(self.sum) + '\n')
            self.fileObject.write("D;JGE" + '\n')
            self.fileObject.write("@NOTEQ" + str(self.sum) + '\n')
            self.fileObject.write("0;JMP" + '\n')

            self.fileObject.write("(NEGY" + str(self.sum) + ")" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=M" + '\n')
            self.fileObject.write("@CHECK" + str(self.sum) + '\n')
            self.fileObject.write("D;JLT" + '\n')
            self.fileObject.write("@NOTEQ" + str(self.sum) + '\n')
            self.fileObject.write("0;JMP" + '\n')

            self.fileObject.write("(CHECK" + str(self.sum) + ")" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=M" + '\n')
            self.fileObject.write("@y" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=D-M" + '\n')
            self.fileObject.write("@EQ" + str(self.sum) + '\n')
            self.fileObject.write("D;JEQ" + '\n')
            self.fileObject.write("@NOTEQ" + str(self.sum) + '\n')
            self.fileObject.write("0;JMP" + '\n')

            self.fileObject.write("(EQ" + str(self.sum) + ")" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("M=-1" + '\n')
            self.fileObject.write("@END" + str(self.sum) + '\n')
            self.fileObject.write("0;JMP" + '\n')

            self.fileObject.write("(NOTEQ" + str(self.sum) + ")" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("M=0" + '\n')
            self.fileObject.write("(END" + str(self.sum) + ")" + '\n')

            self.fileObject.write("@SP" + '\n')
            self.fileObject.write("M=M-1" + '\n')
            self.sum += 1
        elif command == "gt":
            self.fileObject.write("@SP" + '\n')
            self.fileObject.write("D=M-1" + '\n')
            self.fileObject.write("@y" + str(self.sum) + '\n')
            self.fileObject.write("M=D" + '\n')
            self.fileObject.write("D=D-1" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("M=D" + '\n')

            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=M" + '\n')
            self.fileObject.write("@POSX" + str(self.sum) + '\n')
            self.fileObject.write("D;JGE" + '\n')

            self.fileObject.write("@y" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=M" + '\n')
            self.fileObject.write("@CHECK" + str(self.sum) + '\n')
            self.fileObject.write("D;JLE" + '\n')
            self.fileObject.write("@XLY" + str(self.sum) + '\n')
            self.fileObject.write("0;JMP" + '\n')

            self.fileObject.write("(POSX" + str(self.sum) + ")" + '\n')
            self.fileObject.write("@y" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=M" + '\n')
            self.fileObject.write("@CHECK" + str(self.sum) + '\n')
            self.fileObject.write("D;JGE" + '\n')
            self.fileObject.write("@XGY" + str(self.sum) + '\n')
            self.fileObject.write("0;JMP" + '\n')

            self.fileObject.write("(CHECK" + str(self.sum) + ")" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=M" + '\n')
            self.fileObject.write("@y" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=D-M" + '\n')
            self.fileObject.write("@XGY" + str(self.sum) + '\n')
            self.fileObject.write("D;JGT" + '\n')
            self.fileObject.write("@XLY" + str(self.sum) + '\n')
            self.fileObject.write("0;JMP" + '\n')

            self.fileObject.write("(XLY" + str(self.sum) + ")" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("M=0" + '\n')
            self.fileObject.write("@END" + str(self.sum) + '\n')
            self.fileObject.write("0;JMP" + '\n')

            self.fileObject.write("(XGY" + str(self.sum) + ")" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("M=-1" + '\n')
            self.fileObject.write("(END" + str(self.sum) + ")" + '\n')

            self.fileObject.write("@SP" + '\n')
            self.fileObject.write("M=M-1" + '\n')
            self.sum += 1
        elif command == "lt":
            self.fileObject.write("@SP" + '\n')
            self.fileObject.write("D=M-1" + '\n')
            self.fileObject.write("@y" + str(self.sum) + '\n')
            self.fileObject.write("M=D" + '\n')
            self.fileObject.write("D=D-1" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("M=D" + '\n')

            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=M" + '\n')
            self.fileObject.write("@POSX" + str(self.sum) + '\n')
            self.fileObject.write("D;JGT" + '\n')

            self.fileObject.write("@y" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=M" + '\n')
            self.fileObject.write("@CHECK" + str(self.sum) + '\n')
            self.fileObject.write("D;JLE" + '\n')
            self.fileObject.write("@XLY" + str(self.sum) + '\n')
            self.fileObject.write("0;JMP" + '\n')

            self.fileObject.write("(POSX" + str(self.sum) + ")" + '\n')
            self.fileObject.write("@y" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=M" + '\n')
            self.fileObject.write("@CHECK" + str(self.sum) + '\n')
            self.fileObject.write("D;JGT" + '\n')
            self.fileObject.write("@XGY" + str(self.sum) + '\n')
            self.fileObject.write("0;JMP" + '\n')

            self.fileObject.write("(CHECK" + str(self.sum) + ")" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=M" + '\n')
            self.fileObject.write("@y" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=D-M" + '\n')
            self.fileObject.write("@XGY" + str(self.sum) + '\n')
            self.fileObject.write("D;JGE" + '\n')
            self.fileObject.write("@XLY" + str(self.sum) + '\n')
            self.fileObject.write("0;JMP" + '\n')

            self.fileObject.write("(XLY" + str(self.sum) + ")" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("M=-1" + '\n')
            self.fileObject.write("@END" + str(self.sum) + '\n')
            self.fileObject.write("0;JMP" + '\n')

            self.fileObject.write("(XGY" + str(self.sum) + ")" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("M=0" + '\n')
            self.fileObject.write("(END" + str(self.sum) + ")" + '\n')

            self.fileObject.write("@SP" + '\n')
            self.fileObject.write("M=M-1" + '\n')
            self.sum += 1
        elif command == "and":
            self.fileObject.write("@SP" + '\n')
            self.fileObject.write("D=M-1" + '\n')
            self.fileObject.write("@y" + str(self.sum) + '\n')
            self.fileObject.write("M=D" + '\n')
            self.fileObject.write("D=D-1" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("M=D" + '\n')

            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=M" + '\n')
            self.fileObject.write("@y" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=D&M" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("M=D" + '\n')

            self.fileObject.write("@SP" + '\n')
            self.fileObject.write("M=M-1" + '\n')
            self.sum += 1
        elif command == "or":
            self.fileObject.write("@SP" + '\n')
            self.fileObject.write("D=M-1" + '\n')
            self.fileObject.write("@y" + str(self.sum) + '\n')
            self.fileObject.write("M=D" + '\n')
            self.fileObject.write("D=D-1" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("M=D" + '\n')

            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=M" + '\n')
            self.fileObject.write("@y" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("D=D|M" + '\n')
            self.fileObject.write("@x" + str(self.sum) + '\n')
            self.fileObject.write("A=M" + '\n')
            self.fileObject.write("M=D" + '\n')

            self.fileObject.write("@SP" + '\n')
            self.fileObject.write("M=M-1" + '\n')
            self.sum += 1
        elif command == "not":
            self.fileObject.write("@SP" + '\n')
            self.fileObject.write("A=M-1" + '\n')
            self.fileObject.write("M=!M" + '\n')

    def writePushPop(self, command):
        """
        writing to the file according to the command
        :param command: command to translate
        """
        self.fileObject.write("//" + command + '\n')
        posh_pop, segment, index = command.split(" ")
        if posh_pop == "push":
            if segment == "local":
                self.fileObject.write("@{}".format(index) + '\n')
                self.fileObject.write("D=A" + '\n')
                self.fileObject.write("@LCL" + '\n')
                self.fileObject.write("A=M+D" + '\n')
                self.fileObject.write("D=M" + '\n')
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("A=M" + '\n')
                self.fileObject.write("M=D" + '\n')
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("M=M+1" + '\n')
            elif segment == "argument":
                self.fileObject.write("@{}".format(index) + '\n')
                self.fileObject.write("D=A" + '\n')
                self.fileObject.write("@ARG" + '\n')
                self.fileObject.write("A=M+D" + '\n')
                self.fileObject.write("D=M" + '\n')
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("A=M" + '\n')
                self.fileObject.write("M=D" + '\n')
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("M=M+1" + '\n')
            elif segment == "this":
                self.fileObject.write("@{}".format(index) + '\n')
                self.fileObject.write("D=A" + '\n')
                self.fileObject.write("@THIS" + '\n')
                self.fileObject.write("A=M+D" + '\n')
                self.fileObject.write("D=M" + '\n')
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("A=M" + '\n')
                self.fileObject.write("M=D" + '\n')
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("M=M+1" + '\n')
            elif segment == "that":
                self.fileObject.write("@{}".format(index) + '\n')
                self.fileObject.write("D=A" + '\n')
                self.fileObject.write("@THAT" + '\n')
                self.fileObject.write("A=M+D" + '\n')
                self.fileObject.write("D=M" + '\n')
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("A=M" + '\n')
                self.fileObject.write("M=D" + '\n')
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("M=M+1" + '\n')
            elif segment == "constant":
                self.fileObject.write("@{}".format(int(index)) + '\n')
                self.fileObject.write("D=A" + '\n')
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("A=M" + '\n')
                self.fileObject.write("M=D" + '\n')
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("M=M+1" + '\n')
            elif segment == "pointer":
                if int(index) == 0:
                    self.fileObject.write("@THIS" + '\n')
                    self.fileObject.write("D=M" + '\n')
                    self.fileObject.write("@SP" + '\n')
                    self.fileObject.write("A=M" + '\n')
                    self.fileObject.write("M=D" + '\n')
                    self.fileObject.write("@SP" + '\n')
                    self.fileObject.write("M=M+1" + '\n')
                else:
                    self.fileObject.write("@THAT" + '\n')
                    self.fileObject.write("D=M" + '\n')
                    self.fileObject.write("@SP" + '\n')
                    self.fileObject.write("A=M" + '\n')
                    self.fileObject.write("M=D" + '\n')
                    self.fileObject.write("@SP" + '\n')
                    self.fileObject.write("M=M+1" + '\n')
            elif segment == "static":
                self.fileObject.write(
                    "@" + NAMES_OF_FILES[self.counter] + "." + str(
                        index) + '\n')
                self.fileObject.write("D=M" + '\n')
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("A=M" + '\n')
                self.fileObject.write("M=D" + '\n')
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("M=M+1" + '\n')
            elif segment == "temp":
                self.fileObject.write("@5" + '\n')
                self.fileObject.write("D=A" + '\n')
                self.fileObject.write("@" + str(index) + '\n')
                self.fileObject.write("D=D+A" + '\n')
                self.fileObject.write("A=D" + '\n')
                self.fileObject.write("D=M" + '\n')
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("A=M" + '\n')
                self.fileObject.write("M=D" + '\n')
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("M=M+1" + '\n')
        else:  # posh+pop == "pop"
            if segment == "local":
                self.fileObject.write("@{}".format(index) + '\n')
                self.fileObject.write("D=A" + '\n')
                self.fileObject.write("@LCL" + '\n')
                self.fileObject.write("D=M+D" + '\n')
                self.fileObject.write("@ADDRESS" + str(self.sum) + '\n')
                self.fileObject.write("M=D" + '\n')
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("M=M-1" + '\n')
                self.fileObject.write("A=M" + '\n')
                self.fileObject.write("D=M" + '\n')
                self.fileObject.write("@ADDRESS" + str(self.sum) + '\n')
                self.fileObject.write("A=M" + '\n')
                self.fileObject.write("M=D" + '\n')
                self.sum += 1
            elif segment == "argument":
                # save the value from the stack and update SP
                self.fileObject.write("@{}".format(index) + '\n')
                self.fileObject.write("D=A" + '\n')
                self.fileObject.write("@ARG" + '\n')
                self.fileObject.write("D=M+D" + '\n')
                self.fileObject.write("@ADDRESS" + str(self.sum) + '\n')
                self.fileObject.write("M=D" + '\n')
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("M=M-1" + '\n')
                self.fileObject.write("A=M" + '\n')
                self.fileObject.write("D=M" + '\n')
                self.fileObject.write("@ADDRESS" + str(self.sum) + '\n')
                self.fileObject.write("A=M" + '\n')
                self.fileObject.write("M=D" + '\n')
                self.sum += 1
            elif segment == "this":
                self.fileObject.write("@{}".format(index) + '\n')
                self.fileObject.write("D=A" + '\n')
                self.fileObject.write("@THIS" + '\n')
                self.fileObject.write("D=M+D" + '\n')
                self.fileObject.write("@ADDRESS" + str(self.sum) + '\n')
                self.fileObject.write("M=D" + '\n')
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("M=M-1" + '\n')
                self.fileObject.write("A=M" + '\n')
                self.fileObject.write("D=M" + '\n')
                self.fileObject.write("@ADDRESS" + str(self.sum) + '\n')
                self.fileObject.write("A=M" + '\n')
                self.fileObject.write("M=D" + '\n')
                self.sum += 1
            elif segment == "that":
                self.fileObject.write("@{}".format(index) + '\n')
                self.fileObject.write("D=A" + '\n')
                self.fileObject.write("@THAT" + '\n')
                self.fileObject.write("D=M+D" + '\n')
                self.fileObject.write("@ADDRESS" + str(self.sum) + '\n')
                self.fileObject.write("M=D" + '\n')
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("M=M-1" + '\n')
                self.fileObject.write("A=M" + '\n')
                self.fileObject.write("D=M" + '\n')
                self.fileObject.write("@ADDRESS" + str(self.sum) + '\n')
                self.fileObject.write("A=M" + '\n')
                self.fileObject.write("M=D" + '\n')
                self.sum += 1
            elif segment == "pointer":
                if int(index) == 0:
                    self.fileObject.write("@SP" + '\n')
                    self.fileObject.write("AM=M-1" + '\n')
                    self.fileObject.write("D=M" + '\n')
                    self.fileObject.write("@THIS" + '\n')
                    self.fileObject.write("M=D" + '\n')
                else:
                    self.fileObject.write("@SP" + '\n')
                    self.fileObject.write("AM=M-1" + '\n')
                    self.fileObject.write("D=M" + '\n')
                    self.fileObject.write("@THAT" + '\n')
                    self.fileObject.write("M=D" + '\n')
            elif segment == "static":
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("AM=M-1" + '\n')
                self.fileObject.write("D=M" + '\n')
                self.fileObject.write(
                    "@" + NAMES_OF_FILES[self.counter] + "." + str(
                        index) + '\n')
                self.fileObject.write("M=D" + '\n')
            elif segment == "temp":
                self.fileObject.write("@" + str(START_TEMP) + '\n')
                self.fileObject.write("D=A" + '\n')
                self.fileObject.write("@" + str(index) + '\n')
                self.fileObject.write("D=D+A" + '\n')
                self.fileObject.write("@R13" + '\n')
                self.fileObject.write("M=D" + '\n')
                self.fileObject.write("@SP" + '\n')
                self.fileObject.write("AM=M-1" + '\n')
                self.fileObject.write("D=M" + '\n')
                self.fileObject.write("@R13" + '\n')
                self.fileObject.write("A=M" + '\n')
                self.fileObject.write("M=D" + '\n')

    def brancing_label(self, command):
        nameLable = command[0].split(" ")[1]
        self.fileObject.write("//" + command[0] + '\n')
        line = "(" + self.name_of_file + "$" + nameLable + ")"
        self.fileObject.write(line + '\n')

    def brancing_if(self, command):
        nameLable = command[0].split(" ")[1]
        self.fileObject.write("//" + command[0] + '\n')

        # self.fileObject.write("// " + nameLable + '\n')
        self.fileObject.write("@SP" + '\n')
        self.fileObject.write("A=M-1" + '\n')
        self.fileObject.write("D=M" + '\n')
        self.fileObject.write("@SP" + '\n')
        self.fileObject.write("M=M-1" + '\n')
        line = self.name_of_file + "$" + nameLable
        self.fileObject.write("@" + line + '\n')
        self.fileObject.write("D;JNE" + '\n')

    def brancing_goto(self, command):
        self.fileObject.write("//" + command[0] + '\n')

        nameLable = command[0].split(" ")[1]
        # self.fileObject.write("// " + nameLable + '\n')
        line = self.name_of_file + "$" + nameLable
        self.fileObject.write("@" + line + '\n')
        self.fileObject.write("0;JMP" + '\n')

    def branchingCall(self, command):
        x, nameOfFumc, numArg = command[0].split(" ")
        # push return address
        self.fileObject.write("//" + command[0] + '\n')

        self.fileObject.write(
            "@" + "CONTINUE" + str(self.sum) + '\n')  # push return address
        self.fileObject.write("D=A" + '\n')
        self.fileObject.write("@SP" + '\n')
        self.fileObject.write("A=M" + '\n')
        self.fileObject.write("M=D" + '\n')
        self.fileObject.write("@SP" + '\n')
        self.fileObject.write("M=M+1" + '\n')

        self.fileObject.write("@LCL" + '\n')  # push LCL
        self.fileObject.write("D=M" + '\n')
        self.fileObject.write("@SP" + '\n')
        self.fileObject.write("A=M" + '\n')
        self.fileObject.write("M=D" + '\n')
        self.fileObject.write("@SP" + '\n')
        self.fileObject.write("M=M+1" + '\n')

        self.fileObject.write("@ARG" + '\n')  # push ARG
        self.fileObject.write("D=M" + '\n')
        self.fileObject.write("@SP" + '\n')
        self.fileObject.write("A=M" + '\n')
        self.fileObject.write("M=D" + '\n')
        self.fileObject.write("@SP" + '\n')
        self.fileObject.write("M=M+1" + '\n')

        self.fileObject.write("@THIS" + '\n')  # push THIS
        self.fileObject.write("D=M" + '\n')
        self.fileObject.write("@SP" + '\n')
        self.fileObject.write("A=M" + '\n')
        self.fileObject.write("M=D" + '\n')
        self.fileObject.write("@SP" + '\n')
        self.fileObject.write("M=M+1" + '\n')

        self.fileObject.write("@THAT" + '\n')  # push THAT
        self.fileObject.write("D=M" + '\n')
        self.fileObject.write("@SP" + '\n')
        self.fileObject.write("A=M" + '\n')
        self.fileObject.write("M=D" + '\n')
        self.fileObject.write("@SP" + '\n')
        self.fileObject.write("M=M+1" + '\n')

        self.fileObject.write("@" + str(numArg) + '\n')  # ARG = SP-n-5
        self.fileObject.write("D=A" + '\n')
        self.fileObject.write("@R5" + '\n')
        self.fileObject.write("D=D+A" + '\n')
        self.fileObject.write("@SP" + '\n')
        self.fileObject.write("D=M-D" + '\n')
        self.fileObject.write("@ARG" + '\n')
        self.fileObject.write("M=D" + '\n')

        self.fileObject.write("@SP" + '\n')  # LCL = SP
        self.fileObject.write("D=M" + '\n')
        self.fileObject.write("@LCL" + '\n')
        self.fileObject.write("M=D" + '\n')

        self.fileObject.write("@" + str(nameOfFumc) + '\n')  # goto f
        self.fileObject.write("0;JMP" + '\n')

        self.fileObject.write("(" + "CONTINUE" + str(self.sum) + ")" + '\n')
        self.sum += 1

    def branchingFuncion(self, command):
        x, nameOfFunc, numLocal = command[0].split(" ")  # update label
        self.fileObject.write("//" + command[0] + '\n')

        self.fileObject.write("(" + str(nameOfFunc) + ")" + '\n')
        # print(numLocal)
        for i in range(int(numLocal)):  # update local values 0
            self.fileObject.write("@" + str(i) + '\n')
            self.fileObject.write("D=A" + '\n')
            self.fileObject.write("@LCL" + '\n')
            self.fileObject.write("A=M+D" + '\n')
            self.fileObject.write("M=0" + '\n')
        self.fileObject.write("@" + str(numLocal) + '\n')
        self.fileObject.write("D=A" + '\n')
        self.fileObject.write("@SP" + '\n')
        self.fileObject.write("M=M+D" + '\n')

    def branchingReturn(self, command):
        self.fileObject.write("//" + command[0] + '\n')
        self.fileObject.write("@LCL" + '\n')  # FRAME =LCL
        self.fileObject.write("D=M" + '\n')
        self.fileObject.write("@FRAME" + str(self.sum) + '\n')
        self.fileObject.write("M=D" + '\n')

        self.fileObject.write("@R5" + '\n')  # RET = FARAM - 5
        self.fileObject.write("D=A" + '\n')
        self.fileObject.write("@FRAME" + str(self.sum) + '\n')
        self.fileObject.write("D=M-D" + '\n')
        self.fileObject.write("A=D" + '\n')
        self.fileObject.write("D=M" + '\n')
        self.fileObject.write("@RET" + str(self.sum) + '\n')
        self.fileObject.write("M=D" + '\n')

        self.fileObject.write("@SP" + '\n')  # *ARG = pop()
        self.fileObject.write("AM=M-1" + '\n')
        self.fileObject.write("D=M" + '\n')
        self.fileObject.write("@ARG" + '\n')
        self.fileObject.write("A=M" + '\n')
        self.fileObject.write("M=D" + '\n')

        self.fileObject.write("@ARG" + '\n')  # SP = ARG + 1
        self.fileObject.write("D=M+1" + '\n')
        self.fileObject.write("@SP" + '\n')
        self.fileObject.write("M=D" + '\n')

        self.fileObject.write("@R1" + '\n')  # THAT = FRAME-1
        self.fileObject.write("D=A" + '\n')
        self.fileObject.write("@FRAME" + str(self.sum) + '\n')
        self.fileObject.write("D=M-D" + '\n')
        self.fileObject.write("A=D" + '\n')
        self.fileObject.write("D=M" + '\n')
        self.fileObject.write("@THAT" + '\n')
        self.fileObject.write("M=D" + '\n')

        self.fileObject.write("@R2" + '\n')  # THIS = FRAME-2
        self.fileObject.write("D=A" + '\n')
        self.fileObject.write("@FRAME" + str(self.sum) + '\n')
        self.fileObject.write("D=M-D" + '\n')
        self.fileObject.write("A=D" + '\n')
        self.fileObject.write("D=M" + '\n')
        self.fileObject.write("@THIS" + '\n')
        self.fileObject.write("M=D" + '\n')

        self.fileObject.write("@R3" + '\n')  # ARG = FRAME-3
        self.fileObject.write("D=A" + '\n')
        self.fileObject.write("@FRAME" + str(self.sum) + '\n')
        self.fileObject.write("D=M-D" + '\n')
        self.fileObject.write("A=D" + '\n')
        self.fileObject.write("D=M" + '\n')
        self.fileObject.write("@ARG" + '\n')
        self.fileObject.write("M=D" + '\n')

        self.fileObject.write("@R4" + '\n')  # LCL = FRAME-4
        self.fileObject.write("D=A" + '\n')
        self.fileObject.write("@FRAME" + str(self.sum) + '\n')
        self.fileObject.write("D=M-D" + '\n')
        self.fileObject.write("A=D" + '\n')
        self.fileObject.write("D=M" + '\n')
        self.fileObject.write("@LCL" + '\n')
        self.fileObject.write("M=D" + '\n')

        self.fileObject.write("@RET" + str(self.sum) + '\n')
        self.fileObject.write("A=M" + '\n')
        self.fileObject.write("0;JMP" + '\n')

        self.sum += 1

    def close(self):
        """
        close the file we wrote
        """
        self.fileObject.close()


def main():
    """
    main function
    """
    directory = sys.argv[1]
    s = parser(directory)
    s.cleanLines()
    codeWriter(directory, s.lineStrArray, s.folderName)

if __name__ == '__main__':
    main()