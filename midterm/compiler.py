import re

# Token Types
NUMBER, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, IDENT, ASSIGN, PRINT, EOF = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
    'IDENT', 'ASSIGN', 'PRINT', 'EOF'
)

# Lexer
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'{self.type}:{self.value}'

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
    
    def next_token(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

        if self.pos >= len(self.text):
            return Token(EOF)

        char = self.text[self.pos]

        if char.isdigit():
            start = self.pos
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1
            return Token(NUMBER, int(self.text[start:self.pos]))

        if char.isalpha():
            start = self.pos
            while self.pos < len(self.text) and self.text[self.pos].isalnum():
                self.pos += 1
            word = self.text[start:self.pos]
            if word == 'print':
                return Token(PRINT)
            return Token(IDENT, word)

        self.pos += 1
        if char == '+': return Token(PLUS)
        if char == '-': return Token(MINUS)
        if char == '*': return Token(TIMES)
        if char == '/': return Token(DIVIDE)
        if char == '(': return Token(LPAREN)
        if char == ')': return Token(RPAREN)
        if char == '=': return Token(ASSIGN)

        raise Exception(f"Unknown character: {char}")

# AST Nodes
class Number: pass
class BinOp: pass
class Assign: pass
class Print: pass
class Var: pass

# Parser
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token = self.lexer.next_token()

    def eat(self, token_type):
        if self.token.type == token_type:
            self.token = self.lexer.next_token()
        else:
            raise Exception(f"Expected {token_type}, got {self.token.type}")

    def factor(self):
        if self.token.type == NUMBER:
            val = self.token.value
            self.eat(NUMBER)
            return ('number', val)
        elif self.token.type == IDENT:
            name = self.token.value
            self.eat(IDENT)
            return ('var', name)
        elif self.token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node

    def term(self):
        node = self.factor()
        while self.token.type in (TIMES, DIVIDE):
            op = self.token.type
            self.eat(op)
            node = ('binop', op, node, self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.token.type in (PLUS, MINUS):
            op = self.token.type
            self.eat(op)
            node = ('binop', op, node, self.term())
        return node

    def statement(self):
        if self.token.type == IDENT:
            varname = self.token.value
            self.eat(IDENT)
            self.eat(ASSIGN)
            expr = self.expr()
            return ('assign', varname, expr)
        elif self.token.type == PRINT:
            self.eat(PRINT)
            expr = self.expr()
            return ('print', expr)

    def parse(self):
        statements = []
        while self.token.type != EOF:
            statements.append(self.statement())
        return statements

# Code Generator
class CodeGen:
    def __init__(self):
        self.bytecode = []
        self.vars = {}

    def gen(self, node):
        nodetype = node[0]
        if nodetype == 'number':
            self.bytecode.append(('PUSH', node[1]))
        elif nodetype == 'var':
            self.bytecode.append(('LOAD', node[1]))
        elif nodetype == 'binop':
            _, op, left, right = node
            self.gen(left)
            self.gen(right)
            ops = {'PLUS': 'ADD', 'MINUS': 'SUB', 'TIMES': 'MUL', 'DIVIDE': 'DIV'}
            self.bytecode.append((ops[op],))
        elif nodetype == 'assign':
            _, name, expr = node
            self.gen(expr)
            self.bytecode.append(('STORE', name))
        elif nodetype == 'print':
            self.gen(node[1])
            self.bytecode.append(('PRINT',))

# Virtual Machine
class VM:
    def __init__(self, bytecode):
        self.bytecode = bytecode
        self.stack = []
        self.vars = {}

    def run(self):
        for instr in self.bytecode:
            op = instr[0]
            if op == 'PUSH':
                self.stack.append(instr[1])
            elif op == 'LOAD':
                self.stack.append(self.vars[instr[1]])
            elif op == 'STORE':
                val = self.stack.pop()
                self.vars[instr[1]] = val
            elif op == 'ADD':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a + b)
            elif op == 'SUB':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a - b)
            elif op == 'MUL':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a * b)
            elif op == 'DIV':
                b, a = self.stack.pop(), self.stack.pop()
                self.stack.append(a // b)
            elif op == 'PRINT':
                print(self.stack.pop())

# Run Compiler
def run_compiler(source):
    lexer = Lexer(source)
    parser = Parser(lexer)
    ast = parser.parse()

    codegen = CodeGen()
    for stmt in ast:
        codegen.gen(stmt)

    vm = VM(codegen.bytecode)
    vm.run()

# Example input
program = """
x = 3 + 4 * 2
y = x - 5
print y
"""

run_compiler(program)
