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

    with open('./logs/error.log','w') as fp:
        pass

    tokens, error = Lexer(text).process()
    with open('./logs/tokens.log','w') as fp:
        for t in tokens: 
            print(t, file=fp)
    
    print(f'Analise Lexica concluida: {error} erro(s) encontrado(s)')
    if(error):
        print('Corrija os erros para que a analise sintatica seja executada')
    else:
        parser = Parser(tokens)
        parser.parse()
        
        with open('./logs/symbol_tables.log','w') as fp:
            for name,table in parser.table_symbols.items():
                print(f'Tabela de simbolos da funcao {name}:', file=fp)
                print(table, file=fp)

        with open('./logs/ast.log','w') as fp:
            for ast in parser.trees:
                print(str(ast), file=fp)
                ast.verify_type()  
        
    print('')
    print('Verifique os erros em logs/error.log')
    print('Verifique os tokens em logs/tokens.log')
    print('Verifique as tabelas de simbolo em logs/symbol_tables.log')
    print('Verifique os arvores de sintaxe abstrata em logs/ast.log')
    