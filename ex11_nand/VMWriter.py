import os


class VMWriter:
    outputFile = None

    def __init__(self, file_name):
        self.outputFile = open(os.path.splitext(file_name)[0] + ".vm", 'w')

    def write_push(self, segment, index):
        self.outputFile.write('push ' + segment + ' ' + str(index) + '\n')

    def write_pop(self, segment, index):
        self.outputFile.write('pop ' + segment + ' ' + str(index) + '\n')

    def write_arithmetic(self, command):
        self.outputFile.write(self.symbol(command) + '\n')

    def write_label(self, label):
        self.outputFile.write('label ' + label + '\n')

    def write_goto(self, label):
        self.outputFile.write('goto ' + label + '\n')

    def write_if(self, label):
        self.outputFile.write('if-goto ' + label + '\n')

    def write_call(self, name, nArgs):
        self.outputFile.write('call ' + name + ' ' + str(nArgs) + '\n')

    def write_function(self, name, nLocals):
        self.outputFile.write('function ' + name + ' ' + str(nLocals) + '\n')

    def write_return(self):
        self.outputFile.write('return\n')

    def close_output_file(self):
        self.outputFile.close()


    def symbol(self, commend):  # {"+", "-", "*", "/", "&", "|", "<", ">", "="}:
        if commend == '+':
            return 'add'
        elif commend == '-':
            return 'sub'
        elif commend == "&":
            return 'and'
        elif commend == '<':
            return 'lt'
        elif commend == '=':
            return 'eq'
        elif commend == '>':
            return 'gt'
        elif commend == '%':
            return 'and'
        elif commend == '|':
            return 'or'
        elif commend == '~':
            return 'not'
        elif commend == '*':
            return "call Math.multiply 2"
        elif commend == '/':
            return "call Math.divide 2"
        elif commend == '--':
            return 'neg'


