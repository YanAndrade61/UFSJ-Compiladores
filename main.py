import os
import sys
from src.lexer import Lexer
from src.parser import Parser

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Erro: Arquivo não especificado.")
        print("Uso: python main.py <caminho_do_arquivo>")
        exit()

    file_name = sys.argv[1]

    try:
        with open(file_name, "r") as file:
            text = file.read()
    except FileNotFoundError:
        print("Erro: Arquivo não encontrado.")
        exit()

    with open('logs/error.log','w') as fp:
        pass

    tokens, error = Lexer(text).process()
    with open('logs/tokens.log','w') as fp:
        for t in tokens: 
            print(t, file=fp)
    
    print(f'Analise Lexica concluida: {error} erro(s) encontrado(s)')
    if(error):
        print('Corrija os erros para que a analise sintatica seja executada')
    else:
        Parser(tokens).parse()
    
    print('')
    print('Verifique os erros em logs/error.log')
    print('Verifique os tokens em logs/tokens.log')
    