from src.tokens import TokenType
from src.symbols import Symbols
import enum

class Lexer:

    """
    This class breaks down the input text into a sequence of tokens,
    identifying identifiers, keywords, operators, literals, and other
    syntactic elements of the language.
    """

    def __init__(self, input_text: str):
        """
        Initializes the Lexer with the input text.

        Args:
            input_text (str): Text to be processed
        """
        
        self.text = input_text
        self.idx = 0
        self.line = 1
        self.tokens = []
        self.errors = 0

    def process(self) -> list[tuple[str, str, int]]:
        """
        Performs lexical analysis on the input text.

        Returns:
            list[tuple[str, str, int]]: A list of tokens, where each token is a tuple
                                        (token name, lexeme, line number).
        """

        while self.idx < len(self.text):
            self.get_next_token()
        return self.tokens, self.errors

    def get_next_token(self):
        """
        Reads the next token from the input text.
        """
        symbol = self.text[self.idx]

        # Skip whitespace
        if symbol == " ":
            self.idx += 1
            return

        # Check for newline
        if symbol == "\n":
            self.line += 1
            self.idx += 1
            return

        # Check for two-character operators (like "==" or "<=")
        if self.next_symbol() and symbol + self.next_symbol() in Symbols.operators:
            operator = symbol + self.next_symbol()
            self.add_token(TokenType.get_token(operator), operator)
            self.idx += 2
            return
        
        # Check for single-character operators
        if symbol in Symbols.operators + Symbols.pontuaction:
            self.add_token(TokenType.get_token(symbol), symbol)
            self.idx += 1
            return
        
        # # Check for identifiers or keywords
        if symbol in Symbols.letters:
            self.get_identifier_or_keyword()
            return

        # # Check for numbers
        if symbol in Symbols.digits:
            self.get_number()
            return
        
        # Check for char literal
        if symbol == "'":
            self.get_char_literal()
            return
        
        # Check for string literal
        if symbol == '"':
            self.get_string_formatted()
            return
        
        # Unknown character, mark as error
        self.add_token(TokenType.ERROR, symbol)
        self.error(symbol)
        self.idx += 1

    def get_identifier_or_keyword(self):
        """
        Reads an identifier or keyword from the input text.
        """
        start_pos = self.idx
        while self.next_symbol() is not None and (self.next_symbol() in Symbols.letters + Symbols.digits + ['_']):
            self.idx += 1
        self.idx += 1
        word = self.text[start_pos:self.idx]
        token_type = TokenType.get_token(word)
        self.add_token(token_type if token_type else TokenType.IDENTIFIER, word)

    def get_number(self):
        """
        Reads a number (integer or float) from the input text.
        """
        start_pos = self.idx
        while self.next_symbol() and self.next_symbol() in Symbols.digits:
            self.idx += 1
        if self.next_symbol() == '.' and self.next_symbol(2) and self.next_symbol(2) in Symbols.digits:
            self.idx += 1
            while self.next_symbol() and self.next_symbol() in Symbols.digits:
                self.idx += 1
            self.idx += 1
            self.add_token(TokenType.FLOAT_CONSTANT, self.text[start_pos:self.idx])
        else:
            self.idx += 1
            self.add_token(TokenType.INT_CONSTANT, self.text[start_pos:self.idx])

    def get_char_literal(self):
        """
        Reads a char ('symbol') from the input text.
        """
        if(self.next_symbol(2) and self.next_symbol(2) == "'" and \
           self.next_symbol() in Symbols.symbols):
            self.add_token(TokenType.CHAR_LITERAL, self.text[self.idx:self.idx+3])
        else:    
            self.add_token(TokenType.ERROR, self.text[self.idx:self.idx+3])
            self.error(self.text[self.idx:self.idx+3])
        self.idx += 3

    def get_string_formatted(self):
        """
        Reads a string formatted ("{}") from the input text.
        """
        if(self.next_symbol(3) and self.text[self.idx:self.idx+4] == '"{}"'):
            self.add_token(TokenType.FORMATTED_STRING, self.text[self.idx:self.idx+4])
        else:    
            self.add_token(TokenType.ERROR, self.text[self.idx:self.idx+3])
            self.error(self.text[self.idx:self.idx+3])
        self.idx += 4

    def next_symbol(self, offset: int = 1) -> str:
        """
        Get the next symbol with a definied offset.
        
        Args:
            offset (int): Distance to next symbol
        Returns:
            str: symbol in the offset position of input_text.
        """
        if self.idx + offset < len(self.text):
            return self.text[self.idx + offset]
        return None

    def add_token(self, token_type: enum.Enum, lexem: str) -> None:
        """
        Adds a token to the list of processed tokens.

        Args:
            token_type (enum.Enum): The token to be include.
            lexem (str): The lexem that generate the token.
        """
        self.tokens.append((token_type, lexem, self.line))
    
    def error(self, lexem: str):
        """
        Register an error in the output file.

        Args:
            lexem (str): The lexem that generate the token.
        """
        self.errors += 1
        with open('logs/error.log','+a') as fp:
            print(f'Erro Lexico:\n\tLinha: {self.line}\n\tLexem: {lexem}',file=fp)