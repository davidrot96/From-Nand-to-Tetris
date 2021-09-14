from SymbolTable import *
from VMWriter import *
from JackTokenizer import *

KIND_DICT = {'field': 'FIELD', 'static': 'STATIC', 'var': 'VAR'}
DIC_SAGMENTS = {'argument': 'argument', 'var': 'local', 'field': 'this'}
UNARY_OP_TYPES = ['-', '~']


class CompiliationEngine:
    directory = ''
    tokenizer = None
    vm_writer = None
    table = None
    token_index = 0
    while_counter = 0
    if_counter = 0
    name_of_class = ''

    def __init__(self, tokenizer, directory):
        """
        :param tokenizer:
        :param directory:
        """
        self.tokenizer = tokenizer
        self.directory = directory
        self.vm_writer = VMWriter(directory)
        self.table = SymbolTable()
        self.compile_class()
        self.vm_writer.close_output_file()

    def compile_class(self):
        """
        :return: compile class
        """
        self.token_index += 1  # class
        self.name_of_class = self.tokenizer.output_token[self.token_index]
        self.token_index += 2
        token = self.tokenizer.output_token[self.token_index]

        while token in ["static", "field"]:
            self.compile_class_var_dec()
            token = self.tokenizer.output_token[self.token_index]
        while token in ["constructor", "function", "method"]:
            self.if_counter = 0
            self.while_counter = 0
            self.table.start_subroutine()
            self.compile_subroutine()
            token = self.tokenizer.output_token[self.token_index]

    def compile_parameter_list(self):
        """
        :return: compile parameter list
        """
        token = self.tokenizer.output_token[self.token_index]
        while token != ")":
            type = self.tokenizer.output_token[self.token_index]
            self.token_index += 1
            name = self.tokenizer.output_token[self.token_index]
            self.token_index += 1
            self.table.define_symbol(name, type, 'ARG')
            token = self.tokenizer.output_token[self.token_index]
            if token == ',':
                self.token_index += 1
        self.token_index += 1

    def compile_statements(self):
        """
        :return: compile statements
        """
        token = self.tokenizer.output_token[self.token_index]
        while token in ['let', 'if', 'else', 'while', 'do', 'return']:
            if token == 'let':
                self.compile_let()
            elif token in ['if', 'else']:
                self.compile_if()
            elif token == 'while':
                self.compile_while()
            elif token == 'do':
                self.compile_do()
            elif token == 'return':
                self.compile_return()
            token = self.tokenizer.output_token[self.token_index]

    def compile_do(self):
        self.token_index += 1  # do
        self.compile_subroutine_call()
        self.vm_writer.write_pop("temp", 0)
        self.token_index += 1

    def compile_subroutine_call(self):
        num_of_parm = 0
        token_name = self.tokenizer.output_token[self.token_index]
        self.token_index += 1
        token = self.tokenizer.output_token[self.token_index]
        if token == '.':
            self.token_index += 1
            func_name = self.tokenizer.output_token[self.token_index]
            if self.table.kind_of(token_name) is not None:
                type_of = self.table.type_of(token_name)
                paire = [type_of, func_name]
                num_of_parm += 1
                self.pushing(token_name)
            else:
                paire = [token_name, func_name]
            self.token_index += 1
        else:  # token == "(":
            self.vm_writer.write_push("pointer", 0)
            paire = [self.name_of_class, token_name]
            num_of_parm += 1
        self.token_index += 1

        num_of_parm += self.compile_expression_list()
        self.token_index += 1

        self.vm_writer.write_call('.'.join(paire), num_of_parm)

    def compile_expression_list(self):
        sum = 0
        token = self.tokenizer.output_token[self.token_index]
        while token != ")":
            self.compile_expression()
            token = self.tokenizer.output_token[self.token_index]
            if token == ',':
                self.token_index += 1
            sum += 1
        return sum

    def compile_expression(self):
        self.compile_term()
        token = self.tokenizer.output_token[self.token_index]
        while token in {"+", "-", "*", "/", "&", "|", "<", ">", "="}:
            arithmetic = token
            self.token_index += 1
            self.compile_term()
            self.vm_writer.write_arithmetic(arithmetic)
            token = self.tokenizer.output_token[self.token_index]

    def poping(self, name):
        kindName = self.table.kind_of(name)
        if kindName is None:
            return
        indexName = self.table.index_of(name)
        if kindName == 'STATIC':
            self.vm_writer.write_pop('static', indexName)
        elif kindName == 'FIELD':
            self.vm_writer.write_pop('this', indexName)
        elif kindName == 'ARG':
            self.vm_writer.write_pop('argument', indexName)
        elif kindName == 'VAR':
            self.vm_writer.write_pop('local', indexName)

    def pushing(self, name):
        kindName = self.table.kind_of(name)
        if kindName is None:
            return
        indexName = self.table.index_of(name)
        if kindName == 'STATIC':
            self.vm_writer.write_push('static', indexName)
        elif kindName == 'FIELD':
            self.vm_writer.write_push('this', indexName)
        elif kindName == 'ARG':
            self.vm_writer.write_push('argument', indexName)
        elif kindName == 'VAR':
            self.vm_writer.write_push('local', indexName)

    def compile_class_var_dec(self):
        num_definitions = 0
        kind = self.tokenizer.output_token[self.token_index]  # 'field', 'static', 'var'
        self.token_index += 1
        type = self.tokenizer.output_token[self.token_index]
        self.token_index += 1
        name = self.tokenizer.output_token[self.token_index]
        self.token_index += 1
        self.table.define_symbol(name, type, KIND_DICT[kind])
        num_definitions += 1
        token = self.tokenizer.output_token[self.token_index]
        while token != ';':
            if token != ',':
                name = token
                self.table.define_symbol(name, type, KIND_DICT[kind])
                num_definitions += 1
            self.token_index += 1
            token = self.tokenizer.output_token[self.token_index]
        self.token_index += 1
        return num_definitions

    def compile_subroutine(self):
        type_func = self.tokenizer.output_token[self.token_index]  # constructor, method, function
        self.token_index += 1
        return_value = self.tokenizer.output_token[self.token_index]
        self.token_index += 1
        name_func = self.tokenizer.output_token[self.token_index]
        self.token_index += 1  # '('
        next_token = self.tokenizer.output_token[self.token_index + 1]
        self.token_index += 1
        if type_func == 'method':
            self.table.define_symbol('this', self.name_of_class, 'ARG')
        if next_token != ')':
            self.compile_parameter_list()
        else:
            self.token_index += 1  # ')'
        self.token_index += 1  # '{'
        self.compile_subroutine_body(type_func, return_value, name_func)
        self.token_index += 1  # '{'

    def compile_subroutine_body(self, type_func, return_value, name_func):
        token = self.tokenizer.output_token[self.token_index]
        num_vars = 0

        if token == '{':
            self.token_index += 1
            token = self.tokenizer.output_token[self.token_index]

        while token == 'var':
            num_vars += self.compile_class_var_dec()
            token = self.tokenizer.output_token[self.token_index]
        self.vm_writer.write_function(self.name_of_class + '.' + name_func, num_vars)
        if type_func == 'method':
            self.vm_writer.write_push("argument", 0)
            self.vm_writer.write_pop("pointer", 0)
        elif type_func == 'constructor':
            self.vm_writer.write_push("constant", self.table.var_count("FIELD"))
            self.vm_writer.write_call("Memory.alloc", 1)
            self.vm_writer.write_pop("pointer", 0)

        self.compile_statements()

    def compile_let(self):
        self.token_index += 1
        name = self.tokenizer.output_token[self.token_index]
        self.token_index += 1
        if self.tokenizer.output_token[self.token_index] == "[":
            self.token_index += 1

            self.compile_expression()
            self.pushing(name)
            self.vm_writer.write_arithmetic("+")
            self.token_index += 1  # '['

            self.token_index += 1  # '='
            self.compile_expression()
            self.vm_writer.write_pop("temp", 0)
            self.vm_writer.write_pop("pointer", 1)
            self.vm_writer.write_push("temp", 0)
            self.vm_writer.write_pop("that", 0)

        else:  # '='
            self.token_index += 1
            self.compile_expression()
            self.poping(name)
        self.token_index += 1  # ';'

    def compile_while(self):
        while_index = self.while_counter
        self.while_counter += 1
        self.vm_writer.write_label('WHILE_EXP' + str(while_index))
        self.token_index += 2  # while(
        self.compile_expression()
        self.token_index += 1  # )
        self.vm_writer.write_arithmetic("~")
        self.vm_writer.write_if("WHILE_END" + str(while_index))
        self.token_index += 1  # {
        self.compile_statements()
        self.token_index += 1  # }
        self.vm_writer.write_goto("WHILE_EXP" + str(while_index))
        self.vm_writer.write_label("WHILE_END" + str(while_index))

    def compile_return(self):
        self.token_index += 1
        token = self.tokenizer.output_token[self.token_index]
        if token != ';':
            self.compile_expression()
        else:
            self.vm_writer.write_push('constant', 0)
        self.vm_writer.write_return()
        self.token_index += 1  # '}'

    def compile_if(self):
        self.token_index += 2  # '('
        self.compile_expression()
        self.token_index += 1  # ')'
        if_num = self.if_counter

        self.vm_writer.write_if('IF_TRUE' + str(if_num))
        self.vm_writer.write_goto('IF_FALSE' + str(if_num))
        self.vm_writer.write_label('IF_TRUE' + str(if_num))
        self.if_counter += 1
        self.token_index += 1  # '{'
        self.compile_statements()
        self.token_index += 1  # '}'

        token = self.tokenizer.output_token[self.token_index]
        if token == 'else':
            self.vm_writer.write_goto('IF_END' + str(if_num))
            self.vm_writer.write_label('IF_FALSE' + str(if_num))
            self.token_index += 2  # 'else {'
            self.compile_statements()
            self.token_index += 1  # '}'
            self.vm_writer.write_label('IF_END' + str(if_num))
        else:
            self.vm_writer.write_label('IF_FALSE' + str(if_num))

    def write_string(self, string_token):
        val = self.tokenizer.stringVal(string_token)
        self.vm_writer.write_push('constant', len(val))
        self.vm_writer.write_call('String.new', 1)
        for char in val:
            self.vm_writer.write_push('constant', ord(char))
            self.vm_writer.write_call('String.appendChar', 2)

    def compile_term(self):
        token = self.tokenizer.output_token[self.token_index]
        token_type = self.tokenizer.tokenType(token)
        if token_type == 'INT_CONST':
            self.vm_writer.write_push('constant', token)
            self.token_index += 1
        elif token_type == 'STRING_CONST':
            self.write_string(token)
            self.token_index += 1

        elif token == '(':
            self.token_index += 1  # '('
            self.compile_expression()
            self.token_index += 1  # ')'

        elif token in UNARY_OP_TYPES:
            unary_op = token
            self.token_index += 1
            self.compile_term()
            if unary_op == '-':
                unary_op = '--'
            self.vm_writer.write_arithmetic(unary_op)

        elif token_type == 'IDENTIFIER':
            self.token_index += 1
            next_token = self.tokenizer.output_token[self.token_index]
            if next_token in ['(', '.']:
                self.token_index -= 1
                self.compile_subroutine_call()
            elif next_token == '[':
                self.token_index += 1
                self.compile_array(token)
                self.token_index += 1
            else:
                self.pushing(token)
        else:  # token is KEYWORD
            if token == 'true':
                self.vm_writer.write_push('constant', 0)
                self.vm_writer.write_arithmetic('~')
            elif token == 'this':
                self.vm_writer.write_push('pointer', 0)
            else:
                self.vm_writer.write_push('constant', 0)
            self.token_index += 1

    def compile_array(self, name):
        self.compile_expression()
        self.pushing(name)
        self.vm_writer.write_arithmetic('+')
        self.vm_writer.write_pop('pointer', 1)
        self.vm_writer.write_push('that', 0)
