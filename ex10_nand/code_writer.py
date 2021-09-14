import os
import sys
import copy

OPEN_KEYWORD = "<keyword> "
CLOSE_KEYWORD = " </keyword>\n"
OPEN_IDENTIFIER = "<identifier> "
CLOSE_IDENTIFIER = " </identifier>\n"
OPEN_SYMBOL = "<symbol> "
CLOSE_SYMBOL = " </symbol>\n"
OPEN_INTCONST = "<integerConstant> "
CLOSE_INTCONST = " </integerConstant>\n"
OPEN_STRINGCONST = "<stringConstant> "
CLOSE_STRINGCONST = " </stringConstant>\n"
OPEN_CLASS = "<class>\n"
CLOSE_CLASS = "</class>\n"
OPEN_LETSTATEMENT = "<letStatement>\n"
CLOSE_LETSTATEMENT = "</letStatement>\n"
OPEN_EXPRESSION = "<expression>\n"
CLOSE_EXPRESSION = "</expression>\n"
OPEN_DO = "<doStatement>\n"
CLOSE_DO = "</doStatement>\n"
OPEN_RETURN = "<returnStatement>\n"
CLOSE_RETURN = "</returnStatement>\n"
OPEN_WHILE = "<whileStatement>\n"
CLOSE_WHILE = "</whileStatement>\n"
OPEN_IF = "<ifStatement>\n"
CLOSE_IF = "</ifStatement>\n"
OPEN_STATEMENTS = "<statements>\n"
CLOSE_STATEMENTS = "</statements>\n"
OPEN_VARDEC = "<varDec>\n"
CLOSE_VARDEC = "</varDec>\n"
OPEN_CLASSVAR = "<classVarDec>\n"
CLOSE_CLASSVAR = "</classVarDec>\n"
OPEN_SUBDEC = "<subroutineDec>\n"
CLOSE_SUBDEC = "</subroutineDec>\n"
OPEN_SUBBODY = "<subroutineBody>\n"
CLOSE_SUBBODY = "</subroutineBody>\n"
OPEN_EXPRESSIONLIST = "<expressionList>\n"
CLOSE_EXPRESSIONLIST = "</expressionList>\n"
OPEN_TERM = "<term>\n"
CLOSE_TERM = "</term>\n"
OPEN_PARAMLIST = "<parameterList>\n"
CLOSE_PARAMLIST = "</parameterList>\n"

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

UNARY_OP_TYPES = ['-','~']

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
            #print(self.output_token)

    def fill_output(self):
        str_const = False
        strTemp = ''
        for line in self.tempStrList:
            line = line.split("//")[0]
            line = line.split("/**")[0]
            if len(line) > 1 and line[1] == '*':
                line = line.split("*")[0]



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


class JackAnalyzer:
    directory = ''
    jackToken = []
    xmlNewFile = []
    countFiles = 0

    def __init__(self, directory):
        self.directory = directory
        if (os.path.isfile(self.directory)):  # if it's a file
            self.jackToken.append(JackTokenizer(self.directory))
            self.xmlNewFile.append(open(os.path.splitext(self.directory)[0] + ".xml", 'w'))
            self.countFiles += 1

        else:
            for filename in os.listdir(directory):  # if it's a folder
                if filename.endswith(".jack"):
                    newTokenizer = copy.deepcopy(JackTokenizer(self.directory + '/' + filename))
                    newFile = open(self.directory + '/' + os.path.splitext(filename)[0] + ".xml", 'w')
                    self.jackToken.append(newTokenizer)
                    self.xmlNewFile.append(newFile)
                    self.countFiles += 1
                    newTokenizer = None

        self.jackTranslate()

    def jackTranslate(self):
        # compileFiles = CompiliationEngine(self.jackToken, self.xmlNewFile)
        for i in range(self.countFiles):
            CompiliationEngine(self.jackToken[i], self.xmlNewFile[i])


