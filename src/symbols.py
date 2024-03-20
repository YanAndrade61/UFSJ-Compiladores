import string

class Symbols:
    """
    Class to maintain all valid symbols of language P.
    """

    symbols = set()

    letters = list(string.ascii_uppercase + string.ascii_lowercase)
    symbols.update(letters)

    digits = list(string.digits)
    symbols.update(digits)

    operators = ['+','-','*','/','>','>=','<','<=','=','==','!=','->']
    symbols.update(operators)

    pontuaction = [',',';',':','(',')','{','}']
    symbols.update(pontuaction)

    extra = [' ', '\'', '"','_','.']
    symbols.update(extra)
