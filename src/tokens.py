from typing import Optional
import enum

class TokenType(enum.Enum):
    """
    Class to maintain all valid tokens of language P.
    """

    # KEYWORD_MAIN      = "main"
    KEYWORD_READ      = "read"
    KEYWORD_PRINT     = "print"
    KEYWORD_RETURN    = "return"
    KEYWORD_PRINTLN   = "println"
    KEYWORD_FUNCTION  = "fn"
    KEYWORD_INT       = "int"
    KEYWORD_LET       = "let"
    KEYWORD_CHAR      = "char"
    KEYWORD_FLOAT     = "float"
    KEYWORD_IF        = "if"
    KEYWORD_ELSE      = "else"
    KEYWORD_WHILE     = "while"
    KEYWORD_FOR       = "for"

    PUNCTUATOR_LPAREN     = "("
    PUNCTUATOR_RPAREN     = ")"
    PUNCTUATOR_LBRACE     = "{"
    PUNCTUATOR_RBRACE     = "}"
    PUNCTUATOR_COMMA      = ","
    PUNCTUATOR_COLON      = ":"
    PUNCTUATOR_SEMICOLON  = ";"

    OPERATOR_LT        = "<"
    OPERATOR_LE        = "<="
    OPERATOR_GT        = ">"
    OPERATOR_GE        = ">="
    OPERATOR_PLUS      = "+"
    OPERATOR_MINUS     = "-"
    OPERATOR_MULTIPLY  = "*"
    OPERATOR_DIVIDE    = "/"
    OPERATOR_ASSIGN    = "="

    IDENTIFIER        = "ID"
    INT_CONSTANT      = "INT_CONST"
    FLOAT_CONSTANT    = "FLOAT_CONST"
    CHAR_LITERAL      = "CHAR_LITERAL"
    FORMATTED_STRING  = "FORMATTED_STRING"

    SYMBOL_ARROW  = "->" 
    SYMBOL_EQUAL  = "=="
    SYMBOL_DIFF   = "!=" 
    
    ERROR  = "ERROR" 

    def get_token(value: str) -> Optional[enum.Enum]:
        """
        Encontra o token com base no valor.

        Args:
            value (str): O valor do token.

        Returns:
            enum.Enum: O token, se encontrado, ou None caso contrário.
        """
        for token in TokenType:
            if value == token.value:
                return token
        
        return None