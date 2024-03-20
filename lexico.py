from tokens import TokenType
from alphabet import Alphabet

class Lexico:
    def __init__(self, input_text):
        self.text = input_text
        self.idx = 0
        self.line = 1
        self.tokens = []

    def process(self):
        """
        Performs lexical analysis on the input text.
        """
        while self.idx < len(self.text):
            self.get_next_token()
        return self.tokens

    def get_next_token(self):
        """
        Reads the next token from the input text.
        """
        symbol = self.text[self.idx]

        # Skip whitespace
        if symbol.isspace():
            self.idx += 1
            return

        # Check for newline
        if symbol == '\n':
            self.line += 1
            self.idx += 1
            return

        # Check for two-character operators (like "==" or "<=")
        if self.next_symbol() and symbol + self.next_symbol() in Alphabet.operators:
            operator = symbol + self.next_symbol()
            self.add_token(TokenType.get_token(operator), operator)
            self.idx += 2
            return
        
        # Check for single-character operators
        if symbol in Alphabet.operators + Alphabet.pontuaction:
            self.add_token(TokenType.get_token(symbol), symbol)
            self.idx += 1
            return
        
        # # Check for identifiers or keywords
        if symbol in Alphabet.letters:
            self.get_identifier_or_keyword()
            return

        # # Check for numbers
        if symbol in Alphabet.digits:
            self.get_number()
            return
        
        # Check for char literal
        if symbol == "'":
            if(self.next_symbol(2) and self.next_symbol(2) == "'" and self.next_symbol() in Alphabet.symbols):
                self.add_token(TokenType.CHAR_LITERAL, self.text[self.idx:self.idx+3])
            else:    
                self.add_token(TokenType.ERROR, self.text[self.idx:self.idx+3])
            self.idx += 3
            return
        
        # Check for string literal
        if symbol == '"':
            if(self.next_symbol(3) and self.text[self.idx:self.idx+4] == '"{}"'):
                self.add_token(TokenType.FORMATTED_STRING, self.text[self.idx:self.idx+4])
            else:    
                self.add_token(TokenType.ERROR, self.text[self.idx:self.idx+3])
            self.idx += 4
            return
        
        # Unknown character, mark as error
        self.add_token(TokenType.ERROR, symbol)
        self.idx += 1

    def get_identifier_or_keyword(self):
        """
        Reads an identifier or keyword from the input text.
        """
        start_pos = self.idx
        while self.next_symbol() is not None and (self.next_symbol() in Alphabet.letters + Alphabet.digits + ['_']):
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
        while self.next_symbol() and self.next_symbol() in Alphabet.digits:
            self.idx += 1
        if self.next_symbol() == '.' and self.next_symbol(2) and self.next_symbol(2) in Alphabet.digits:
            self.idx += 1
            while self.next_symbol() and self.next_symbol() in Alphabet.digits:
                self.idx += 1
            self.idx += 1
            self.add_token(TokenType.FLOAT_CONSTANT, self.text[start_pos:self.idx])
        else:
            self.idx += 1
            self.add_token(TokenType.INT_CONSTANT, self.text[start_pos:self.idx])
        

    def next_symbol(self, offset=1):
        if self.idx + offset < len(self.text):
            return self.text[self.idx + offset]
        return None

    def add_token(self, token_type, value):
        """
        Adds a token to the list of processed tokens.
        """
        self.tokens.append((token_type.name, value, self.line))


# Example usage
text = ".5"
lexer = Lexico(text)
tokens = lexer.process()

for t in tokens:
    print(t)


# Em caso de erro, continuar do proximo caractere
# Token, lexema, linha
