class SymbolTable:
    tableClass = {}
    tableSubroutine = {}
    tableIndex = {}

    def __init__(self):
        self.tableClass = dict()
        self.tableSubroutine = dict()
        self.tableIndex = {'STATIC': 0, 'FIELD': 0, 'ARG': 0, 'VAR': 0}

    def start_subroutine(self):
        self.tableSubroutine.clear()
        self.tableIndex['ARG'] = 0
        self.tableIndex['VAR'] = 0

    def define_symbol(self, name, type, kind):
        if kind in ['STATIC', 'FIELD']:
            self.tableClass[name] = [type, kind, self.tableIndex[kind]]
            self.tableIndex[kind] += 1
        else:
            self.tableSubroutine[name] = [type, kind, self.tableIndex[kind]]
            self.tableIndex[kind] += 1

    def var_count(self, kind):
        return self.tableIndex[kind]

    def kind_of(self, name):
        if name in self.tableSubroutine:
            return self.tableSubroutine[name][1]
        elif name in self.tableClass:
            return self.tableClass[name][1]
        return None

    def type_of(self, name):
        if name in self.tableSubroutine:
            return self.tableSubroutine[name][0]
        elif name in self.tableClass:
            return self.tableClass[name][0]
        return None

    def index_of(self, name):
        if name in self.tableSubroutine:
            return self.tableSubroutine[name][2]
        elif name in self.tableClass:
            return self.tableClass[name][2]
        return -1




