# Updated lexer.py with line number tracking for error handling

def tokenize(code):
    tokens = []
    lines = code.splitlines()

    for lineno, line in enumerate(lines, start=1):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if line.startswith("bata dost") or line.startswith("likh dost"):
            tokens.append(("PRINT", line.split("dost", 1)[1].strip(), lineno))


        elif line.startswith("bana dost"):
            var_part = line[9:].strip()
            if "=" in var_part:
                var_name, value = var_part.split("=", 1)
                tokens.append(("VAR_DECLARATION", var_name.strip(), value.strip(), lineno))
            else:
                tokens.append(("VAR_DECLARATION", var_part.strip(), None, lineno))

        elif line.startswith("kaam dost"):
            func_def = line[9:].strip()
            if "(" in func_def and ")" in func_def:
                func_name = func_def[:func_def.find("(")].strip()
                params_str = func_def[func_def.find("(")+1:func_def.find(")")].strip()
                params = [p.strip() for p in params_str.split(",") if p.strip()]
                tokens.append(("FUNC_DEF", func_name, params, lineno))
            else:
                tokens.append(("FUNC_DEF", func_def, [], lineno))

        elif line.startswith("bula dost"):
            func_call = line[9:].strip()
            if "(" in func_call and ")" in func_call:
                func_name = func_call[:func_call.find("(")].strip()
                args_str = func_call[func_call.find("(")+1:func_call.find(")")].strip()
                args = [arg.strip() for arg in args_str.split(",") if arg.strip()]
                tokens.append(("FUNC_CALL", func_name, args, lineno))
            else:
                tokens.append(("FUNC_CALL", func_call.replace("()", ""), [], lineno))

        elif line.startswith("wapas dost"):
            value = line[10:].strip()
            tokens.append(("RETURN", value if value else None, lineno))

        elif line.startswith("agar dost"):
            tokens.append(("IF", line[9:].strip(), lineno))

        elif line.startswith("nahi to dost"):
            tokens.append(("ELSE", None, lineno))

        elif line.startswith("jab tak dost"):
            tokens.append(("WHILE", line[12:].strip(), lineno))

        elif line.startswith("ghum dost"):
            parts = line[9:].strip().split()
            if len(parts) >= 5 and parts[1] == "se" and "tak" in parts:
                try:
                    tak_index = parts.index("tak")
                    var_name = parts[0]
                    start = parts[2]
                    end = parts[tak_index + 1]
                    step = parts[tak_index + 3] if len(parts) > tak_index + 3 else "1"
                    tokens.append(("FOR", var_name, start, end, step, lineno))
                except:
                    tokens.append(("UNKNOWN", line, lineno))

        elif line.startswith("bas dost"):
            tokens.append(("END", None, lineno))

        elif "=" in line and not line.startswith("bana dost"):
            var_name, value = line.split("=", 1)
            tokens.append(("ASSIGNMENT", var_name.strip(), value.strip(), lineno))


        else:
            tokens.append(("UNKNOWN", line, lineno))

    return tokens
