from src.tokens import TokenType
from src.symbols_table import SymbolTable, TableEntry
class Parser:

    def __init__(self, tokens: str):
        self.tokens = tokens
        self.idx = 0
        self.qtd_error = 0
        
        self.table_symbols = {}
        self.curr_table = ""
        self.param_pos = 0

    def parse(self) -> list[tuple[str, str, int]]:
        self.program()
        print(f'Analise Sintatica concluida: {self.qtd_error} erro(s) encontrado(s)')
    
    def error(self, expected_tokens: list[TokenType]):
        self.qtd_error += 1
        token = self.get_current_token()[0]
        nline = self.tokens[self.idx-1][2]
        expected_tokens = [t.name for t in expected_tokens]
        print(f'Erro linha {nline}:\n\tEsperado(s) {",".join(expected_tokens)}\n\tEncontrado {token.name}')

    def match(self, expected_token: TokenType):
        token = self.get_current_token()[0]
        if token == expected_token:
            self.idx += 1
        else:
            self.error([expected_token])            

    def program(self):
        self.function()
        self.function_sequence()

    def function(self):
        self.match(TokenType.KEYWORD_FUNCTION)
        
        self.table_symbols[self.get_current_token()[1]] = SymbolTable()
        self.curr_table = self.get_current_token()[1]
        self.param_pos = 0

        self.match(TokenType.IDENTIFIER)
        self.match(TokenType.PUNCTUATOR_LPAREN)
        self.parameter_list()
        self.match(TokenType.PUNCTUATOR_RPAREN)
        self.return_type()
        self.block()

    def function_sequence(self):
        if self.get_current_token() and self.get_current_token()[0] == TokenType.KEYWORD_FUNCTION:
            self.function()
            self.function_sequence()

    def parameter_list(self):
        if self.get_current_token()[0] == TokenType.IDENTIFIER:

            lexem = self.get_current_token()[1]

            self.match(TokenType.IDENTIFIER)
            self.match(TokenType.PUNCTUATOR_COLON)
            type_ = self.type_()

            entry = TableEntry('parameter', lexem, type_, self.param_pos)
            self.table_symbols[self.curr_table].insertEntry(lexem, entry)
            self.param_pos += 1

            if self.get_current_token()[0] == TokenType.PUNCTUATOR_COMMA:
                self.match(TokenType.PUNCTUATOR_COMMA)
                self.parameter_list()

    def return_type(self):
        if self.get_current_token()[0] == TokenType.SYMBOL_ARROW:
            self.match(TokenType.SYMBOL_ARROW)
            self.type_()

    def type_(self):
        token = self.get_current_token()[0]
        first = [TokenType.KEYWORD_INT, TokenType.KEYWORD_FLOAT, TokenType.KEYWORD_CHAR]
        if token in first:
            self.match(token)
            return token
        else:
            self.error(first)

    def block(self):
        self.match(TokenType.PUNCTUATOR_LBRACE)
        self.sequence()
        self.match(TokenType.PUNCTUATOR_RBRACE)

    def sequence(self):
        token = self.get_current_token()[0]
        if token == TokenType.KEYWORD_LET:
            self.declaration()
            self.sequence()
        elif token in [TokenType.IDENTIFIER, TokenType.KEYWORD_WHILE, TokenType.KEYWORD_PRINT, TokenType.KEYWORD_PRINTLN, TokenType.KEYWORD_RETURN, TokenType.KEYWORD_IF]:
            self.statement()
            self.sequence()

    def declaration(self):

        self.lexems = []

        self.match(TokenType.KEYWORD_LET)
        self.variable_list()
        self.match(TokenType.PUNCTUATOR_COLON)
        type_ = self.type_()
        for lexem in self.lexems:
            entry = TableEntry('variable', lexem, type_)
            self.table_symbols[self.curr_table].insertEntry(lexem, entry)
        self.match(TokenType.PUNCTUATOR_SEMICOLON)

    def variable_list(self):
        self.lexems.append(self.get_current_token()[1])
        self.match(TokenType.IDENTIFIER)

        if self.get_current_token()[0] == TokenType.PUNCTUATOR_COMMA:
            self.match(TokenType.PUNCTUATOR_COMMA)
            self.variable_list()

    def statement(self):
        token = self.get_current_token()[0]
        first = [TokenType.IDENTIFIER, TokenType.KEYWORD_IF, TokenType.PUNCTUATOR_LBRACE, TokenType.KEYWORD_WHILE, TokenType.KEYWORD_RETURN]
        if token == TokenType.IDENTIFIER:
            self.match(TokenType.IDENTIFIER)
            self.assignment_or_call()
        elif token in [TokenType.KEYWORD_IF, TokenType.PUNCTUATOR_LBRACE]:
            self.if_statement()
        elif token == TokenType.KEYWORD_WHILE:
            self.match(TokenType.KEYWORD_WHILE)
            self.expression()
            self.block()
        elif token in [TokenType.KEYWORD_PRINT, TokenType.KEYWORD_PRINTLN]:
            self.match(token)
            self.match(TokenType.PUNCTUATOR_LPAREN)
            self.match(TokenType.FORMATTED_STRING)
            self.match(TokenType.PUNCTUATOR_COMMA)
            self.argument_list()
            self.match(TokenType.PUNCTUATOR_RPAREN)
            self.match(TokenType.PUNCTUATOR_SEMICOLON)
        elif token == TokenType.KEYWORD_RETURN:
            self.match(TokenType.KEYWORD_RETURN)
            self.expression()
            self.match(TokenType.PUNCTUATOR_SEMICOLON)
        else:
            self.error(first)

    def assignment_or_call(self):
        token = self.get_current_token()[0]
        first = [TokenType.OPERATOR_ASSIGN, TokenType.PUNCTUATOR_LPAREN]
        if token == TokenType.OPERATOR_ASSIGN:
            self.match(TokenType.OPERATOR_ASSIGN)
            self.expression()
            self.match(TokenType.PUNCTUATOR_SEMICOLON)
        elif token == TokenType.PUNCTUATOR_LPAREN:
            self.match(TokenType.PUNCTUATOR_LPAREN)
            self.argument_list()
            self.match(TokenType.PUNCTUATOR_RPAREN)
        else:
            self.error(first)

    def if_statement(self):
        token = self.get_current_token()[0]
        first = [TokenType.KEYWORD_IF, TokenType.PUNCTUATOR_LBRACE]
        if token == TokenType.KEYWORD_IF:
            self.match(TokenType.KEYWORD_IF)
            self.expression()
            self.block()
            self.else_statement()
        elif token == TokenType.PUNCTUATOR_LBRACE:
            self.block()
        else:
            self.error(first)

    def else_statement(self):
        if self.get_current_token()[0] == TokenType.KEYWORD_ELSE:
            self.match(TokenType.KEYWORD_ELSE)
            self.if_statement()

    def expression(self):
        self.relative()
        self.expression_optional()

    def relative(self):
        self.additive()
        self.relative_optional()

    def additive(self):
        self.term()
        self.additive_optional()

    def term(self):
        self.factor()
        self.term_optional()

    def term_optional(self):
        if self.get_current_token()[0] in [TokenType.OPERATOR_MULTIPLY, TokenType.OPERATOR_DIVIDE]:
            self.operator_mult()
            self.factor()
            self.term_optional()

    def operator_mult(self):
        token = self.get_current_token()[0]
        if token in [TokenType.OPERATOR_MULTIPLY, TokenType.OPERATOR_DIVIDE]:
            self.match(token)

    def additive_optional(self):
        if self.get_current_token()[0] in [TokenType.OPERATOR_PLUS, TokenType.OPERATOR_MINUS]:
            self.operator_add()
            self.term()
            self.additive_optional()

    def operator_add(self):
        token = self.get_current_token()[0]
        if token in [TokenType.OPERATOR_PLUS, TokenType.OPERATOR_MINUS]:
            self.match(token)

    def relative_optional(self):
        if self.get_current_token()[0] in [TokenType.OPERATOR_LE, TokenType.OPERATOR_LT, TokenType.OPERATOR_GE, TokenType.OPERATOR_GT]:
            self.operator_rel()
            self.additive()
            self.relative_optional()

    def operator_rel(self):
        token = self.get_current_token()[0]
        if token in [TokenType.OPERATOR_LT, TokenType.OPERATOR_LE, TokenType.OPERATOR_GT, TokenType.OPERATOR_GE]:
            self.match(token)

    def factor(self):
        token = self.get_current_token()[0]
        first = [TokenType.IDENTIFIER, TokenType.INT_CONSTANT, TokenType.FLOAT_CONSTANT, TokenType.CHAR_LITERAL, TokenType.PUNCTUATOR_LPAREN]
        if token == TokenType.IDENTIFIER:
            self.match(TokenType.IDENTIFIER)
            self.function_call()
        elif token in [TokenType.INT_CONSTANT, TokenType.FLOAT_CONSTANT, TokenType.CHAR_LITERAL]:
            self.match(token)
        elif token == TokenType.PUNCTUATOR_LPAREN:
            self.match(TokenType.PUNCTUATOR_LPAREN)
            self.expression()
            self.match(TokenType.PUNCTUATOR_RPAREN)
        else:
            self.error(first)

    def expression_optional(self):
        token = self.get_current_token()[0]
        if token in [TokenType.SYMBOL_EQUAL, TokenType.SYMBOL_DIFF]:
            self.operator_equal()
            self.relative()
            self.expression_optional()

    def operator_equal(self):
        token = self.get_current_token()[0]
        if token in [TokenType.SYMBOL_EQUAL, TokenType.SYMBOL_DIFF]:
            self.match(token)

    def function_call(self):
        if self.get_current_token()[0] == TokenType.PUNCTUATOR_LPAREN:
            self.match(TokenType.PUNCTUATOR_LPAREN)
            self.argument_list()
            self.match(TokenType.PUNCTUATOR_RPAREN)

    def argument_list(self):
        if self.get_current_token()[0] in [TokenType.IDENTIFIER, TokenType.INT_CONSTANT, TokenType.FLOAT_CONSTANT, TokenType.CHAR_LITERAL, TokenType.PUNCTUATOR_LPAREN]:
            self.expression()
            if self.get_current_token()[0] == TokenType.PUNCTUATOR_COMMA:
                self.match(TokenType.PUNCTUATOR_COMMA)
                self.argument_list()

    def get_current_token(self):
        if self.idx < len(self.tokens):
            return self.tokens[self.idx]

