from lexer import tokenize
from diamond import execute_token, Scope

print("💎 Diamond Lang REPL")
print("Type `exit dost` to quit.\n")

repl_scope = Scope()

BLOCK_STARTERS = ("kaam dost", "agar dost", "warna dost", "jab tak dost", "ghum dost")

buffer = []
in_block = False

while True:
    try:
        prompt = "... " if in_block else ">>> "
        line = input(prompt).strip()

        if line == "exit dost":
            print("👋 Exiting Diamond Lang REPL.")
            break

        if not line:
            continue

        buffer.append(line)

        # Start of multi-line block
        if not in_block and any(line.startswith(kw) for kw in BLOCK_STARTERS):
            in_block = True
            continue

        # End of block
        if in_block and line == "bas dost":
            in_block = False

        # Only process when not in a block
        if in_block:
            continue

        code = "\n".join(buffer)
        tokens = tokenize(code)

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token[0] in ("FUNC_DEF", "IF", "WHILE", "FOR"):
                result = execute_token(token, tokens, i, scope=repl_scope)
                i = result if result is not None else i + 1
            else:
                execute_token(token, scope=repl_scope)
                i += 1

        buffer.clear()

    except KeyboardInterrupt:
        print("\n👋 Exiting Diamond Lang REPL.")
        break
    except Exception as e:
        print(f"❌ Error: {e}")
        buffer.clear()
        in_block = False
