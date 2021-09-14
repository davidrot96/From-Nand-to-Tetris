# David96,nataliy
import os
import sys

START = 16

destDic = {"M": "001", "D": "010", "MD": "011", "A": "100", "AM": "101",
           "AD": "110", "AMD": "111", "": "000"}

compDic = {"0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100",
           "A": "0110000", "!D": "0001101", "!A": "0110001", "-D": "0001111",
           "-A": "0110011", "D+1": "0011111", "A+1": "0110111",
           "D-1": "0001110", "A-1": "0110010", "D+A": "0000010",
           "D-A": "0010011", "A-D": "0000111", "D|A": "0010101", "M": "1110000",
           "!M": "1110001", "-M": "1110011", "M+1": "1110111", "M-1": "1110010",
           "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
           "D&M": "1000000", "D|M": "1010101", "D&A": "0000000",
           "D<<": "0110000", "D>>": "0010000", "A<<": "0100000",
           "A>>": "0000000", "M<<": "1100000", "M>>": "1000000"}

jumpDic = {"JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100",
           "JNE": "101", "JLE": "110", "JMP": "111", "": "000"}


def lineTranslate(lines, ourDict, fileName,dir):
    """
    :param lines: the current line in the file
    :param ourDict: the dict of the base label
    :param fileName: the name of the file
    :param dir: the path to the file
    :return: the function dose not return anything
    """
    if(dir != ""):
        fileObject = open(dir + "/" + os.path.splitext(fileName)[0] + ".hack", 'w')
    else:
        fileObject = open(fileName.split(".")[0] + ".hack", 'w')
    counter = START
    for line in lines:
        newLine = line.replace(" ", "")
        if newLine == '\n' or newLine == "" or newLine[0:2] == "//":
            continue
        if newLine[0] == '@':
            name = newLine[1::]
            if not contains(ourDict, name):
                if name.isdigit():
                    addEntry(ourDict, name, int(name))
                else:
                    addEntry(ourDict, name, counter)
                    counter += 1
            binaryNum = '{0:016b}'.format(ourDict[name])
        elif newLine[0] == '(':
            continue
        else:
            dest = ""
            jump = ""
            comp = ""
            if '=' in newLine:
                dest = newLine.split('=')[0]
                if ';' in newLine:
                    comp = newLine.split(';')[0]
                    jump = newLine.split(';')[1]
                else:
                    comp = newLine.split('=')[1]
            elif ';' in newLine:
                comp = newLine.split(';')[0]
                jump = newLine.split(';')[1]

            if "<<" in comp or ">>" in comp:
                binaryNum = "101"
            else:
                binaryNum = "111"
            binaryNum += compDic[comp]
            binaryNum += destDic[dest]
            binaryNum += jumpDic[jump]
        fileObject.write(binaryNum + '\n')
    fileObject.close()

def stepOne(lines, ourDict):
    """
    :param lines: the current line in the file
    :param ourDict: the dict of the base label
    :return: the function dose not return anything
    """
    counter = 0
    indexLine = 0
    newString = lines.copy()
    for line in lines:
        newLine = line.replace(" ", "")
        newString[indexLine] = newLine
        if newLine == '\n' or newLine == "" or newLine[0:2] == "//":
            newString.remove(newLine)
            continue
        if "//" in newLine:
            newString[indexLine] = newLine.split('//')[0]
        if newLine[0:1] == '(':
            ourDict[newLine.split(')')[0][1::]] = counter
            indexLine += 1
        else:
            indexLine += 1
            counter += 1
    return newString

def intilize(directory):
    """
    :param directory: the directorh of the files
    :return: the function dose not return anything
    """
    if(os.path.isfile(directory)) and directory.endswith(".asm"):
        newDict = creatDict()
        with open(directory,'r') as file:
            stringLine = ""
            lines1 = file.readlines()
            for line in lines1:
                stringLine += line
            newString = stepOne(stringLine.split('\n'), newDict)
            lineTranslate(newString, newDict, directory,"")
    else:
        for filename in os.listdir(directory):
            if filename.endswith(".asm"):
                newDict = creatDict()
                with open(directory+"/" + filename, 'r') as file:
                    stringLine = ""
                    lines1 = file.readlines()
                    for line in lines1:
                        stringLine += line
                    newString = stepOne(stringLine.split('\n'), newDict)
                    lineTranslate(newString, newDict, filename,directory)

def creatDict():
    """
    :return: the duct with rhe base label
    """
    symbolDict = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576
    }
    for i in range(16):
        temp = "{}".format(i)
        symbolDict["R" + temp] = i
    return symbolDict


def addEntry(dict, newKey, newValue):
    """
    :param dict: the dict of the base label
    :param newKey: the new ker to insert
    :param newValue: the new value to insert
    :return: the dict
    """
    dict[newKey] = newValue
    return dict


def contains(dict, symbol):
    """
    :param dict: the dict of the base label
    :param symbol: the key in duct
    :return: true if the key if the dict, false otherwise
    """
    if symbol in dict.keys():
        return True
    return False


def getAddress(dict, symbol):
    """
    :param dict: the dict of the base label
    :param symbol: the key
    :return: the value in the dict
    """
    return dict[symbol]


def main():
    """
    :return: None
    """
    intilize(sys.argv[1])


if __name__ == '__main__':
    main()