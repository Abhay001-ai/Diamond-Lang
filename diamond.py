from lexer import tokenize
from expression_parser import eval_expr
import sys

functions = {}
loop_context = {
    'break': False,
    'continue': False,
    'return_value': None
}

class Scope:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent
        self.return_value = None

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        return globals().get(name)

    def set(self, name, value):
        if name in self.variables:
            # print(f"DEBUG: Updating variable '{name}' to {value}")
            self.variables[name] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            # print(f"DEBUG: Creating variable '{name}' = {value}")
            self.variables[name] = value



def evaluate_expression(expr, scope, lineno=None):
    if scope is None:
        raise RuntimeError("Scope was not provided to evaluate_expression")

    if isinstance(expr, str):
        if expr.startswith("bula dost"):
            func_name = expr[9:expr.find("(")].strip()
            args_str = expr[expr.find("(")+1:expr.find(")")].strip()
            args = [arg.strip() for arg in args_str.split(",")] if args_str else []
            return execute_token(("FUNC_CALL", func_name, args, lineno), scope=scope)

        try:
            return eval_expr(expr, scope)
        except Exception as e:
            print(f"Line {lineno if lineno else '?'}: Expression Error: {e} => '{expr}'")
            return None

    return expr

def execute_token(token, tokens=None, index=None, scope=None):
    if scope is None:
        raise RuntimeError("Scope was not provided to execute_token")

    try:
        type_ = token[0]
        args = token[1:-1] if len(token) > 2 else token[1:]
        lineno = token[-1] if len(token) > 2 else None

        if type_ == "PRINT":
            value = evaluate_expression(args[0], scope, lineno)
            print(value)

        elif type_ == "VAR_DECLARATION":
            var_name = args[0]
            value = evaluate_expression(args[1], scope, lineno) if args[1] is not None else None
            scope.set(var_name, value)

        elif type_ == "ASSIGNMENT":
            var_name = args[0]
            value = evaluate_expression(args[1], scope, lineno)
            scope.set(var_name, value)


        elif type_ == "FUNC_DEF":
            if tokens and index is not None:
                func_name, params = args
                body = []
                i = index + 1
                while i < len(tokens) and tokens[i][0] != "END":
                    body.append(tokens[i])
                    i += 1
                functions[func_name] = (params, body)
                return i + 1

        elif type_ == "FUNC_CALL":
            func_name, call_args = args
            if func_name not in functions:
                raise Exception(f"Function '{func_name}' is not defined.")
            params, body = functions[func_name]
            old_scope = scope
            new_scope = Scope(old_scope)
            scope = new_scope

            for param, arg in zip(params, call_args):
                value = evaluate_expression(arg, old_scope, lineno)
                scope.set(param, value)

            for t in body:
                result = execute_token(t, scope=scope)
                if scope.return_value is not None:
                    break

            result = scope.return_value
            scope = old_scope
            return result

        elif type_ == "RETURN":
            value = evaluate_expression(args[0], scope, lineno) if args[0] else None
            scope.return_value = value
            return value

        elif type_ == "IF":
            condition = evaluate_expression(args[0], scope, lineno)
            i = index + 1

            if condition:
                # Execute IF block
                while i < len(tokens) and tokens[i][0] not in ("ELSE", "END"):
                    execute_token(tokens[i], scope=scope)
                    i += 1

                # Skip ELSE block if it exists
                while i < len(tokens) and tokens[i][0] != "END":
                    i += 1

            else:
                # Skip to ELSE
                while i < len(tokens) and tokens[i][0] != "ELSE":
                    i += 1
                i += 1  # Move past 'ELSE'

                # Execute ELSE block
                while i < len(tokens) and tokens[i][0] != "END":
                    execute_token(tokens[i], scope=scope)
                    i += 1

            return i


        elif type_ == "WHILE":
            i = index + 1
            body = []

            while i < len(tokens) and tokens[i][0] != "END":
                body.append(tokens[i])
                i += 1

            # Prevent infinite loop crash (optional)
            loop_guard = 0
            while evaluate_expression(args[0], scope, lineno):
                loop_guard += 1
                if loop_guard > 1000:
                    print("⚠️ Infinite loop protection triggered")
                    break

                for t in body:
                    execute_token(t, scope=scope)

            return i  # index after END


        elif type_ == "FOR":
            var, start_expr, end_expr, step_expr = args
            start_val = int(evaluate_expression(start_expr, scope, lineno))
            end_val = int(evaluate_expression(end_expr, scope, lineno))
            step_val = int(evaluate_expression(step_expr, scope, lineno))
            i = index + 1
            block_start = i
            while i < len(tokens) and tokens[i][0] != "END":
                i += 1
            block_end = i
            for v in range(start_val, end_val + 1, step_val):
                scope.set(var, v)
                j = block_start
                while j < block_end:
                    execute_token(tokens[j], scope=scope)
                    j += 1
            return block_end

        elif type_ == "END":
            return index

    except Exception as e:
        print(f"Line {lineno if lineno else '?'}: Execution Error at token {token}: {e}")
        return index + 1

def run(file_path):
    scope = Scope()

    with open(file_path, "r") as f:
        code = f.read()

    tokens = tokenize(code)
    i = 0
    while i < len(tokens):
        if tokens[i][0] in ("FUNC_DEF", "IF", "WHILE", "FOR"):
            result = execute_token(tokens[i], tokens, i, scope=scope)
            i = result if result is not None else i + 1
        else:
            execute_token(tokens[i], scope=scope)
            i += 1

def main():
    if len(sys.argv) != 2:
        print("Usage: diamond <file.diamond>")
        sys.exit(1)
    file_path = sys.argv[1]
    run(file_path)

if __name__ == "__main__":
    main()
