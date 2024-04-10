Aqui está uma versão revisada e mais legível do seu código:

```python
from tokens import TokenType
from symbols import Symbols
from src.lexer import Lexer
import enum
import sys


class Parser:

    def __init__(self, tokens: str):
        self.tokens = tokens
        self.idx = 0

    def parse(self) -> list[tuple[str, str, int]]:
        return self.program()

    def match(self, expected_token):
        token = self.get_current_token()
        if token == expected_token:
            print(f'Token {token.name} reconhecido na entrada.')
            self.idx += 1
        else:
            print(f'Erro: esperado {expected_token.name}, encontrado {token.name}')
            self.idx += 1

    def program(self):
        self.function()
        self.function_sequence()

    def function(self):
        self.match(TokenType.KEYWORD_FUNCTION)
        self.match(TokenType.IDENTIFIER)
        self.match(TokenType.PUNCTUATOR_LPAREN)
        self.parameter_list()
        self.match(TokenType.PUNCTUATOR_RPAREN)
        self.return_type()
        self.block()

    def function_sequence(self):
        if self.get_current_token() == TokenType.KEYWORD_FUNCTION:
            self.function()
            self.function_sequence()

    def parameter_list(self):
        if self.get_current_token() == TokenType.IDENTIFIER:
            self.match(TokenType.IDENTIFIER)
            self.match(TokenType.PUNCTUATOR_COLON)
            self.type_()
            if self.get_current_token() == TokenType.PUNCTUATOR_COMMA:
                self.match(TokenType.PUNCTUATOR_COMMA)
                self.parameter_list()

    def return_type(self):
        if self.get_current_token() == TokenType.SYMBOL_ARROW:
            self.match(TokenType.SYMBOL_ARROW)
            self.type_()

    def type_(self):
        token = self.get_current_token()
        if token in [TokenType.KEYWORD_INT, TokenType.KEYWORD_FLOAT, TokenType.KEYWORD_CHAR]:
            self.match(token)

    def block(self):
        self.match(TokenType.PUNCTUATOR_LBRACE)
        self.sequence()
        self.match(TokenType.PUNCTUATOR_RBRACE)

    def sequence(self):
        token = self.get_current_token()
        if token == TokenType.KEYWORD_LET:
            self.declaration()
            self.sequence()
        elif token in [TokenType.IDENTIFIER, TokenType.KEYWORD_WHILE, TokenType.KEYWORD_PRINT, TokenType.KEYWORD_PRINTLN, TokenType.KEYWORD_RETURN, TokenType.KEYWORD_IF]:
            self.statement()
            self.sequence()

    def declaration(self):
        self.match(TokenType.KEYWORD_LET)
        self.variable_list()
        self.match(TokenType.PUNCTUATOR_COLON)
        self.type_()
        self.match(TokenType.PUNCTUATOR_SEMICOLON)

    def variable_list(self):
        self.match(TokenType.IDENTIFIER)
        if self.get_current_token() == TokenType.PUNCTUATOR_COMMA:
            self.match(TokenType.PUNCTUATOR_COMMA)
            self.variable_list()

    def statement(self):
        token = self.get_current_token()
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

    def assignment_or_call(self):
        token = self.get_current_token()
        if token == TokenType.OPERATOR_ASSIGN:
            self.match(TokenType.OPERATOR_ASSIGN)
            self.expression()
            self.match(TokenType.PUNCTUATOR_SEMICOLON)
        elif token == TokenType.PUNCTUATOR_LPAREN:
            self.match(TokenType.PUNCTUATOR_LPAREN)
            self.argument_list()
            self.match(TokenType.PUNCTUATOR_RPAREN)
        else:
            print(f'Erro: atribuição ou chamada {token.name}')

    def if_statement(self):
        token = self.get_current_token()
        if token == TokenType.KEYWORD_IF:
            self.match(TokenType.KEYWORD_IF)
            self.expression()
            self.block()
            self.else_statement()
        elif token == TokenType.PUNCTUATOR_LBRACE:
            self.block()
        else:
            print('Erro: comando if')

    def else_statement(self):
        if self.get_current_token() == TokenType.KEYWORD_ELSE:
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
        if self.get_current_token() in [TokenType.OPERATOR_MULTIPLY, TokenType.OPERATOR_DIVIDE]:
            self.operator_mult()
            self.factor()
            self.term_optional()

    def operator_mult(self):
        token = self.get_current_token()
        if token in [TokenType.OPERATOR_MULTIPLY, TokenType.OPERATOR_DIVIDE]:
            self.match(token)

    def additive_optional(self):
        if self.get_current_token() in [TokenType.OPERATOR_PLUS, TokenType.OPERATOR_MINUS]:
            self.operator_add()
            self.term()
            self.additive_optional()

    def operator_add(self):
        token = self.get_current_token()
        if token in [TokenType.OPERATOR_PLUS, TokenType.OPERATOR_MINUS]:
            self.match(token)

    def relative_optional(self):
        if self.get_current_token() in [TokenType.OPERATOR_LE, TokenType.OPERATOR_LT, TokenType.OPERATOR_GE, TokenType.OPERATOR_GT]:
            self.operator_rel()
            self.additive()
            self.relative_optional()

    def operator_rel(self):
        token = self.get_current_token()
        if token in [TokenType.OPERATOR_LT, TokenType.OPERATOR_LE, TokenType.OPERATOR_GT, TokenType.OPERATOR_GE]:
            self.match(token)

    def factor(self):
        token = self.get_current_token()
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
            print('Erro: fator')

    def expression_optional(self):
        token = self.get_current_token()
        if token in [TokenType.SYMBOL_EQUAL, TokenType.SYMBOL_DIFF]:
            self.operator_equal()
            self.relative()
            self.expression_optional()

    def operator_equal(self):
        token = self.get_current_token()
        if token in [TokenType.SYMBOL_EQUAL, TokenType.SYMBOL_DIFF]:
            self.match(token)

    def function_call(self):
        if self.get_current_token() == TokenType.PUNCTUATOR_LPAREN:
            self.match(TokenType.PUNCTUATOR_LPAREN)
            self.argument_list()
            self.match(TokenType.PUNCTUATOR_RPAREN)

    def argument_list(self):
        if self.get_current_token() in [TokenType.IDENTIFIER, TokenType.INT_CONSTANT, TokenType.FLOAT_CONSTANT, TokenType.CHAR_LITERAL, TokenType.PUNCTUATOR_LPAREN]:
            self.expression()
            if self.get_current_token() == TokenType.PUNCTUATOR_COMMA:
                self.match(TokenType.PUNCTUATOR_COMMA)
                self.argument_list()

    def get_current_token(self):
        if self.idx < len(self.tokens):
            return self.tokens[self.idx][0]


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Erro: Arquivo não especificado.")
        print("Uso: python lexer.py <caminho_do_arquivo>")
        exit()

    file_name = sys.argv[1]

    try:
        with open(file_name, "r") as file:
            text = file.read()
    except FileNotFoundError:
        print("Erro: Arquivo não encontrado.")
        exit()

    tokens = Lexer(text).process()

    Parser(tokens).parse()
    def operator_equal(self):
        token = self.get_current_token()
        if token in [TokenType.SYMBOL_EQUAL, TokenType.SYMBOL_DIFF]:
            self.match(token)

    def function_call(self):
        if self.get_current_token() == TokenType.PUNCTUATOR_LPAREN:
            self.match(TokenType.PUNCTUATOR_LPAREN)
            self.argument_list()
            self.match(TokenType.PUNCTUATOR_RPAREN)

    def argument_list(self):
        if self.get_current_token() in [TokenType.IDENTIFIER, TokenType.INT_CONSTANT, TokenType.FLOAT_CONSTANT, TokenType.CHAR_LITERAL, TokenType.PUNCTUATOR_LPAREN]:
            self.expression()
            if self.get_current_token() == TokenType.PUNCTUATOR_COMMA:
                self.match(TokenType.PUNCTUATOR_COMMA)
                self.argument_list()

    def get_current_token(self):
        if self.idx < len(self.tokens):
            return self.tokens[self.idx][0]


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Erro: Arquivo não especificado.")
        print("Uso: python parser.py <caminho_do_arquivo>")
        exit()

    file_name = sys.argv[1]

    try:
        with open(file_name, "r") as file:
            text = file.read()
    except FileNotFoundError:
        print("Erro: Arquivo não encontrado.")
        exit()

    tokens = Lexer(text).process()

    Parser(tokens).parse()