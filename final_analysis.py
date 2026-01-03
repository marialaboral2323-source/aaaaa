#!/usr/bin/env python3

# KEYWORDS DISPONIBLES:
# - and
# - as  
# - await
# - class
# - del
# - else
# - except
# - in
# - is
# - pass
#
# ESTO ES INTERESANTE!
# Tengo disponible: class, del, except, await, as, in, is
#
# DEL es interesante!
# del puede eliminar variables/atributos
# Pero ¿qué puedo hacer con del sin () [] o acceso útil?
#
# EXCEPT es interesante!
# Puedo usar try/except... pero try está prohibido (tiene 'r', 'y')
# WAIT: except está DISPONIBLE pero necesito try para usarlo
# Y try no está disponible
# Hmm...
#
# AWAIT está disponible!
# await se usa con coroutines async
# Pero necesito async que tiene 'y' prohibida
# Y await necesita un objeto awaitable
# No puedo crear uno sin def o () 
#
# AS está disponible!
# as se usa en:
# - import X as Y - pero import prohibido
# - with X as Y - pero with prohibido
# - except X as e - pero try prohibido
# No puedo usarlo solo
#
# IN e IS:
# Estos son operadores que puedo usar en expresiones
# - in: verifica membresía
# - is: verifica identidad
# Pero solo retornan True/False, no ejecutan código
#
# CLASS ya lo exploré
# PASS es solo un no-op
#
# AND podría ser útil para expresiones
# But again, solo evalúa, no ejecuta
#
# DEL ES LA MÁS INTERESANTE:
# del puede eliminar cosas del namespace
# Por ejemplo:
# del __name__
# del exec
# etc.
#
# ¿Qué pasa si elimino algo del __builtins__?
# del __builtins__.exec
#
# Pero:
# - __builtins__ tiene 'b' prohibida
# - Y esto solo elimina, no me ayuda a leer el flag
#
# WAIT WAIT WAIT:
# ¿Qué pasa con las ANNOTATIONS?
#
# En Python 3.6+, hay annotations:
# def func(x: int) -> str:
#     pass
#
# Pero necesito def que tiene 'f' prohibida
#
# PERO también hay annotations para variables:
# x: int = 5
#
# ¿Esto está permitido?
# La sintaxis es: name: annotation = value
# : no está prohibido!
#
# ¿Puedo hacer algo útil con annotations?
# Las annotations se evalúan en tiempo de definición
# Así que:
# x: exec = 1
#
# Esto evalúa 'exec' (que es la función builtin)
# y lo asigna a __annotations__['x']
#
# Pero esto solo obtiene la referencia a exec, no lo llama
#
# A menos que... la annotation sea una expresión compleja?
# x: func() = 1  # La annotation func() se EVALÚA!
#
# PERO necesito () para llamar la función en la annotation
#
# Hmm, no ayuda directamente...
#
# PERO WAIT:
# Las annotations pueden ser CUALQUIER expresión
# Y se evalúan en tiempo de definición
#
# ¿Hay alguna expresión que tenga efectos secundarios sin usar ()?
#
# Operadores:
# - a + b: llama a.__add__(b) pero necesito () implícito
# - a - b: llama a.__sub__(b)
# - a @ b: llama a.__matmul__(b)
# - etc.
#
# Si tuviera un objeto cuyo operador tenga efectos secundarios...
# Pero necesito crear tal objeto primero, lo que requiere def o ()
#
# ESTOY EN CÍRCULOS DE NUEVO
#
# ÚLTIMA IDEA: Revisar el problema desde otro ángulo completamente
#
# El servidor acepta conexiones en el puerto
# Cada conexión ejecuta app.py que:
# 1. Lee input() hasta línea vacía
# 2. Valida el código
# 3. Ejecuta con exec()
# 4. Captura excepciones y las muestra
#
# ¿Hay alguna vuln en este flujo?
#
# INPUT():
# input() en Python 3 es seguro, solo lee texto
# No hay inyección posible
#
# EXEC():
# exec() ejecuta código Python
# Si puedo bypassear el filtro, puedo ejecutar lo que quiera
#
# EXCEPTION HANDLING:
# Las excepciones se capturan y se muestra type(e).__name__ y e
# ¿Puedo crear una excepción custom que revele información?
# Necesitaría class y raise, pero raise tiene 'r' prohibida
#
# NAMESPACE:
# El exec se ejecuta con globals={'__builtins__': __builtins__}
# Así que solo __builtins__ está disponible
# ¿Hay alguna forma de explotar esto?
#
# __builtins__ contiene todas las funciones builtin
# Pero tiene 'b' prohibida, no puedo accederlo directamente
#
# WAIT: ¿Puedo acceder a __builtins__ sin escribir la palabra?
#
# Por ejemplo, usando globals() retorna el dict de globals
# Pero globals tiene 'o' y 'b' prohibidas
# Y necesitaría () para llamarlo
#
# ¿Hay alguna variable especial que apunte a __builtins__?
# - __name__: contiene el nombre del módulo
# - __spec__: contiene el spec del módulo (puede ser None)
# - ¿Hay otras?
#
# En el contexto de exec():
# Las únicas variables disponibles son las que están en globals
# que es {'__builtins__': __builtins__}
#
# Así que no hay otras variables especiales accesibles
#
# A MENOS QUE...
#
# ¿Qué pasa si el código de validación tiene un BUG LÓGICO?
#
# Revisemos una vez más:

print('REVISIÓN FINAL DEL FILTRO:')
print('=' * 60)

code_filter = '''
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

print(code_filter)
print('=' * 60)

# ANALIZANDO CADA VALIDACIÓN:
print('\nANÁLISIS:')
print('1. Regex de letras/números prohibidos: Simple, no hay bypass')
print('2. Length > 25: Simple, no hay bypass')  
print('3. Caracteres prohibidos in code: Simple, no hay bypass')
print('4. Keywords prohibidas in code.lower(): Substring search')
print()
print('Para #4:')
print('  - Busca substring en lowercase')
print('  - No busca palabras completas')
print('  - Si escribo "printing", se detecta porque contiene "print"')
print('  - ¿Hay algún bypass?')
print()
print('  IDEA: ¿Qué pasa si uso caracteres Unicode que se normalizan?')
print('  Por ejemplo, algunos caracteres Unicode se ven como letras ASCII')
print('  pero son diferentes codepoints')
print()
print('  Ejemplos de caracteres confusables:')
print('    - ᵖ (U+1D56) - superscript p')
print('    - ʳ (U+02B3) - modifier letter r')
print('    - ⁱ (U+2071) - superscript i')
print('    - ⁿ (U+207F) - superscript n')
print('    - ᵗ (U+1D57) - superscript t')
print()
print('  Si uso estos para escribir "print" como "ᵖʳⁱⁿᵗ"')
print('  el filtro busca en code.lower() que es "ᵖʳⁱⁿᵗ".lower()')
print('  ¿Estos caracteres tienen lowercase diferentes?')
print()

# Probar caracteres Unicode
test_unicode = 'ᵖʳⁱⁿᵗ'
print(f'  Original: {test_unicode}')
print(f'  Lowercase: {test_unicode.lower()}')
print(f'  ¿Contiene "print"?: {"print" in test_unicode.lower()}')
print()

# Pero el problema es: ¿Python acepta estos como identificadores?
print('  PERO: Python solo acepta ciertos Unicode en identificadores')
print('  Los superscripts probablemente no sean válidos')
print()

# Verificar si Python acepta el identificador
import sys
try:
    compile('ᵖʳⁱⁿᵗ', '<string>', 'eval')
    print('  Python acepta: SÍ')
except SyntaxError:
    print('  Python acepta: NO (SyntaxError)')
