# Simulador de Compilador

Este programa simula um compilador básico, implementando as duas primeiras partes: o analisador léxico e o analisador sintático.

## Uso

Para executar o programa, utilize o seguinte comando no terminal:

```
python main.py <caminho_do_arquivo>
```

Substitua `<caminho_do_arquivo>` pelo caminho do arquivo que deseja compilar.

## Funcionamento

O programa consiste em três partes principais:

1. **Analisador Léxico**: Responsável por analisar o texto de entrada e dividí-lo em tokens.

2. **Analisador Sintático**: Utiliza os tokens gerados pelo analisador léxico para verificar se a estrutura do programa está correta de acordo com a gramática definida.

## Arquivos de Log

O programa gera dois arquivos de log:

- **tokens.log**: Contém os tokens identificados pelo analisador léxico.
- **error.log**: Registra quaisquer erros encontrados durante a análise léxica ou sintática.

## Exemplo

```python
python main.py exemplo.txt
```

## Exemplo de Arquivo de Entrada

```plaintext
# exemplo.txt

fn main(){ 
    let i: int;
    i = 0;
    while i < 10 {
        println("{}", i);
        i = i + 1;
    }
}
```