class CompiliationEngine:
    counter = 0
    inpotTokens = None
    outputFile = ''

    def __init__(self, inpotTokens, outputFile):
        self.inpotTokens = inpotTokens
        self.outputFile = outputFile
        self.counter = 0
        self.CompileClass()

    def CompileClass(self):
        self.outputFile.write(OPEN_CLASS)
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_KEYWORD + token + CLOSE_KEYWORD)
        self.counter += 1
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_IDENTIFIER + token + CLOSE_IDENTIFIER)
        self.counter += 1
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
        self.counter += 1
        token = self.inpotTokens.output_token[self.counter]
        while token in ["static", "field"]:
            self.compileClassVarDec()
            token = self.inpotTokens.output_token[self.counter]
        while token in ["constructor", "function", "method"]:
            self.compileSubroutine()
            token = self.inpotTokens.output_token[self.counter]
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
        self.outputFile.write(CLOSE_CLASS)

    def compileLet(self):
        self.outputFile.write(OPEN_LETSTATEMENT)
        self.outputFile.write(OPEN_KEYWORD + "let" + CLOSE_KEYWORD)
        self.counter += 1
        token = self.inpotTokens.output_token[self.counter]
        nextToken = self.inpotTokens.output_token[self.counter + 1]
        if nextToken == '[':
            self.outputFile.write(OPEN_IDENTIFIER + token + CLOSE_IDENTIFIER)
            self.counter += 1
            self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(nextToken) + CLOSE_SYMBOL)
            self.counter += 1
            self.compileExpression()
            token = self.inpotTokens.output_token[self.counter]
            self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
            self.counter += 1
            token = self.inpotTokens.output_token[self.counter]
            self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
            self.counter += 1
        else:
            self.outputFile.write(OPEN_IDENTIFIER + token + CLOSE_IDENTIFIER)
            self.counter += 1
            self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(nextToken) + CLOSE_SYMBOL)
            self.counter += 1
        self.compileExpression()
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
        self.outputFile.write(CLOSE_LETSTATEMENT)

    def compileExpression(self):

        self.outputFile.write(OPEN_EXPRESSION)
        token = self.inpotTokens.output_token[self.counter]
        priTokenType = self.inpotTokens.tokenType(self.inpotTokens.output_token[self.counter-1])
        priTokenType2 = self.inpotTokens.tokenType(self.inpotTokens.output_token[self.counter -2])
        while token not in [',', ')', ']', ';']:
            if token not in OP_TYPES or (token in UNARY_OP_TYPES and (priTokenType != 'IDENTIFIER')):
                self.compileTerm()
            else:
                self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
                self.counter += 1
            token = self.inpotTokens.output_token[self.counter]
            priTokenType = self.inpotTokens.tokenType(self.inpotTokens.output_token[self.counter - 1])
            priTokenType2 = self.inpotTokens.tokenType(self.inpotTokens.output_token[self.counter -2])
        self.outputFile.write(CLOSE_EXPRESSION)

    def checkTerm(self):
        priTokenType = self.inpotTokens.tokenType(self.inpotTokens.output_token[self.counter-1])
        priTokenType2 = self.inpotTokens.tokenType(self.inpotTokens.output_token[self.counter -2])
        if priTokenType == 'IDENTIFIER':
            return True
        elif self.inpotTokens.output_token[self.counter-1] in [')',']']:
            if priTokenType2 == 'IDENTIFIER':
                return True
        return False




    def compileDo(self):
        self.outputFile.write(OPEN_DO)
        self.outputFile.write(OPEN_KEYWORD + "do" + CLOSE_KEYWORD)
        self.counter += 1
        token = self.inpotTokens.output_token[self.counter]
        while token != "(":
            if token != ".":
                self.outputFile.write(OPEN_IDENTIFIER + token + CLOSE_IDENTIFIER)
            else:
                self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
            self.counter += 1
            token = self.inpotTokens.output_token[self.counter]
        self.complieExpressionList()
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
        self.counter += 1
        self.outputFile.write(CLOSE_DO)

    def compileReturn(self):
        self.outputFile.write(OPEN_RETURN)
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_KEYWORD + token + CLOSE_KEYWORD)
        self.counter += 1
        token = self.inpotTokens.output_token[self.counter]
        if token != ';':
            self.compileExpression()
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
        self.counter += 1
        self.outputFile.write(CLOSE_RETURN)

    def compileWhile(self):
        self.outputFile.write(OPEN_WHILE)
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_KEYWORD + token + CLOSE_KEYWORD)  # "while"
        self.counter += 1
        token = self.inpotTokens.output_token[self.counter]
        self.counter += 1
        self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)  # '('
        self.compileExpression()
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
        self.counter += 1
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
        self.compileStatements()
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
        self.counter += 1

        self.outputFile.write(CLOSE_WHILE)

    def compileIf(self):
        self.outputFile.write(OPEN_IF)
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_KEYWORD + token + CLOSE_KEYWORD)
        self.counter += 1
        if token == "if":
            token = self.inpotTokens.output_token[self.counter]
            self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
            self.counter += 1
            self.compileExpression()
        token = self.inpotTokens.output_token[self.counter]  # ")"
        self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
        self.counter += 1
        token = self.inpotTokens.output_token[self.counter]  # '{'
        self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
        self.counter += 1
        self.compileStatements()
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
        self.counter += 1
        token = self.inpotTokens.output_token[self.counter]
        if token == "else":
            self.outputFile.write(OPEN_KEYWORD + token + CLOSE_KEYWORD)
            self.counter += 1
            token = self.inpotTokens.output_token[self.counter]
            self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
            self.counter += 1
            self.compileStatements()
            token = self.inpotTokens.output_token[self.counter]
            self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
            self.counter += 1

        self.outputFile.write(CLOSE_IF)

    def compileStatements(self):
        token = self.inpotTokens.output_token[self.counter]
        nextToken = self.inpotTokens.output_token[self.counter + 1]
        while token != "}":
            if token == 'var':
                self.compileVarDec()
                token = self.inpotTokens.output_token[self.counter]
                nextToken = self.inpotTokens.output_token[self.counter + 1]
            elif nextToken == 'var':
                self.counter += 1
                token = self.inpotTokens.output_token[self.counter]
                nextToken = self.inpotTokens.output_token[self.counter + 1]
            else:
                break
        self.outputFile.write(OPEN_STATEMENTS)
        token = self.inpotTokens.output_token[self.counter]
        while token != "}":
            if token == "let":
                self.compileLet()
            elif token == "if":
                self.compileIf()
            elif token == "while":
                self.compileWhile()
            elif token == "do":
                self.compileDo()
            elif token == "return":
                self.compileReturn()
            else:
                self.counter += 1
            token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(CLOSE_STATEMENTS)

    def compileVarDec(self):
        self.outputFile.write(OPEN_VARDEC)
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_KEYWORD + token + CLOSE_KEYWORD)
        self.counter += 1
        token = self.inpotTokens.output_token[self.counter]
        if self.inpotTokens.tokenType(token) == "KEYWORD":
            self.outputFile.write(OPEN_KEYWORD + token + CLOSE_KEYWORD)
        else:
            self.outputFile.write(OPEN_IDENTIFIER + token + CLOSE_IDENTIFIER)
        self.counter += 1
        token = self.inpotTokens.output_token[self.counter]
        while token != ";":
            if token == ",":
                self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
            else:
                self.outputFile.write(OPEN_IDENTIFIER + token + CLOSE_IDENTIFIER)
            self.counter += 1
            token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
        self.outputFile.write(CLOSE_VARDEC)

    def compileClassVarDec(self):
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_CLASSVAR)
        self.outputFile.write(OPEN_KEYWORD + token + CLOSE_KEYWORD)
        self.counter += 1
        token = self.inpotTokens.output_token[self.counter]
        if self.inpotTokens.tokenType(token) == "KEYWORD":
            self.outputFile.write(OPEN_KEYWORD + token + CLOSE_KEYWORD)
        else:
            self.outputFile.write(OPEN_IDENTIFIER + token + CLOSE_IDENTIFIER)
        self.counter += 1
        token = self.inpotTokens.output_token[self.counter]
        while token != ";":
            if token == ",":
                self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
            else:
                self.outputFile.write(OPEN_IDENTIFIER + token + CLOSE_IDENTIFIER)
            self.counter += 1
            token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
        self.counter += 1
        self.outputFile.write(CLOSE_CLASSVAR)

    def compileSubroutine(self):
        self.outputFile.write(OPEN_SUBDEC)
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_KEYWORD + token + CLOSE_KEYWORD)
        self.counter += 1
        token = self.inpotTokens.output_token[self.counter]
        if self.inpotTokens.tokenType(token) == "KEYWORD":
            self.outputFile.write(OPEN_KEYWORD + token + CLOSE_KEYWORD)
        else:
            self.outputFile.write(OPEN_IDENTIFIER + token + CLOSE_IDENTIFIER)
        self.counter += 1
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_IDENTIFIER + token + CLOSE_IDENTIFIER)
        self.counter += 1
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
        self.counter += 1
        self.compileParameterList()
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
        self.outputFile.write(OPEN_SUBBODY)
        self.counter += 1
        token = self.inpotTokens.output_token[self.counter]
        if token == "{":
            self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
            self.compileStatements()
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
        self.counter += 1
        self.outputFile.write(CLOSE_SUBBODY)
        self.outputFile.write(CLOSE_SUBDEC)

    def complieExpressionList(self):
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
        self.counter += 1
        self.outputFile.write(OPEN_EXPRESSIONLIST)
        token = self.inpotTokens.output_token[self.counter]
        while token != ")":
            if token == ",":
                self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
                self.counter += 1
            else:
                self.compileExpression()
            token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(CLOSE_EXPRESSIONLIST)
        token = self.inpotTokens.output_token[self.counter]
        self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
        self.counter += 1

    def compileTerm(self):
        token = self.inpotTokens.output_token[self.counter]
        tokenType = self.inpotTokens.tokenType(token)
        self.outputFile.write(OPEN_TERM)

        if tokenType == "INT_CONST":
            self.outputFile.write(OPEN_INTCONST + token + CLOSE_INTCONST)
            self.counter += 1
        elif tokenType == "STRING_CONST":
            self.outputFile.write(OPEN_STRINGCONST + self.inpotTokens.stringVal(token) + CLOSE_STRINGCONST)
            self.counter += 1
        elif tokenType == "KEYWORD" and token in ['true', 'false', 'null', 'this']:
            self.outputFile.write(OPEN_KEYWORD + token + CLOSE_KEYWORD)
            self.counter += 1
        elif tokenType == "IDENTIFIER":
            nextToken = self.inpotTokens.output_token[self.counter + 1]
            if nextToken == "[":
                self.outputFile.write(OPEN_IDENTIFIER + token + CLOSE_IDENTIFIER)
                self.counter += 1
                self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(nextToken) + CLOSE_SYMBOL)
                self.counter += 1
                self.compileExpression()
                token = self.inpotTokens.output_token[self.counter]
                self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
                self.counter += 1
            elif nextToken in ['(', '.']:
                self.compileSubroutineCall()
            else:
                self.outputFile.write(OPEN_IDENTIFIER + token + CLOSE_IDENTIFIER)
                self.counter += 1
        elif token == "(":
            self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
            self.counter += 1
            self.compileExpression()
            token = self.inpotTokens.output_token[self.counter]
            self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
            self.counter += 1
        elif token in ['-', '~']:
            self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
            self.counter += 1
            self.compileTerm()
            #token = self.inpotTokens.output_token[self.counter]
            #tokenType = self.inpotTokens.tokenType(token)
        self.outputFile.write(CLOSE_TERM)

    def compileParameterList(self):
        self.outputFile.write(OPEN_PARAMLIST)
        token = self.inpotTokens.output_token[self.counter]
        tokenType = self.inpotTokens.tokenType(token)
        while token != ")":
            if tokenType == "KEYWORD":
                self.outputFile.write(OPEN_KEYWORD + token + CLOSE_KEYWORD)
            elif tokenType == "IDENTIFIER":
                self.outputFile.write(OPEN_IDENTIFIER + token + CLOSE_IDENTIFIER)
            else:
                self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
            self.counter += 1
            token = self.inpotTokens.output_token[self.counter]
            tokenType = self.inpotTokens.tokenType(token)
        self.outputFile.write(CLOSE_PARAMLIST)

    def compileSubroutineCall(self):
        token = self.inpotTokens.output_token[self.counter]
        nextToken = self.inpotTokens.output_token[self.counter + 1]
        if nextToken == "(":
            self.outputFile.write(OPEN_IDENTIFIER + token + CLOSE_IDENTIFIER)
            self.counter += 1
            self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(nextToken) + CLOSE_SYMBOL)
            self.counter += 1
            self.complieExpressionList()
            token = self.inpotTokens.output_token[self.counter]
            self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(token) + CLOSE_SYMBOL)
            self.counter += 1
        else:
            self.outputFile.write(OPEN_IDENTIFIER + token + CLOSE_IDENTIFIER)
            self.counter += 1
            self.outputFile.write(OPEN_SYMBOL + self.checkSymbol(nextToken) + CLOSE_SYMBOL)
            self.counter += 1
            token = self.inpotTokens.output_token[self.counter]
            self.outputFile.write(OPEN_IDENTIFIER + token + CLOSE_IDENTIFIER)
            self.counter += 1
            self.complieExpressionList()

    def checkSymbol(self, mySymbol):
        if mySymbol == '<':
            return "&lt;"
        elif mySymbol == '>':
            return "&gt;"
        elif mySymbol == '&':
            return "&amp;"
        else:
            return mySymbol


if __name__ == '__main__':
    directory = sys.argv[1]
    JackAnalyzer(directory)
