import json

class SymbolTable:
    def __init__(self):
        self.table = {}
    def insertEntry(self, lexema, entry):
        self.table[lexema] = entry
    def getEntry(self, lexema):
        return self.table[lexema]
    def __str__(self):
        return '\n'.join([str(entry) for entry in self.table.values()])

class TableEntry:
    def __init__(self, category, lexem, type, pos_param = -1):
        self.lexem = lexem
        self.type = type
        self.category = category
        self.pos_param = pos_param
    
    def __str__(self):
        return f'\t{self.lexem} -> {self.category} {self.type} {self.pos_param}'