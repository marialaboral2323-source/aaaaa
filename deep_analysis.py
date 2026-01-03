#!/usr/bin/env python3

# ANÁLISIS PROFUNDO:
# 
# Descubrimientos hasta ahora:
# 1. __name__ funciona (no produce error)
# 2. __name__.__len__ funciona (acceso a método)
# 3. No podemos usar True, False, None (tienen letras prohibidas: r, F, o)
# 4. Letras permitidas: a c d e g i j l m n p s t u w x (y mayúsculas)
# 5. Sin paréntesis = no podemos LLAMAR funciones
# 6. Sin corchetes = no podemos indexar
# 7. Longitud máxima: 25 caracteres
#
# IDEA CLAVE: 
# En Python, algunos objetos tienen comportamiento especial cuando se evalúan
# sin ser llamados. Por ejemplo:
# - Decoradores se aplican automáticamente
# - Descriptores se activan al acceder
# - Properties se ejecutan al acceder
# - __getattribute__ se llama automáticamente
#
# PERO __getattribute__ está en la lista de prohibidos!
#
# OTRA IDEA:
# ¿Qué pasa con __builtins__?
# Podemos acceder a él directamente en el globals
#
# Probemos acceder a funciones en __builtins__ sin llamarlas
# y ver si podemos hacer algo útil
#
# En Python 3, __builtins__ puede ser un módulo o un dict dependiendo del contexto
# En exec() con globals={'__builtins__': __builtins__}, es el objeto builtins
#
# Funciones útiles en builtins que NO tienen letras prohibidas:
# - eval (tiene 'v' - PROHIBIDA)
# - exec (permitida! e-x-e-c)
# - open (tiene 'o' - PROHIBIDA) 
# - input (permitida! i-n-p-u-t)
# - len (permitida! l-e-n)
# - id (permitida! i-d)
# - dir (tiene 'r' - PROHIBIDA)
# - type (tiene 'y' - PROHIBIDA)
# - getattr (tiene 'r' - PROHIBIDA)
# - setattr (tiene 'r' - PROHIBIDA)
# - __import__ (prohibida en lista de palabras)
#
# WAIT! exec está permitida!
# Pero... necesitamos () para llamar exec
#
# A menos que... ¿podamos crear una situación donde exec se llame automáticamente?
#
# IDEA CRÍTICA: Decoradores!
# En Python, si hacemos:
# @decorator
# def func(): pass
#
# El decorador se APLICA automáticamente sin que lo llamemos con ()
# Es equivalente a: func = decorator(func)
#
# Pero:
# 1. Necesitamos 'def' que tiene 'f' - PROHIBIDA
# 2. Los decoradores necesitan ser una expresión que evalúe a un callable
# 3. Luego ese callable se llama con la función como argumento
#
# Hmm, esto no funciona directamente...
#
# NUEVA IDEA: Assignment expressions (walrus operator :=)
# En Python 3.8+, podemos usar :=
# Pero aún así, no ejecuta funciones automáticamente
#
# PENSANDO MÁS:
# ¿Hay algún SIDE EFFECT que podamos causar sin llamar funciones?
# 
# En Python:
# - Asignaciones a variables: no tienen side effects visibles fuera del scope
# - Operadores: solo calculan valores
# - Accesos a atributos: pueden tener side effects si hay properties/descriptors
#
# MOMENTO: ¿Y si el objetivo NO es leer el flag directamente, sino extraer
# información de alguna otra forma?
#
# Por ejemplo:
# - Causar un error que revele rutas
# - Hacer timing attacks
# - Explotar alguna funcionalidad del exec() mismo
#
# ERROR DISCLOSURE:
# Si causamos un error, el traceback podría revelar información
# Pero el código captura Exception y solo muestra type y message, no traceback
#
# TIMING ATTACK:
# Podríamos hacer algo que tome diferente tiempo según condiciones
# Pero no tenemos forma de medir el tiempo desde afuera con precisión
# Y además, ¿cómo haríamos un loop sin números y sin 'for'/'while' (tienen letras prohibidas)?
#
# 'for' tiene 'f' y 'o' y 'r' - todas prohibidas
# 'while' tiene 'h' - prohibida
#
# EXPLOIT DEL EXEC:
# exec() tiene algunas peculiaridades
# Por ejemplo, el código se ejecuta en un namespace específico
# Pero después del exec, no podemos acceder a ese namespace desde afuera
#
# WAIT: Estoy pensando en esto mal
# 
# El código acepta MÚLTIPLES LÍNEAS
# Cada línea puede ser un statement
# Las líneas se unen con \n y luego se validan TODAS juntas
# Luego se ejecutan con exec()
#
# ¿Qué pasa si usamos múltiples líneas para construir algo?
#
# Por ejemplo:
# Línea 1: a=__name__
# Línea 2: b=a.__len__
# Línea 3: ... (?)
#
# Pero aún así, sin () no podemos llamar nada
#
# REFLEXIÓN: Este pyjail parece IMPOSIBLE con las restricciones actuales
# A menos que haya un bypass del filtro
#
# BYPASS DEL FILTRO:
# Revisemos el código del filtro nuevamente:
#
# 1. re.search(r'[bfhkqrvyzo0123456789BFHKQRVYZO]', code)
#    - Busca esas letras/números ANYWHERE en el código
#    - Usa re.search, no re.match, así que busca en cualquier parte
#    - No hay bypass obvio aquí
#
# 2. len(code) > 25
#    - Longitud máxima 25 caracteres
#    - WAIT! Esto es len(code) donde code es el string COMPLETO
#    - Incluyendo los \n entre líneas!
#    - Así que múltiples líneas cuentan para el límite
#
# 3. for char in chrban: if char in code
#    - Busca caracteres prohibidos en el string
#    - No hay bypass obvio
#
# 4. clow = code.lower(); for keyword in ban: if keyword in clow
#    - Convierte a lowercase y busca palabras prohibidas
#    - Busca SUBSTRING, no palabras completas
#    - Ejemplo: 'print' está prohibido, así que 'printing' también falla
#    - Pero esto busca en code.lower(), así que case no importa
#
# ¿HAY ALGÚN BYPASS?
#
# Idea 1: Unicode normalization
# - Python no normaliza automáticamente Unicode en código fuente (en Python 3)
# - Pero los identificadores deben ser válidos
# - Caracteres Unicode en strings pueden ser diferentes
# - Pero necesitamos comillas para strings, que están prohibidas
#
# Idea 2: Encoding tricks
# - El input() lee UTF-8
# - No hay procesamiento especial
# - No hay bypass obvio
#
# Idea 3: Regex bypass
# - La regex r'[bfhkqrvyzo0123456789BFHKQRVYZO]' es simple
# - No hay Unicode flags
# - ¿Podría haber caracteres Unicode que se EJECUTEN como números pero no sean detectados?
# - En Python 3, los números en código deben ser ASCII 0-9
# - No hay bypass aquí
#
# Idea 4: Keyword bypass
# - La búsqueda es substring en lowercase
# - 'print' está prohibido
# - ¿Podemos de alguna forma ejecutar print sin tener 'print' en el código?
# - Sí! Usando getattr(__builtins__, 'print')
# - Pero 'r' está prohibida, así que no podemos escribir 'print' de todos modos
# - Y necesitamos () para llamar getattr
# - Y necesitamos comillas para el string 'print'
#
# Idea 5: ¿Hay alguna variable predefinida que tenga algo útil?
# - __name__ está disponible (es '__main__' en el contexto de exec normalmente)
# - __builtins__ está en el globals
# - ¿Hay otras variables especiales?
#
# En el contexto del exec:
# globals = {'__builtins__': __builtins__}
# locals = {}
#
# Así que solo __builtins__ está en el namespace
#
# IDEA: ¿Podemos acceder a __builtins__ directamente?
# Probemos: __builtins__

