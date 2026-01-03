import re

def block(code):
    chrban = ['[', ']', '(', ')', '"', "'", '\\', '/', '?', '*']
    ban = [
        'import', 'compile', '__import__',
        'breakpoint', 'help', 'license', 'copyright', 'credits', '__subclasses__', 'load_module',
        'system', 'popen', 'subprocess', 'print', 'global', 'mro', '__class__', 'copy', 'sys', '__getattribute__', '+'
    ]

    if re.search(r'[bfhkqrvyzo0123456789BFHKQRVYZO]', code):
        return False, "\nnope!"
    
    if len(code) > 25:
        return False, "\nnope!"
    
    for char in chrban:
        if char in code:
            return False, "\nnope!"
    
    clow = code.lower()
    for keyword in ban:
        if keyword in clow:
            return False, "\nnope!"
    
    return True, "ok"

def run():
    lines = []
    while True:
        try:
            line = input()
            if line == "":
                break
            lines.append(line)
        except EOFError:
            break
    
    code = "\n".join(lines)
    
    if not code.strip():
        return
    
    valid, message = block(code)
    print(f"\n{message}\n")
    
    if not valid:
        return
    
    try:
        rg = {'__builtins__': __builtins__}
        exec(code, rg, {})
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
        return
    
if __name__ == "__main__":
    run()