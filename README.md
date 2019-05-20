# LFA-Parser
Implementação de um parser descendente recursivo para uma Linguagem Livre de Contexto, chamada de MEL.

### Informações gerais
- **Autor**: Lucas Gomes Flegler
- **Linguagem de programação**: Python (versão 3.6.5)
- **Ambiente de desenvolvimento**: Visual Studio Code (versão 1.33.1)

### Descrição geral do código fonte
O código fonte está estruturado da seguinte maneira:

```
src
|_ main.py
|_ mel.py
|_ trab1.sh
|_ testes
   |_ testes.txt
```


#### mel.py
É um módulo que contém uma classe única chamada `MEL`, que tem por responsabilidade manipular as expressões matemáticas e encontrar o seu resultado.

```python
class MEL():
    def __init__(self, tokens):
        self._tokens = tokens
        self._current = tokens[0]
        self._operator = ''
    
    def mount_expression(self, lst):
        tokens = []
        numbers, operators = '', ''

        for i in range(len(lst)):
            # concatenando numeros seguidos por numeros, numeros com '.' e numeros com 'e'
            if (self.digit(lst[i]) or lst[i] == '.' or lst[i] == 'e' or lst[i] == 'E'):
                numbers += lst[i]
                if operators != '':
                    tokens.append(operators)
                    operators = ''
            else:
                # se ja existe um operador '/'
                if operators != '':
                    # caso a expressao tenha '//', ambos ficam na mesma posicao da lista
                    if (operators is '/' and lst[i] is '/'):
                        operators += lst[i]
                    else:
                        tokens.append(operators)
                        tokens.append(lst[i])
                        operators = ''
                else:
                    operators += lst[i]
                if numbers != '':
                    tokens.append(numbers)
                    numbers = ''

        # caso só exista somente numeros como entrada
        if (numbers != '' and operators == ''):
            tokens.append(numbers)
        return tokens
    
    def parser(self,lst):
        tokens = []
        # caso a expressao nao seja aceita
        try:
            tokens = self.mount_expression(lst)
            print(MEL(tokens).exp())
        except:
            print("expressao invalida")

```
O trecho de código mostrado acima representa o construtor da classe. O construtor contém o "token", que é responsável por armazenar a expressão inserida, o "current" que armazena a posição atual da expressão a ser processada e o operador que verifica se a expressão é negativa ou positiva.

O mesmo trecho citado acima também mostra o método chamado `parser`, que tem por responsabilidade ser um intermediário entre a montagem da expressão e a chamada da mesma.
O método `parser` depois de executado, chamará os demais métodos da classe, seguindo as regras de produção definidas para a gramática que é mostrada logo abaixo.

```html
<expr>   ::= <term> ((‘+’ | ‘-’) <term>)*
<term>   ::= <factor> ((‘*’ | ‘/’ | ‘//’ | ‘%’) <factor>)*
<factor> ::= <base> (‘^’ <factor>)?
<base>   ::= (‘-’) <base>
           |  ‘(’ <expr> ‘)’
<digit>  ::= ‘0’ | ‘1’ | ‘2’ | ‘3’ | ‘4’ | ‘5’ | ‘6’ | ‘7’ | ‘8’ | ‘9’
```

#### main.py
É o módulo principal do programa, que tem como objetivo lê a expressão digitada pelo usuário e passar a informação lida para o método `parser`. Depois de receber a expressão, o método `replace` remove todos os espaços em branco e salva em uma lista utilizando o método `list`. Veja o trecho a seguir:

```python
from mel import MEL

try:
    input = raw_input
except NameError:
    pass

def main():
    while True:
        # ignorando espacos
        lst = list(input('> ').replace(' ', ''))
        if len(lst) == 0:
            print("Favor inserir uma expressao")
        else:
            MEL(lst).parser(lst)

if __name__ == '__main__':
    main()
```
Caso a entrada seja vazia, é emitido uma mensagem no console para que tenha pelo menos uma  expressão inserida.

### Como executar?
Para executar o programa no ambiente Linux, basta abrir o CLI(Command Line Interface) no diretório __`/src`__ e digitar o seguinte comando:

```shell
    python3 main.py
```

Dentro dessa mesma pasta(`/src`) existe um script básico para execução do programa. O comando abaixo mostra como executar.

```shell
    ./trab1.sh
```

### Testes
Para testes, foi criado um arquivo de testes chamado `testes.txt`, que fica dentro do diretório `/src/testes`. Esse arquivo contém algumas expressões que foram usadas para teste da gramática. Dentre eles, temos:
```txt
((2+2)*2)-((2-0)+2)
Resposta: 4.0
(10*5)+(100/10)-5+(7%(2^2))
Resposta:58.0
10 * 5 + 100 / 10 - 5 + 7 % 2
Resposta: 56.0
(-2.3)^2 + 2.2E1 * 2e1-12 + 1e1+3
Resposta:446.29
(-2.3)^2 + 2.2E1 * 2e1-12 + (1e1+3) % 2
Resposta: 434.29
2e5 + 3
Resposta: 200003.0
...
```

### Informações adicionais
Todo o código fonte está hospedado no [GitHub](https://github.com/lukasg18/LFA-PARSER).

