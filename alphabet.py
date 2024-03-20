import string

class Alphabet:

    symbols = set()

    # Letras maiúsculas e minúsculas
    letters = list(string.ascii_uppercase + string.ascii_lowercase)
    symbols.update(letters)

    # Números
    digits = list(string.digits)
    symbols.update(digits)

    # Operadores
    operators = ['+','-','*','/','>','>=','<','<=','=','==','!=']
    symbols.update(operators)

    # Sinais de pontuação
    pontuaction = [',',';',':','(',')','{','}']
    symbols.update(pontuaction)

    # Outros
    extra = [' ', '\'', '"','_','.']
    symbols.update(extra)

    def __contains__(self, symbol: str) -> bool:
        """
        Verifica se um símbolo está presente no alfabeto.

        Args:
            symbol (str): O símbolo a ser verificado.

        Returns:
            bool: True se o símbolo estiver presente, False caso contrário.
        """
        return symbol in self.symbols

