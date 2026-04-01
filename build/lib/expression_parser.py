import re

# Token types
NUMBER, IDENTIFIER, OPERATOR, LPAREN, RPAREN, EOF = (
    'NUMBER', 'IDENTIFIER', 'OPERATOR', 'LPAREN', 'RPAREN', 'EOF'
)

# Token specification for basic expressions
token_specification = [
    ('STRING',   r'"[^"\n]*"'),               # Double-quoted string
    (NUMBER,     r'\d+(\.\d+)?'),             # Integer or decimal number
    (IDENTIFIER, r'[A-Za-z_]\w*'),            # Variable names
    (OPERATOR,   r'==|!=|<=|>=|[+\-*/%<>]'),   # Operators
    (LPAREN,     r'\('),                      # (
    (RPAREN,     r'\)'),                      # )
    ('SKIP',     r'[ \t]+'),                  # Whitespace
    ('MISMATCH', r'.'),                       # Unexpected characters
]

tok_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in token_specification)
get_token = re.compile(tok_regex).match

# Tokenizer
def tokenize_expr(expr):
    tokens = []
    pos = 0
    mo = get_token(expr)
    while mo:
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'STRING':
            tokens.append(('STRING', value[1:-1]))  # Strip quotes
        elif kind == NUMBER:
            value = float(value) if '.' in value else int(value)
            tokens.append((NUMBER, value))
        elif kind == IDENTIFIER:
            tokens.append((IDENTIFIER, value))
        elif kind == OPERATOR:
            tokens.append((OPERATOR, value))
        elif kind in (LPAREN, RPAREN):
            tokens.append((kind, value))
        elif kind == 'SKIP':
            pass
        elif kind == 'MISMATCH':
            raise SyntaxError(f"Unexpected character: {value}")
        pos = mo.end()
        mo = get_token(expr, pos)
    tokens.append((EOF, None))
    return tokens

# AST Nodes
class BinOp:
    def __init__(self, left, op, right): self.left, self.op, self.right = left, op, right
class Num:
    def __init__(self, value): self.value = value
class Var:
    def __init__(self, name): self.name = name
class Str:
    def __init__(self, value): self.value = value

# Recursive descent parser
class Parser:
    def __init__(self, tokens): self.tokens = tokens; self.pos = 0

    def current(self): return self.tokens[self.pos]
    def eat(self, kind):
        if self.current()[0] == kind:
            self.pos += 1
        else:
            raise SyntaxError(f"Expected {kind}, got {self.current()}")

    def parse(self):
        return self.comparison_expr()

    def comparison_expr(self):
        node = self.expr()
        while self.current()[0] == OPERATOR and self.current()[1] in ('==', '!=', '<', '<=', '>', '>='):
            op = self.current()[1]
            self.eat(OPERATOR)
            right = self.expr()
            node = BinOp(node, op, right)
        return node

    def expr(self):
        node = self.term()
        while self.current()[0] == OPERATOR and self.current()[1] in ('+', '-'):
            op = self.current()[1]
            self.eat(OPERATOR)
            node = BinOp(node, op, self.term())
        return node


    def term(self):
        node = self.factor()
        while self.current()[0] == OPERATOR and self.current()[1] in ('*', '/', '%'):
            op = self.current()[1]
            self.eat(OPERATOR)
            node = BinOp(node, op, self.factor())
        return node

    def factor(self):
        tok_type, tok_val = self.current()
        if tok_type == NUMBER:
            self.eat(NUMBER)
            return Num(tok_val)
        elif tok_type == IDENTIFIER:
            self.eat(IDENTIFIER)
            return Var(tok_val)
        elif tok_type == 'STRING':
            self.eat('STRING')
            return Str(tok_val)
        elif tok_type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            raise SyntaxError(f"Unexpected token: {self.current()}")

# Evaluator
def evaluate_ast(node, scope):
    if isinstance(node, Num):
        return node.value
    elif isinstance(node, Str):
        return node.value
    elif isinstance(node, Var):
        value = scope.get(node.name)
        # print(f"DEBUG: Variable lookup '{node.name}' = {value}") 
        if value is None:
            raise NameError(f"Variable '{node.name}' not defined")
        return value
    elif isinstance(node, BinOp):
        left = evaluate_ast(node.left, scope)
        right = evaluate_ast(node.right, scope)
        # print(f"DEBUG: BINOP -> {left} {node.op} {right}") # ✅ Add this
        return eval_binary(left, node.op, right)

def eval_binary(left, op, right):
    # print(f"DEBUG: Evaluating binary: {left} {op} {right}")
    if op == '+': return left + right
    elif op == '-': return left - right
    elif op == '*': return left * right
    elif op == '/': return left / right
    elif op == '%': return left % right
    elif op == '<': return left < right
    elif op == '>': return left > right
    elif op == '<=': return left <= right
    elif op == '>=': return left >= right
    elif op == '==': return left == right
    elif op == '!=': return left != right
    else: raise ValueError(f"Unknown operator: {op}")

# Entry point
def eval_expr(expr, scope):
    tokens = tokenize_expr(expr)
    parser = Parser(tokens)
    ast = parser.parse()
    return evaluate_ast(ast, scope)