print("Testing __builtins__ access...")
print("Payload: __builtins__")
print("Length:", len("__builtins__"))
print("Has banned chars:", any(c in "bfhkqrvyzo0123456789BFHKQRVYZO" for c in "__builtins__"))
print("Has banned keywords:", any(kw in "__builtins__".lower() for kw in ['import', 'compile', '__import__', 'breakpoint', 'help', 'license', 'copyright', 'credits', '__subclasses__', 'load_module', 'system', 'popen', 'subprocess', 'print', 'global', 'mro', '__class__', 'copy', 'sys', '__getattribute__', '+']))

# builtins tiene 'b' que está prohibida!
# Hmm...

# ¿Qué tal usar globals()?
# globals tiene 'o' y 'b' - ambas prohibidas

# ¿Qué tal locals()?
# locals tiene 'o' y 'c' - 'o' está prohibida

# ¿Qué tal vars()?
# vars tiene 'v' y 'r' - ambas prohibidas

# ¿Qué tal dir()?
# dir tiene 'r' - prohibida

# ESTAMOS ATASCADOS...

# WAIT: Tal vez estoy enfocándome demasiado en Python puro
# ¿Y si hay una vuln en cómo el servidor procesa el input?
#
# El servidor usa socat para conectar TCP a stdin/stdout de Python
# socat TCP-LISTEN:8000,reuseaddr,fork EXEC:'python3 /app/app.py'
#
# Cada conexión ejecuta una nueva instancia de app.py
# app.py lee líneas con input() hasta recibir una línea vacía
# Luego ejecuta el código con exec()
#
# ¿Hay alguna forma de inyectar algo que bypass el filtro?
# - Command injection en socat: no, el comando está hardcoded
# - Injection en input(): no, input() es seguro
# - Bypass del exec: no, exec() ejecuta lo que le demos
#
# MOMENTO CRÍTICO:
# Tal vez necesito pensar FUERA de Python
# ¿Hay algo en el ENTORNO que pueda explotar?
#
# Según el Dockerfile:
# - flag.txt está en /app/
# - flag.txt tiene permisos 444 (read-only)
# - app.py tiene permisos 555 (read + execute)
# - Ejecutando como usuario 'pyjail' (no root)
#
# Así que el flag está ahí, solo necesitamos leerlo
#
# PERO SIN FORMA DE EJECUTAR CÓDIGO, NO PODEMOS LEERLO
#
# A menos que...
#
# IDEA RADICAL:
# ¿Y si el pyjail NO es resoluble con las restricciones aparentes?
# ¿Y si hay una vuln diferente que debo encontrar?
#
# Por ejemplo:
# - ¿Vulnerabilidad en la versión de Python 3.11?
# - ¿Algún truco específico de Python 3.11 que permita ejecutar código sin ()?
# - ¿Alguna configuración especial del __builtins__ que pueda explotar?
#
# PYTHON 3.11 FEATURES:
# - Exception groups
# - Improved error messages
# - Faster CPython
# - Task groups in asyncio
# - ... nada obvio que ayude aquí
#
# IDEA: ¿Y si busco exploits conocidos de pyjail sin paréntesis?
# NO! El usuario dijo explícitamente no buscar writeups ni soluciones
#
# Debo resolver esto yo mismo...
#
# BACK TO BASICS:
# Sin () no puedo llamar funciones
# Sin [] no puedo indexar
# Sin números no puedo usar literales numéricos
# Sin muchas letras, estoy muy limitado
#
# ¿Hay ALGUNA forma en Python de ejecutar código sin ()?
#
# WAIT WAIT WAIT:
# ¿Qué pasa con el operador @ (matmul)?
# En Python 3.5+, @ es el operador de multiplicación de matrices
# Se puede sobrecargar con __matmul__
#
# Si tuviera un objeto con __matmul__ que ejecute código...
# Pero para crear tal objeto, necesitaría definir una clase
# Y 'class' tiene 'c' y 's' y 'a' y 'l' - todas permitidas!
#
# ¡class está permitida!
#
# Pero:
# - Necesitamos 'def' para definir __matmul__ - 'f' está prohibida
# - O necesitamos asignar un lambda - pero 'lambda' tiene 'b' y 'a' y 'm' - 'b' prohibida
#
# ARGH!
#
# ¿Qué tal otros operadores que se pueden sobrecargar?
# - __add__ (+) - pero + está en la lista de prohibidos!
# - __sub__ (-) - permitido!
# - __mul__ (*) - permitido!
# - __truediv__ (/) - permitido!
# - __mod__ (%) - permitido!
# - __matmul__ (@) - permitido!
# - __and__ (&) - permitido!
# - __or__ (|) - permitido! pero 'or' tiene 'o' y 'r' prohibidas
# - __xor__ (^) - permitido! pero 'xor' tiene 'o' y 'r'
#
# PERO para sobrecargar estos, necesitamos definir la clase
# Y para definir métodos, necesitamos 'def' con 'f' prohibida
#
# ¿Y si uso asignación directa a __dict__?
# Pero necesitamos [] para indexar __dict__
#
# ¿Y si uso setattr?
# setattr tiene 'r' prohibida
#
# ESTOY EN UN CÍRCULO VICIOSO
#
# ÚLTIMA IDEA DESESPERADA:
# ¿Y si el código tiene un BUG?
# Revisemos el código del filtro una vez más...
#
# def block(code):
#     chrban = ['[', ']', '(', ')', '"', "'", '\\', '/', '?', '*']
#     ban = [...]
#     
#     if re.search(r'[bfhkqrvyzo0123456789BFHKQRVYZO]', code):
#         return False, "\nnope!"
#     
#     if len(code) > 25:
#         return False, "\nnope!"
#     
#     for char in chrban:
#         if char in code:
#             return False, "\nnope!"
#     
#     clow = code.lower()
#     for keyword in ban:
#         if keyword in clow:
#             return False, "\nnope!"
#     
#     return True, "ok"
#
# WAIT!!! / está en chrban!
# Pero la descripción de chrban muestra '/' como prohibido
# Sin embargo, probé arriba y no mencioné problema con /
#
# Probemos algo con /:

