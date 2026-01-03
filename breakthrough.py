#!/usr/bin/env python3

# BREAKTHROUGH!
# Puedo definir una clase!
# class A:pass funciona y solo tiene 13 caracteres (con el newline son 14)
#
# Ahora, ¿qué puedo hacer con una clase?
#
# En Python, cuando defines una clase, se ejecuta el cuerpo de la clase
# Cualquier código en el cuerpo se ejecuta durante la definición
#
# Por ejemplo:
# class A:
#     x = 1 + 1  # Esto se ejecuta inmediatamente
#     print("hello")  # Esto también se ejecuta
#
# PERO print está prohibido
#
# ¿Qué código útil puedo poner en el cuerpo de una clase?
#
# Ideas:
# 1. Importar módulos - 'import' prohibido
# 2. Definir métodos - 'def' tiene 'f' prohibida
# 3. Asignar atributos con efectos secundarios
#
# Para #3, ¿qué asignaciones tienen efectos secundarios observables?
#
# En Python, las asignaciones normales no tienen efectos secundarios
# A menos que uses descriptores/properties
#
# PERO: Si asigno a un atributo de clase que es un descriptor,
# el descriptor se invoca!
#
# ¿Hay descriptores builtin que pueda usar?
#
# property() es un descriptor, pero:
# - 'property' tiene 'o', 'p', 'e', 'r', 't', 'y' - 'o', 'r', 'y' prohibidas
#
# staticmethod, classmethod:
# - 'staticmethod' tiene 't' prohibida... wait no, 't' está permitida
# - Veamos: s-t-a-t-i-c-m-e-t-h-o-d
# - Tiene 'h' y 'o' prohibidas
#
# ¿Hay otros descriptores?
#
# IDEA DIFERENTE:
# ¿Qué pasa si uso el mecanismo de metaclass?
#
# class A(metaclass=SomeMetaclass):
#     pass
#
# Cuando Python crea la clase, llama a SomeMetaclass.__call__
# con el namespace de la clase
#
# Pero:
# - 'metaclass' tiene 'c' prohibida... no wait, 'c' está permitida
# - m-e-t-a-c-l-a-s-s: todas permitidas!
# - Pero necesitamos () para pasar el argumento metaclass=...
# - Y necesitamos un metaclass que haga algo útil
#
# WAIT: En Python 3, puedes especificar metaclass sin =:
# class A(metaclass):  # NO, esto no es sintaxis válida
#
# Necesitas: class A(metaclass=Meta):
# Y esto requiere = y el nombre de la metaclass
#
# Pero NO requiere () alrededor de metaclass=Meta!
# La sintaxis es: class Name(bases, **kwds):
#
# Así que podría hacer:
# class A(metaclass=type):
#     pass
#
# Veamos:
# - 'class A' : 7 chars
# - '(metaclass=type):': 16 chars
# - 'pass': 4 chars
# - Total: 27 chars - DEMASIADO LARGO (límite 25)
#
# Necesito nombres más cortos:
# class A(metaclass=type):pass
# - Total: 28 chars - aún muy largo
#
# class A(metaclass=int):pass
# - 'int' tiene 'i', 'n', 't' todas permitidas
# - Total: 27 chars - aún muy largo
#
# Necesito algo AÚN más corto...
#
# class A:
#  x=...
#
# Con espacios/indentación mínima:
# class A:
#  x=__name__
#
# Esto es válido Python y cuenta los newlines/espacios
# Veamos: 'class A:\n x=__name__'
# - Longitud: 19 chars - DENTRO DEL LÍMITE!
#
# ¿Qué hace esto?
# - Define una clase A
# - Con un atributo x que es __name__
# - No hace nada útil visible
#
# PERO: El cuerpo de la clase se ejecuta como código normal
# Así que cualquier expresión válida ahí se ejecuta
#
# ¿Puedo poner algo que lea el archivo?
#
# Ideas:
# - open - tiene 'o' prohibida
# - __import__ - prohibido en keywords
# - exec - permitida pero necesita () para llamar
# - eval - tiene 'v' prohibida
#
# WAIT: ¿Qué pasa si uso exec como statement en Python 2 style?
# En Python 2, exec era un statement: exec "code"
# En Python 3, exec es una función: exec("code")
#
# Python 3 no tiene exec statement, solo función
#
# IDEA: ¿Puedo usar __init__ sin def?
#
# No, necesito def para definir métodos
# A menos que asigne un callable después
#
# Pero para asignar después, necesito tener acceso a la clase
# después de definirla, y eso requiere más líneas que excedan el límite
#
# PENSANDO MÁS...
#
# ¿Hay alguna forma de ejecutar código arbitrario desde el cuerpo de una clase?
#
# En Python, el cuerpo de una clase es esencialmente un bloque de código
# que se ejecuta en un namespace especial
# El namespace resultante se usa para crear el diccionario de la clase
#
# Así que puedo poner cualquier código válido ahí
# Pero con las restricciones de:
# - Sin ()
# - Sin []
# - Sin números
# - Sin ciertas letras
# - Max 25 chars
#
# Es muy difícil...
#
# NUEVA IDEA: ¿Qué pasa con las comprehensions?
#
# [x for x in ...] - List comprehension
# Pero necesito [] que está prohibido
#
# {x for x in ...} - Set comprehension
# Pero necesito {} y 'for' tiene 'o', 'r', 'f' prohibidas
#
# (x for x in ...) - Generator expression
# Pero necesito () que está prohibido
# Y 'for' está prohibido
#
# NO FUNCIONA
#
# IDEA: ¿Operadores de slice sin []?
# En Python, slice(start, stop, step) crea un objeto slice
# Pero necesito () para llamar slice
#
# Y la sintaxis x[a:b] requiere []
#
# IDEA: ¿Assignment con unpacking?
# a, b = 1, 2
# Pero necesito números
#
# a, b = __name__, __name__
# Esto funciona pero no hace nada útil
# Y tiene más de 25 chars
#
# IDEA CRÍTICA: ¿Puedo modificar __builtins__ desde el cuerpo de la clase?
#
# class A:
#  __builtins__.x = ...
#
# Pero __builtins__ tiene 'b' prohibida
#
# IDEA: ¿Usar __dict__ o __annotations__ o algo similar?
#
# class A:
#  __annotations__=...
#
# Esto asigna a __annotations__ pero no hace nada útil
#
# IDEA: ¿Crear una excepción con información del flag?
#
# class A:
#  assert False, open(...)
#
# Pero:
# - open tiene 'o' prohibida
# - assert tiene 'a', 's', 'e', 't' permitidas!
# - Pero necesito () para llamar open
# - Y necesito comillas para el filename
#
# NO FUNCIONA
#
# ESTOY GIRANDO EN CÍRCULOS DE NUEVO
#
# Déjame pensar en esto desde un ángulo diferente...
#
# El objetivo final es leer /app/flag.txt
# Para leer un archivo necesito:
# 1. Abrirlo: open()
# 2. Leerlo: read()
# 3. Mostrarlo: print() o similar
#
# TODAS estas operaciones requieren () para llamar funciones
#
# Sin () no puedo llamar funciones en Python 3
# Esto es un hecho fundamental del lenguaje
#
# A MENOS QUE...
#
# ¿Hay alguna situación donde Python llame una función automáticamente
# sin que yo use ()explícitamente?
#
# Situaciones donde Python llama funciones automáticamente:
# 1. __init__ cuando creas una instancia: x = Class()
#    - Pero Class() requiere ()
# 2. __call__ cuando usas un objeto como función: obj()
#    - Pero obj() requiere ()
# 3. Descriptors (__get__, __set__) cuando accedes a atributos
#    - Esto es prometedor!
# 4. Properties cuando accedes a atributos
#    - También prometedor!
# 5. __enter__ y __exit__ con context managers: with obj:
#    - 'with' tiene 'w', 'i', 't', 'h' - 'h' prohibida
# 6. __iter__ y __next__ con loops: for x in obj:
#    - 'for' tiene prohibidas varias letras
# 7. Operadores sobrecargados: __add__, __sub__, etc.
#    - Esto es muy prometedor!
# 8. __del__ cuando el objeto se destruye
#    - Interesante pero difícil de controlar
# 9. Metaclasses cuando se crea una clase
#    - Ya exploré esto
# 10. Decorators cuando se definen funciones
#     - Necesito 'def' con 'f' prohibida
#
# FOCUS EN #3, #4, #7:
#
# DESCRIPTORS:
# Si creo un descriptor y lo accedo, se llama __get__
# class Desc:
#     def __get__(self, obj, objtype=None):
#         # código aquí se ejecuta cuando accedo al descriptor
#         return value
#
# class A:
#     x = Desc()
#
# a = A()  # Requiere ()
# a.x  # Esto llama Desc.__get__
#
# Pero para crear una instancia, necesito ()
#
# WAIT: ¿Puedo acceder a un descriptor de clase SIN instanciar?
# A.x  # En un descriptor de clase, esto también llama __get__
#
# Así que si puedo:
# 1. Definir una clase con un descriptor
# 2. Acceder al descriptor sin ()
#
# Entonces el código en __get__ se ejecuta!
#
# Pero el problema es: ¿cómo defino un descriptor sin 'def'?
#
# Necesito definir __get__ que requiere 'def'
# A menos que... asigne una función existente
#
# class Desc:
#     __get__ = some_existing_function
#
# Pero las funciones existentes necesitan la firma correcta
# Y necesito que hagan algo útil
#
# IDEA: ¿Puedo usar una función builtin como __get__?
# Por ejemplo:
# class Desc:
#     __get__ = len
#
# Pero len tiene la firma len(obj), no __get__(self, obj, objtype)
# Probablemente causaría un error
#
# Hmm, esto no es simple...
#
# OPERADORES SOBRECARGADOS:
# Si defino __sub__ y uso -, se llama __sub__
# class A:
#     def __sub__(self, other):
#         # código aquí
#         return result
#
# a = A()  # Requiere ()
# a - 1  # Esto llama __sub__
#
# De nuevo, necesito instanciar con ()
#
# WAIT: ¿Hay clases builtin que ya tengan operadores sobrecargados
# de formas interesantes?
#
# Por ejemplo, int, str, list, etc.
# Pero estos se comportan normalmente
#
# ¿Hay alguna clase en __builtins__ que tenga un comportamiento especial?
#
# IDEA LOCA: ¿Qué pasa con las excepciones?
# Las clases de Exception tienen __init__ que se puede llamar
# Pero de nuevo, necesito () para crearlas
#
# WAIT WAIT WAIT:
# ¿Puedo usar raise sin ()?
#
# raise SomeException  # Esto crea una instancia automáticamente!
#
# En Python 3, puedes hacer:
# raise Exception  # Sin (), se instancia automáticamente
#
# Así que raise llama __init__ automáticamente!
#
# ¿Puedo explotar esto?
#
# class MyException(Exception):
#     def __init__(self):
#         # código aquí se ejecuta cuando se lanza la excepción
#         super().__init__()
#
# raise MyException  # Esto llama __init__!
#
# Pero:
# - Necesito 'def' para definir __init__
# - Necesito () para llamar super().__init__()
# - Y el código captura las excepciones, así que no sale del script
#
# Hmm...
#
# PERO: ¿Qué pasa si defino __init__ sin def?
#
# No hay forma sin def o lambda (que tiene 'b' prohibida)
#
# A MENOS QUE...
#
# ¿Puedo asignar a __init__ después de definir la clase?
#
# class A:
#     pass
# A.__init__ = some_function
# raise A
#
# Pero esto es múltiples líneas y excede 25 chars
# Y necesito some_function que haga algo útil
#
# IDEA: ¿Usar una función builtin como __init__?
# class A:
#     __init__ = exit
# raise A
#
# exit es builtin y no tiene letras prohibidas (e-x-i-t)
# Pero exit() termina el programa, no ayuda
#
# Y esto es más de 25 chars de todos modos
#
# FRUSTRACIÓN MÁXIMA
#
# Necesito encontrar una forma completamente diferente...
#
# MOMENTO: Tal vez estoy sobre-complicando esto
#
# ¿Qué pasa si el filtro tiene un bug SIMPLE que no he visto?
#
# Revisemos el filtro LÍNEA POR LÍNEA:

# def block(code):
#     chrban = ['[', ']', '(', ')', '"', "'", '\\', '/', '?', '*']
#     ban = [
#         'import', 'compile', '__import__',
#         'breakpoint', 'help', 'license', 'copyright', 'credits', '__subclasses__', 'load_module',
#         'system', 'popen', 'subprocess', 'print', 'global', 'mro', '__class__', 'copy', 'sys', '__getattribute__', '+'
#     ]
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

# WAIT!!!! VOY A REVISAR ESTO MÁS CUIDADOSAMENTE
#
# La validación del LENGTH:
# if len(code) > 25:
#     return False, "\nnope!"
#
# Esto verifica len(code) donde code es el string COMPLETO incluyendo newlines
#
# Pero DESPUÉS el código se ejecuta con exec(code, ...)
# exec() puede ejecutar múltiples statements separados por \n
#
# PERO la validación verifica el string COMPLETO
# Así que si envío:
# a=__name__\nb=__name__
# El len es más de 25 y falla
#
# NO HAY BYPASS AQUÍ
#
# La validación de CARACTERES PROHIBIDOS:
# for char in chrban: if char in code
#
# Esto es simple string search, no hay bypass obvio
#
# La validación de REGEX:
# re.search(r'[bfhkqrvyzo0123456789BFHKQRVYZO]', code)
#
# Esto busca cualquiera de esas letras/números
# No hay bypass Unicode porque Python 3 trata los caracteres correctamente
#
# La validación de KEYWORDS:
# clow = code.lower()
# for keyword in ban: if keyword in clow
#
# Convierte a lowercase y busca substring
# NO busca palabras completas, solo substring
# Así que 'print' bloquea 'printing', 'printf', etc.
#
# WAIT: ¿Qué pasa si la keyword está dividida por un newline?
#
# Por ejemplo:
# pri\nnt
#
# Cuando se junta es 'pri\nnt' que en lowercase es 'pri\nnt'
# ¿'print' in 'pri\nnt'? -> False
#
# ¡¡¡BYPASS ENCONTRADO!!!
#
# Si divido una keyword prohibida con \n, el filtro no la detecta!
#
# Pero WAIT: Cuando Python ejecuta el código con \n,
# 'pri\nnt' no es sintaxis válida
#
# A menos que... use line continuation con \
# 'pri\\\nnt' -> Esto se interpreta como 'print'
#
# Pero \ está en chrban, prohibido!
#
# Hmm, no funciona...
#
# OTRA IDEA: ¿Qué pasa con espacios o tabs?
# 'pri nt' -> No es sintaxis válida
# 'pr int' -> No es sintaxis válida
#
# NO FUNCIONA
#
# DESESPERACIÓN TOTAL
#
# Voy a listar TODAS las funciones builtin disponibles
# y ver cuáles puedo deletrear con las letras permitidas:

import builtins
allowed_letters = set('acdegijlmnpstuwxACDEGIJLMNPSTUWX')

builtin_names = dir(builtins)
usable = []
for name in builtin_names:
    if all(c in allowed_letters or c == '_' for c in name):
        usable.append(name)

print("Builtins usables (solo con letras permitidas):")
for name in sorted(usable):
    print(f"  {name}")
