from src.tokens import TokenType
from src.symbols_table import SymbolTable, TableEntry
import src.ast as AST
class Parser:

    def __init__(self, tokens: str):
        self.tokens = tokens
        self.idx = 0
        self.qtd_error = 0
        
        # For symbol tables
        self.table_symbols = {}
        self.lexems = []
        self.curr_table = ""
        self.param_pos = 0


        self.trees = []

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

        node_fn = AST.NodeFunction(self.get_current_token()[1])

        # For symbol tables
        self.table_symbols[self.get_current_token()[1]] = SymbolTable()
        self.curr_table = self.get_current_token()[1]
        self.param_pos = 0

        self.match(TokenType.IDENTIFIER)
        self.match(TokenType.PUNCTUATOR_LPAREN)
        self.parameter_list()
        self.match(TokenType.PUNCTUATOR_RPAREN)
        self.return_type()
        node_block = self.block()

        node_fn.children.append(node_block)

        self.trees.append(node_fn)

    def function_sequence(self):
        if self.get_current_token() and self.get_current_token()[0] == TokenType.KEYWORD_FUNCTION:
            self.function()
            self.function_sequence()

    def parameter_list(self):
        if self.get_current_token()[0] == TokenType.IDENTIFIER:

            # For symbol tables
            lexem = self.get_current_token()[1]

            self.match(TokenType.IDENTIFIER)
            self.match(TokenType.PUNCTUATOR_COLON)
            node = self.type_()
            
            # For symbol tables
            entry = TableEntry('parameter', lexem, node.type, self.param_pos)
            error = self.table_symbols[self.curr_table].insertEntry(lexem, entry)
            self.param_pos += 1
            self.qtd_error += error

            if self.get_current_token()[0] == TokenType.PUNCTUATOR_COMMA:
                self.match(TokenType.PUNCTUATOR_COMMA)
                self.parameter_list()

    def return_type(self):
        if self.get_current_token()[0] == TokenType.SYMBOL_ARROW:
            self.match(TokenType.SYMBOL_ARROW)
            self.type_()

    def type_(self):
        token = self.get_current_token()
        if token[0] == TokenType.KEYWORD_INT:
            node = AST.NodeIntConst(token[1])
            self.match(TokenType.KEYWORD_INT)
            return node
        elif token[0] == TokenType.KEYWORD_FLOAT:
            node = AST.NodeFloatConst(token[1])
            self.match(TokenType.KEYWORD_FLOAT)
            return node
        elif token[0] == TokenType.KEYWORD_CHAR:
            node = AST.NodeCharConst(token[1])
            self.match(TokenType.KEYWORD_CHAR)
            return node
        else:
            self.error([TokenType.KEYWORD_INT, TokenType.KEYWORD_FLOAT, TokenType.KEYWORD_CHAR])

    def block(self):
        self.match(TokenType.PUNCTUATOR_LBRACE)
        node_block = AST.NodeBlock()
        self.sequence(node_block)
        self.match(TokenType.PUNCTUATOR_RBRACE)
        return node_block

    def sequence(self, node_block):
        token = self.get_current_token()
        if token[0] == TokenType.KEYWORD_LET:
            self.declaration()
            self.sequence(node_block)
        elif token[0] in [TokenType.IDENTIFIER, TokenType.KEYWORD_WHILE, TokenType.KEYWORD_PRINT, TokenType.KEYWORD_PRINTLN, TokenType.KEYWORD_RETURN, TokenType.KEYWORD_IF]:
            node_st = self.statement()
            node_block.children.append(node_st)
            self.sequence(node_block)
        
        return node_block

    def declaration(self):

        self.lexems = []

        self.match(TokenType.KEYWORD_LET)
        self.variable_list()
        self.match(TokenType.PUNCTUATOR_COLON)
        node = self.type_()

        # For symbol tables
        for lexem in self.lexems:
            entry = TableEntry('variable', lexem, node.type)
            error = self.table_symbols[self.curr_table].insertEntry(lexem, entry)
            self.qtd_error += error
        self.match(TokenType.PUNCTUATOR_SEMICOLON)

    def variable_list(self):
        # For symbol tables
        self.lexems.append(self.get_current_token()[1])
        
        self.match(TokenType.IDENTIFIER)
        if self.get_current_token()[0] == TokenType.PUNCTUATOR_COMMA:
            self.match(TokenType.PUNCTUATOR_COMMA)
            self.variable_list()

    def statement(self):
        token = self.get_current_token()
        first = [TokenType.IDENTIFIER, TokenType.KEYWORD_IF, TokenType.PUNCTUATOR_LBRACE, TokenType.KEYWORD_WHILE, TokenType.KEYWORD_RETURN]
        if token[0] == TokenType.IDENTIFIER:
            node_id = AST.NodeId(self.get_current_token()[1], self.table_symbols[self.curr_table].getEntry(self.get_current_token()[1]).type)
            self.match(TokenType.IDENTIFIER)
            return self.assignment_or_call(node_id)
        elif token[0] in [TokenType.KEYWORD_IF, TokenType.PUNCTUATOR_LBRACE]:
            return self.if_statement()
        elif token[0] == TokenType.KEYWORD_WHILE:
            self.match(TokenType.KEYWORD_WHILE)
            node_exp = self.expression()
            node_block = self.block()
            return AST.NodeWhile(node_exp, node_block)
        elif token[0] in [TokenType.KEYWORD_PRINT, TokenType.KEYWORD_PRINTLN]:
            self.match(token[0])
            self.match(TokenType.PUNCTUATOR_LPAREN)
            self.match(TokenType.FORMATTED_STRING)
            self.match(TokenType.PUNCTUATOR_COMMA)
            node_exp = self.argument_list()
            self.match(TokenType.PUNCTUATOR_RPAREN)
            self.match(TokenType.PUNCTUATOR_SEMICOLON)
            return AST.NodePrint(node_exp, token[1])
        elif token[0] == TokenType.KEYWORD_RETURN:
            self.match(TokenType.KEYWORD_RETURN)
            node_exp = self.expression()
            self.match(TokenType.PUNCTUATOR_SEMICOLON)
            return AST.NodeReturn(node_exp)
        else:
            self.error(first)

    def assignment_or_call(self, node_id):
        token = self.get_current_token()[0]
        first = [TokenType.OPERATOR_ASSIGN, TokenType.PUNCTUATOR_LPAREN]
        if token == TokenType.OPERATOR_ASSIGN:
            self.match(TokenType.OPERATOR_ASSIGN)
            node_exp = self.expression()
            self.match(TokenType.PUNCTUATOR_SEMICOLON)
            return AST.NodeAssign(node_id, node_exp)
        elif token == TokenType.PUNCTUATOR_LPAREN:
            print('chamada de funcao')
            self.function_call()
        else:
            self.error(first)

    def if_statement(self):
        token = self.get_current_token()
        first = [TokenType.KEYWORD_IF, TokenType.PUNCTUATOR_LBRACE]
        if token[0] == TokenType.KEYWORD_IF:
            self.match(TokenType.KEYWORD_IF)
            node_exp = self.expression()
            node_block = self.block()
            node_else = self.else_statement()
            return AST.NodeIf(node_exp, node_block, node_else)
        elif token == TokenType.PUNCTUATOR_LBRACE:
            return self.block()
        else:
            self.error(first)
            return None
        
    def else_statement(self):
        if self.get_current_token()[0] == TokenType.KEYWORD_ELSE:
            self.match(TokenType.KEYWORD_ELSE)
            return self.if_statement()

        return None

    def expression(self):
        node_rel = self.relative()
        return self.expression_optional(node_rel)

    def relative(self):
        node_add = self.additive()
        return self.relative_optional(node_add)

    def additive(self):
        node_term = self.term()
        return self.additive_optional(node_term)

    def term(self):
        node_factor = self.factor()
        return self.term_optional(node_factor)

    def term_optional(self, node_factor):
        token = self.get_current_token()
        if token[0] in [TokenType.OPERATOR_MULTIPLY, TokenType.OPERATOR_DIVIDE]:
            self.operator_mult()
            node_factor2 = self.factor()
            node_mult = AST.NodeExprAritmetica(token[1], node_factor, node_factor2)
            return self.term_optional(node_mult)
        return node_factor

    def operator_mult(self):
        token = self.get_current_token()[0]
        if token in [TokenType.OPERATOR_MULTIPLY, TokenType.OPERATOR_DIVIDE]:
            self.match(token)

    def additive_optional(self, node_factor):
        token = self.get_current_token()
        if token[0] in [TokenType.OPERATOR_PLUS, TokenType.OPERATOR_MINUS]:
            self.operator_add()
            node_factor2 = self.term()
            node_add = AST.NodeExprAritmetica(token[1], node_factor, node_factor2)
            return self.additive_optional(node_add)
        return node_factor
    
    def operator_add(self):
        token = self.get_current_token()[0]
        if token in [TokenType.OPERATOR_PLUS, TokenType.OPERATOR_MINUS]:
            self.match(token)

    def relative_optional(self, node_factor):
        token = self.get_current_token()
        if token[0] in [TokenType.OPERATOR_LE, TokenType.OPERATOR_LT, TokenType.OPERATOR_GE, TokenType.OPERATOR_GT]:
            self.operator_rel()
            node_factor2 = self.additive()
            node_add = AST.NodeExprAritmetica(token[1], node_factor, node_factor2)
            return self.relative_optional(node_add)
        return node_factor

    def operator_rel(self):
        token = self.get_current_token()[0]
        if token in [TokenType.OPERATOR_LT, TokenType.OPERATOR_LE, TokenType.OPERATOR_GT, TokenType.OPERATOR_GE]:
            self.match(token)

    def factor(self):
        token = self.get_current_token()
        first = [TokenType.IDENTIFIER, TokenType.INT_CONSTANT, TokenType.FLOAT_CONSTANT, TokenType.CHAR_LITERAL, TokenType.PUNCTUATOR_LPAREN]
        if token[0] == TokenType.IDENTIFIER:
            self.match(TokenType.IDENTIFIER)
            self.function_call()
            return AST.NodeId(token[1],self.table_symbols[self.curr_table].getEntry(token[1]).type)
        elif token[0] == TokenType.INT_CONSTANT:
            node = AST.NodeIntConst(self.get_current_token()[1])
            self.match(TokenType.INT_CONSTANT)
            return node
        elif token[0] == TokenType.FLOAT_CONSTANT:
            node = AST.NodeFloatConst(self.get_current_token()[1])
            self.match(TokenType.FLOAT_CONSTANT)
            return node
        elif token[0] == TokenType.CHAR_LITERAL:
            node = AST.NodeCharConst(self.get_current_token()[1])
            self.match(TokenType.CHAR_LITERAL)
            return node
        elif token[0] == TokenType.PUNCTUATOR_LPAREN:
            self.match(TokenType.PUNCTUATOR_LPAREN)
            node = self.expression()
            self.match(TokenType.PUNCTUATOR_RPAREN)
            return node
        else:
            self.error(first)

    def expression_optional(self, node_factor):
        token = self.get_current_token()
        if token[0] in [TokenType.SYMBOL_EQUAL, TokenType.SYMBOL_DIFF]:
            self.operator_equal()
            node_factor2 = self.relative()
            node_exp = AST.NodeExprAritmetica(token[1], node_factor, node_factor2)
            return self.expression_optional(node_exp)
        return node_factor
    
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
            node_exp = self.expression()
            if self.get_current_token()[0] == TokenType.PUNCTUATOR_COMMA:
                self.match(TokenType.PUNCTUATOR_COMMA)
                self.argument_list()
            return node_exp

    def get_current_token(self):
        if self.idx < len(self.tokens):
            return self.tokens[self.idx]

