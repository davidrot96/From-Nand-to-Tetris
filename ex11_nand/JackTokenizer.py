import os

KEYWORD_TYPES = ["class", "constructor", "function", "method", "field",
                 "static", "var", "int", "char", "boolean", "void", "true",
                 "false", "null", "this", "let", "do", "if", "else", "while",
                 "return"]

KEYWORD_DICT = {"class": "CLASS", "constructor": "CONSTRACTOR", "function": "FUNCTION", "method": "METHOD",
                "field": "FIELD", "static": "STATIC", "var": "VAR", "int": "INT", "char": "CHAR", "boolean": "BOOLEAN",
                "void": "VOID", "true": "TRUE", "false": "False", "null": "NULL", "this": "THIS", "let": "LET",
                "do": "DO", "if": "IF", "else": "ELSE", "while": "WHILE", "return": "RETURN"}

SYMBOL_TYPES = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*',
                '/', '&', '|', '<', '>', '=', '~']
OP_TYPES = ['+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

UNARY_OP_TYPES = ['-', '~']


class JackTokenizer:
    tempStrList = []
    output_token = []
    numToken = 0

    def __init__(self, directory):
        self.output_token = []
        self.tempStrList = []
        if (os.path.isfile(directory)):  # always gets a file directory
            with open(directory, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    addLine = line.split("\n")
                    addLine = addLine[0].replace("\t", "")
                    self.tempStrList.append(addLine)
            file.close()
            self.fill_output()


    def fill_output(self):
        str_const = False
        strTemp = ''
        str_commend = False

        for line in self.tempStrList:
            line = line.split("//")[0]
            if ('/**' in line or '/*' in line) and '*/' in line:
                line = line.split("/*")[0]
            elif '/**' in line or '/*' in line:
                line = line.split("/*")[0]
                str_commend = True
            if str_commend and '*/' not in line:
                continue
            elif str_commend and  '*/' in line:
                str_commend = False
                continue

            if len(line) > 1 and line[1] == '*':
                line = ''
            for i in range(len(line)):
                charToCheck = line[i]
                if charToCheck == ' ':
                    if strTemp != '' and str_const == False:
                        self.output_token.append(strTemp)
                        strTemp = ''
                        continue
                    elif strTemp != '' and str_const == True:
                        strTemp += ' '
                        continue
                    else:
                        continue
                if charToCheck in SYMBOL_TYPES and charToCheck != '"':
                    if strTemp == '':
                        self.output_token.append(charToCheck)
                        continue

                    elif str_const:
                        strTemp += charToCheck
                        continue

                    else:
                        self.output_token.append(strTemp)
                        self.output_token.append(charToCheck)
                        strTemp = ''
                        continue
                if charToCheck == '"':
                    if strTemp == '':
                        str_const = True
                        strTemp += charToCheck
                        continue
                    else:
                        str_const = False
                        strTemp += charToCheck
                        self.output_token.append(strTemp)
                        strTemp = ''
                        continue
                if charToCheck != '':
                    strTemp += charToCheck
            if strTemp != '':
                self.output_token.append(strTemp)
                strTemp = ''

    def tokenType(self, token):
        if token[0] == '"':
            return "STRING_CONST"
        if token in SYMBOL_TYPES:
            return "SYMBOL"
        if token in KEYWORD_TYPES:
            return "KEYWORD"
        if token.isdigit():
            return "INT_CONST"
        return "IDENTIFIER"

    def keyWord(self, token):
        return KEYWORD_DICT[token]

    def symbol(self, token):
        return token

    def identifier(self, token):
        return token

    def intVal(self, token):
        int(token)

    def stringVal(self, token):
        return token[1:-1]