# Además, * está en chrban!
# Así que no podemos usar * tampoco
#
# Revisando chrban: ['[', ']', '(', ')', '"', "'", '\\', '/', '?', '*']
#
# Esto significa:
# - Sin brackets, paréntesis, comillas: confirma lo que sabía
# - Sin backslash: no podemos usar escape sequences
# - Sin /: no podemos usar división... WAIT, probé división arriba mentalmente
# - Sin ?: no podemos usar ternary operator
# - Sin *: no podemos usar multiplicación, unpacking, etc.
#
# Operadores matemáticos disponibles: + - % @ & | ^ ~ << >> 
# PERO + está en la lista de palabras prohibidas!
#
# Así que solo tenemos: - % @ & | ^ ~ << >> (y comparaciones < > == != etc)
#
# IDEA: ¿Puedo construir un payload usando solo estos operadores?
#
# Con - puedo restar
# Con ~ puedo hacer bitwise NOT
# Con << >> puedo hacer bitwise shifts
# Con & | ^ puedo hacer bitwise AND OR XOR
# Con @ puedo hacer matmul (si hay objetos que lo soporten)
#
# Pero sin una forma de EJECUTAR algo, solo puedo calcular valores
# Y sin una forma de MOSTRAR resultados (sin print, sin paréntesis para otras formas),
# ¿de qué sirve?
#
# A menos que... el RESULTADO del exec sea observable de alguna forma
#
# En Python, exec() puede modificar el namespace que se le pasa
# Pero en este código, locals está vacío y no se usa después
# globals tiene __builtins__, pero tampoco se inspecciona después
#
# El código solo captura excepciones y las muestra
#
# IDEA: ¿Y si causo un error ESPECÍFICO que revele información?
#
# Por ejemplo:
# - AttributeError con un mensaje que incluya parte del flag
# - NameError que revele variables del entorno
# - etc.
#
# Pero los errores solo muestran el tipo y el mensaje
# Y los mensajes son estándar de Python, no revelan contenido de archivos
#
# A menos que...
#
# ¿Y si cargo el archivo de alguna forma en el scope y luego causo un error que lo revele?
#
# Pero necesitaría open() para cargar el archivo, y open tiene 'o' prohibida
# Y necesitaría () para llamar open de todos modos
#
# ESTOY MUY ATASCADO
#
# Dejame pensar en payloads CREATIVOS que puedan hacer ALGO observable...
#
# Payload idea: Modificar __builtins__ de alguna forma?
# Pero __builtins__ tiene 'b' prohibida
#
# Payload idea: Usar algún método mágico que se llame automáticamente?
# - __del__ se llama cuando un objeto se destruye
# - Pero necesitaría crear un objeto y definir __del__
# - Y necesitaría 'class' o 'def', y 'def' tiene 'f' prohibida
#
# class está permitida! (c-l-a-s-s, todas las letras permitidas)
#
# ¿Puedo definir una clase sin usar 'def' para los métodos?
#
# En Python, puedo asignar funciones a atributos de clase después
# Pero necesito crear las funciones primero
# Sin 'def' ni 'lambda', ¿cómo?
#
# ¿Puedo usar funciones builtin como métodos?
# Por ejemplo:
# class A:
#     pass
# A.__del__ = exit
#
# Pero necesitaría () para instanciar A
# Y necesitaría una función que haga algo útil cuando se llame
#
# 'exit' está permitida (e-x-i-t)
# Pero exit solo termina el programa, no ayuda
#
# MOMENTO: ¿Y si simplemente ENVÍO MÚLTIPLES PAYLOADS?
# Cada conexión es independiente, puedo enviar muchas
# Tal vez pueda hacer fuerza bruta o algo similar
#
# Pero ¿fuerza bruta de qué? Sin output, no puedo saber si acerté
#
# A menos que...
#
# TIMING SIDE CHANNEL:
# Si un payload hace que el servidor se cuelgue o tarde más,
# puedo medir eso desde afuera!
#
# ¿Cómo puedo hacer que el server se cuelgue sin loops?
# - Recursión infinita
# - Pero necesito definir una función recursiva, requiere 'def'
# - O necesito llamar algo recursivamente
#
# SIN FORMA DE HACER ESTO CON LAS RESTRICCIONES
#
# OK, NECESITO UN ENFOQUE COMPLETAMENTE DIFERENTE
#
# Voy a revisar si hay algún truco OSCURO de Python que no conozco...
#
# OSCURE PYTHON TRICKS:
# 1. Using `...` (Ellipsis) - es un objeto singleton
# 2. Exec sin paréntesis: NO EXISTE en Python 3
# 3. Eval sin paréntesis: NO EXISTE en Python 3
# 4. Backticks: Solo Python 2
# 5. Import hooks: Necesita definir funciones
# 6. Metaclasses: Muy complejo, necesita 'class' y 'def'
#
# WAIT: ... (Ellipsis) está permitido!
# ... es un literal como None, True, False
# No tiene letras prohibidas (son solo 3 puntos)
#
# ¿Qué puedo hacer con Ellipsis?
# Es solo un singleton, tipo(Ellipsis) es type 'ellipsis'
# No tiene métodos útiles especiales
#
# OTRO TRICK: __import__  está prohibido en la lista de palabras
# Pero hay otras formas de importar?
# - importlib.import_module - necesita import primero
# - execfile - solo Python 2
# - compile + exec - compile está prohibido
#
# NO HAY FORMA
#
# CONCLUSIÓN TEMPORAL:
# Con las restricciones actuales, parece imposible ejecutar código útil
# A menos que haya:
# 1. Un bug en el filtro que no he encontrado
# 2. Un truco muy oscuro de Python que desconozco
# 3. Una vuln diferente en el servidor/setup
#
# Voy a probar algunos payloads más creativos para ver si encuentro algo...

