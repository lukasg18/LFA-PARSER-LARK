"""
expr ::= term (('+' | '-') term)*
term ::= factor (('*' | '/' | '//' | '%') factor)*
factor ::= base ('^' factor)?
base ::= (-) base | '(' expr ')'
digit ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
"""

from operator import floordiv, mod

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

    def next(self): 
        #pula o primeiro elemento, pois ele ja foi processado
        self._tokens = self._tokens[1:] 
        if len(self._tokens) > 0:
            # coloca o proximo elemento a ser processado
            self._current = self._tokens[0]

    def exp(self):
        result = self.term()
        while self._current in ('+', '-'):
            if self._current == '+':
                self.next()
                result += self.term()
            if self._current == '-':
                self.next()
                result -= self.term()
        return result


    def term(self):
        result = self.factor()
        while self._current in ('*', '/', '%', '//'):
            if self._current == '*':
                self.next()
                result *= self.term()
            if self._current == '/':
                self.next()
                result /= self.term()
            if self._current == '//':
                self.next()
                result //= self.term()
            if self._current == '%':
                self.next()
                result %= self.term()
        return result

    def factor(self):
        result = self.base()
        while self._current in ('^'):
            if self._current == '^':
                self.next()
                result **= self.term()
        return result

    def base(self):
        result = None
        if self.digit(self._current[0]):
            # negando o numero: (-) base
            if(self._operator is '-'):
                result = float(self._current) * float(-1.0)
                self._operator = ''
            else:
                result = float(self._current)
                self.next()
        elif self._current is '(':
            # caso a expressao for negagativa: (-) expr
            if(self._operator is '-'):                
                self._operator = ''
                self.next()
                result = self.exp()
                result *= (-1)
                self.next()
            else: 
                self.next()
                result = self.exp()
                self.next()
        else:
            # caso o numero inserido for negativo
            if self._current is '-':
                self._operator = '-'
                self.next()
                result = self.base()
                self.next()
        return result

    def digit(self, current):
        digits = ['0','1','2','3','4','5','6','7','8','9']
        if current in digits:
            return True
        else:
            return False
