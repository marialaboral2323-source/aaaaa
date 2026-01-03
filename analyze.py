#!/usr/bin/env python3

# Análisis del PyJail:
# 
# RESTRICCIONES:
# 1. Caracteres prohibidos: [ ] ( ) " ' \ / ? *
# 2. Palabras prohibidas: import, compile, __import__, breakpoint, help, license, copyright, 
#    credits, __subclasses__, load_module, system, popen, subprocess, print, global, mro, 
#    __class__, copy, sys, __getattribute__, +
# 3. Dígitos/letras prohibidas: b f h k q r v y z o 0-9 B F H K Q R V Y Z O
# 4. Longitud máxima: 25 caracteres
# 5. Se ejecuta con exec(code, {'__builtins__': __builtins__}, {})
#
# LETRAS PERMITIDAS: a c d e g i j l m n p s t u w x A C D E G I J L M N P S T U W X
# OPERADORES DISPONIBLES: - , . ; : = < > ! & | ~ ^ % @ $ #
#
# OBJETIVO: Leer /app/flag.txt
#
# ESTRATEGIA:
# - No podemos usar print() directamente (prohibido)
# - No podemos usar paréntesis ni corchetes
# - No podemos usar import
# - Necesitamos encontrar una forma alternativa de ejecutar código
# 
# IDEAS:
# 1. Usar exec sin paréntesis es imposible
# 2. Usar __builtins__ para acceder a funciones
# 3. Necesitamos una forma de llamar funciones sin ()
# 4. Decoradores? @
# 5. Walrus operator := (disponible en Python 3.8+)
# 6. Generar números sin dígitos: True=1, True+True=2, etc.
# 7. Usar eval, exec indirectamente
# 8. Usar operador @ (matmul) si sobrecargamos
#
# DESAFÍO: Sin paréntesis, sin corchetes, sin números, sin muchas letras clave
#
# Podemos usar:
# - Asignaciones: a = algo
# - Operadores: @ - * / % etc
# - Punto: objeto.atributo
# - Sin llamadas a función obvias
#
# IDEA CLAVE: Python permite decoradores sin paréntesis si no tienen args
# @decorator
# def func(): pass
#
# Pero necesitamos 25 chars max y sin 'def'
#
# OTRA IDEA: Usar walrus := en expresiones
# Pero necesitamos evaluar algo
#
# BREAKTHROUGH: 
# - Podemos usar __import__ ? NO, está en ban
# - Podemos usar eval? eval no está prohibido!
# - Pero necesitamos paréntesis para llamar eval()
#
# WAIT: Mirando más de cerca...
# getattr() no está prohibido
# pero necesitamos () para llamarlo
#
# SIN PARÉNTESIS es casi imposible ejecutar funciones en Python
# A menos que... usemos decoradores o __call__ implícito
#
# Python permite:
# objeto.__dict__ sin ()
# objeto.__class__ sin () - PERO __class__ está prohibido
#
# Necesito pensar en formas alternativas...
# 
# IDEA: Usar ; para ejecutar múltiples statements
# a=__builtins__;b=a.eval  # Pero necesitamos () para llamar
#
# MOMENTO: Si usamos decoradores:
# @eval
# 
# Pero eval está en __builtins__ y necesitamos accederlo
#
# Tal vez podamos usar:
# exec`código`  # No, esto es sintaxis vieja de Python 2
#
# REFLEXIÓN: Este es un pyjail MUY restrictivo
# Sin (), sin [], sin números, sin muchas letras...
#
# Veamos si podemos usar otros trucos:
# - chr() para generar caracteres - NO, necesitamos () y 'chr' tiene 'h' y 'r' prohibidas
# - getattr() - necesitamos ()
# - setattr() - necesitamos ()
#
# IDEA NUEVA: ¿Qué pasa si tratamos de causar un error que revele información?
# Podemos usar: dir, len, id, etc. (si no tienen letras prohibidas)
# 
# dir - tiene 'd' 'i' disponibles pero 'r' prohibida
# len - tiene 'l' 'e' 'n' disponibles!
# id - tiene 'i' 'd' disponibles!
#
# Pero sin () no podemos llamarlos
#
# ÚLTIMO RECURSO: Tal vez el reto requiere encontrar una vulnerabilidad en el filtro
# O usar caracteres Unicode que parecen () pero no lo son
# O usar encoding tricks
#
# Revisando el código del filtro más cuidadosamente:
# - La regex busca [bfhkqrvyzo0123456789BFHKQRVYZO] en el código
# - Busca caracteres en chrban en el código
# - Busca palabras en ban en code.lower()
#
# ¿Hay alguna forma de bypassear esto?
# 
# UNICODE BYPASS:
# - Usar caracteres Unicode que se vean como () pero sean diferentes
# - Python acepta ciertos caracteres Unicode en código
# - Ejemplos: 
#   - \u0028 = (
#   - \u0029 = )
#   - Pero si los ponemos literalmente en el código, el filtro los detecta
# - Si usamos la secuencia de escape... necesitamos \ que está prohibida
#
# ENCODING:
# - ¿Podemos enviar el código en otro encoding que cuando se procese se convierta en lo que queremos?
# - Python lee el input como UTF-8 por defecto
# - Pero input() decodifica automáticamente
#
# IDEA: Multiline con diferentes payloads
# El código acepta múltiples líneas hasta encontrar una línea vacía
# Luego valida TODO el código junto
# Así que no podemos bypassear línea por línea
#
# ESTRATEGIA ALTERNATIVA:
# Tal vez el objetivo no es ejecutar código Python arbitrario
# sino explotar algo en la lógica del filtro o del exec mismo
#
# Revisando exec():
# exec(code, globals, locals)
# globals = {'__builtins__': __builtins__}
# locals = {}
#
# El __builtins__ está disponible, así que tenemos acceso a funciones builtin
# Pero sin () no podemos llamarlas...
#
# WAIT: ¿Y si usamos assignment con efectos secundarios?
# En Python 3.8+, el walrus operator := puede tener efectos secundarios
# Pero aún necesitamos ejecutar algo
#
# IDEA CRÍTICA:
# ¿Hay alguna forma en Python de ejecutar código sin usar ()?
#
# Opciones:
# 1. Decoradores - requieren def que tiene 'd' 'e' pero 'f' está prohibida
# 2. Operador @ sobrecargado - requiere clase que tiene letters prohibidas
# 3. Metaclasses - muy complejo y usa muchas features prohibidas
# 4. Properties - requieren @property que tiene letras prohibidas
# 5. Descriptores - requieren __get__ etc con letras prohibidas
#
# MOMENTO EUREKA:
# ¿Y si el bypass es más simple? ¿Qué pasa si simplemente necesitamos leer variables?
# 
# El exec() se ejecuta con __builtins__ disponible
# Después del exec, ¿podemos inspeccionar el namespace?
# 
# NO, porque el código se ejecuta en un try/except y luego la función termina
#
# PENSANDO MÁS PROFUNDO:
# Sin paréntesis, la única forma de ejecutar código es:
# - Asignaciones que tienen efectos secundarios
# - Operadores que tienen efectos secundarios
#
# En Python, ¿qué asignaciones u operadores tienen efectos secundarios visibles?
#
# IDEA: ¿Y si creamos una excepción que revele información?
# Por ejemplo, dividir por cero, acceder a atributo inexistente, etc.
# El código captura excepciones y las imprime
#
# Podríamos hacer:
# - a.nonexistent - causaría AttributeError mostrando el tipo de 'a'
# - Pero esto no nos ayuda a leer el flag
#
# REFLEXIÓN PROFUNDA:
# Este pyjail es EXTREMADAMENTE restrictivo
# Tal vez el enfoque es diferente...
#
# ¿Qué pasa si hay una vulnerabilidad en el código del filtro mismo?
# Veamos la regex: r'[bfhkqrvyzo0123456789BFHKQRVYZO]'
# Esta busca esos caracteres específicos
# ¿Hay algún bypass Unicode o encoding?
#
# En Python, los identificadores pueden usar ciertos caracteres Unicode
# Por ejemplo, letras acentuadas, letras griegas, etc.
# ¿Podemos usar un carácter Unicode que se normalice a uno permitido?
#
# IDEA: Usar NFKC normalization
# Algunos caracteres Unicode se normalizan a otros
# Pero Python usa la forma en que escribimos los identificadores
#
# WAIT: Revisando la descripción del problema
# "Prueba de Pyjail"
# "nc host8.dreamhack.games 16340"
#
# Es un desafío tipo sandbox escape
# 
# NUEVA ESTRATEGIA:
# Vamos a intentar payloads específicos para ver qué información podemos obtener
#
# 1. Primero, verifiquemos qué podemos hacer con lo disponible
# 2. Luego, tratemos de encontrar un bypass creativo
#
# Payloads para probar:
# 1. "a=__name__" - ver si podemos asignar y si funciona
# 2. "a=__doc__" - ver documentación
# 3. Intentar generar números sin dígitos: "a=True==True" (pero = doble usa ==)
# 4. "a=~True" - NOT bit a bit de True (que es 1) = -2
# 5. "a=-~True" - doble negación para obtener 2
# 6. Usar estas técnicas para construir algo
#
# PERO EL PROBLEMA: Sin print() o forma de salida, ¿cómo vemos resultados?
# A menos que... causemos un error intencional que muestre información
#
# IDEA: ¿Podemos usar el REPL behavior?
# No, porque esto no es un REPL, es exec()
#
# ÚLTIMA IDEA ANTES DE PROBAR:
# Tal vez necesitamos crear una secuencia de asignaciones que eventualmente
# resulten en la ejecución de código cuando el intérprete las procese
#
# O tal vez... el desafío requiere que encontremos una vulnerabilidad específica
# en el filtro del regex o en la lógica
#
# VAMOS A PROBAR COSAS SISTEMÁTICAMENTE:

test_payloads = [
    # Test 1: Variable assignment simple
    ("a=True", "Asignar True a 'a'"),
    
    # Test 2: Acceder a __name__
    ("a=__name__", "Acceder a __name__"),
    
    # Test 3: Intentar operaciones matemáticas
    ("True-True", "Operación True-True"),
    
    # Test 4: Generar números con operadores bitwise
    ("a=~True", "Bitwise NOT de True"),
    
    # Test 5: Intentar acceder a __builtins__
    ("__name__", "Solo __name__"),
    
    # Test 6: Intentar causar error con división por cero
    ("True/~True", "División por ~True (que es -2)"),
    
    # Test 7: Variables con underscore
    ("_=True", "Asignar a _"),
    
    # Test 8: Múltiples statements
    ("a=True;a", "Multiple statements"),
]

print("=" * 80)
print("PAYLOADS A PROBAR:")
print("=" * 80)
for payload, desc in test_payloads:
    print(f"{payload:30s} - {desc}")
print("=" * 80)
