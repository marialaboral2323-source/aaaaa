#!/usr/bin/env python3
# coding: utf-8

# ÚLTIMA ESTRATEGIA: Edge cases y trucos muy oscuros
#
# Voy a intentar payloads que exploten cualquier comportamiento inesperado:
# 1. Comentarios que bypasseen validación
# 2. Encoding tricks
# 3. Null bytes
# 4. Unicode tricks más avanzados
# 5. Python parser quirks
#
# Pero primero, voy a RELEER el código del filtro MUY CUIDADOSAMENTE
# una vez más para ver si hay ALGÚN bug

filter_code = '''
def block(code):
    chrban = ['[', ']', '(', ')', '"', "'", '\\\\', '/', '?', '*']
    ban = [
        'import', 'compile', '__import__',
        'breakpoint', 'help', 'license', 'copyright', 'credits', '__subclasses__', 'load_module',
        'system', 'popen', 'subprocess', 'print', 'global', 'mro', '__class__', 'copy', 'sys', '__getattribute__', '+'
    ]
    
    if re.search(r'[bfhkqrvyzo0123456789BFHKQRVYZO]', code):
        return False, "\\nnope!"
    
    if len(code) > 25:
        return False, "\\nnope!"
    
    for char in chrban:
        if char in code:
            return False, "\\nnope!"
    
    clow = code.lower()
    for keyword in ban:
        if keyword in clow:
            return False, "\\nnope!"
    
    return True, "ok"
'''

print("ANÁLISIS DETALLADO DEL FILTRO:")
print("=" * 70)
print(filter_code)
print("=" * 70)
print()

# ANÁLISIS PASO POR PASO:
print("1. Regex check: re.search(r'[bfhkqrvyzo0123456789BFHKQRVYZO]', code)")
print("   - Busca CUALQUIER ocurrencia de estas letras/números")
print("   - En CUALQUIER parte del string")
print("   - Case-sensitive (b y B son ambos detectados)")
print("   - NO hay bypass con Unicode porque busca codepoints específicos")
print()

print("2. Length check: len(code) > 25")
print("   - El código COMPLETO (con \\n incluidos) debe ser <= 25 chars")
print("   - Simple y directo")
print("   - NO hay bypass")
print()

print("3. Char ban check: for char in chrban: if char in code")
print("   - Busca cada carácter prohibido en el string")
print("   - chrban = ['[', ']', '(', ')', '\"', \"'\", '\\\\', '/', '?', '*']")
print("   - Simple string search")
print("   - NO hay bypass con Unicode porque busca caracteres específicos")
print()

print("4. Keyword ban check: for keyword in ban: if keyword in clow")
print("   - clow = code.lower() - convierte a minúsculas")
print("   - Busca substring, no palabra completa")
print("   - Ejemplo: 'print' detecta 'printing', 'printf', etc.")
print("   - ¿HAY BYPASS?")
print()

# ANÁLISIS DEL KEYWORD CHECK MÁS PROFUNDO
print("ANÁLISIS PROFUNDO DEL KEYWORD CHECK:")
print("-" * 70)
print("clow = code.lower()")
print("for keyword in ban:")
print("    if keyword in clow:")
print("        return False")
print()
print("PREGUNTA: ¿Qué hace str.lower() con caracteres Unicode?")
print()

# Probar lowercase con Unicode
test_cases = [
    ('ᵖʳⁱⁿᵗ', 'superscript letters'),
    ('PRINT', 'uppercase ASCII'),
    ('Print', 'mixed case'),
    ('ｐｒｉｎｔ', 'fullwidth'),
    ('ｐʳⁱⁿᵗ', 'mixed fullwidth and superscript'),
]

print("Testing str.lower() behavior:")
for text, desc in test_cases:
    lower = text.lower()
    contains = 'print' in lower
    print(f"  {text:15s} ({desc:30s})")
    print(f"    .lower() = {lower:15s}")
    print(f"    contains 'print': {contains}")
    print()

# CRUCIAL: Si lowercase de caracteres Unicode no produce 'print' ASCII,
# entonces puedo bypassear el filtro de keywords!

print("=" * 70)
print("CONCLUSIÓN CLAVE:")
print("Si los caracteres Unicode NO se convierten a ASCII con .lower(),")
print("entonces puedo bypassear el filtro de keywords!")
print("=" * 70)
