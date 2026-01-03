#!/usr/bin/env python3

# ¡¡¡EXEC ESTÁ DISPONIBLE!!!
#
# exec es una función builtin que:
# - Solo tiene letras permitidas: e-x-e-c
# - No está en la lista de palabras prohibidas
# - Puede ejecutar código arbitrario
#
# PERO necesito () para llamar exec
# A menos que... haya una forma de hacer exec ejecutarse sin ()
#
# IDEA: ¿Puedo usar exec como descriptor o en alguna otra forma?
#
# WAIT: Voy a revisar la lista de palabras prohibidas de nuevo:
# 'import', 'compile', '__import__',
# 'breakpoint', 'help', 'license', 'copyright', 'credits', '__subclasses__', 'load_module',
# 'system', 'popen', 'subprocess', 'print', 'global', 'mro', '__class__', 'copy', 'sys', '__getattribute__', '+'
#
# exec NO está en la lista!
#
# Pero el problema sigue siendo: necesito () para llamar exec
#
# OTRAS FUNCIONES INTERESANTES:
# - input: lee del stdin - pero necesita ()
# - eval: NO está en la lista permitida (tiene 'v' prohibida)
# - exec: ejecuta código - pero necesita ()
# - isinstance: chequea tipos - pero necesita ()
# - len: obtiene longitud - pero necesita ()
#
# TODAS NECESITAN ()
#
# MOMENTO: ¿Puedo usar raise con exec de alguna forma?
#
# raise exec  # ¿Esto funciona?
# No, exec no es una excepción
#
# ¿Puedo usar assert?
# assert False, exec("code")  # Necesito () para llamar exec
#
# ¿Puedo usar with?
# with exec:  # 'with' tiene 'h' prohibida
#
# ¿Puedo usar for?
# for x in exec:  # 'for' tiene 'o', 'r', 'f' prohibidas
#
# ESTOY EN EL MISMO PROBLEMA
#
# ÚLTIMA IDEA DESESPERADA:
# ¿Hay alguna forma de "ensamblar" una llamada de función sin usar ()?
#
# En Python 2, había sintaxis como:
# print "hello"  # sin ()
# exec "code"  # sin ()
#
# Pero Python 3 eliminó estas sintaxis
#
# En Python 3, NO HAY FORMA de llamar una función sin ()
# Esto es un hecho fundamental del lenguaje
#
# A MENOS QUE...
#
# Hmm, estoy pensando...
#
# ¿Qué pasa con las f-strings?
# f"{expr}" evalúa expr
# Pero necesito comillas que están prohibidas
#
# ¿Qué pasa con los templates?
# No son built-in del lenguaje
#
# ¿Qué pasa con compile + eval?
# compile está en la lista prohibida
# eval tiene 'v' prohibida
#
# VOY A PROBAR UN ENFOQUE DIFERENTE:
# Tal vez NO necesito leer el archivo directamente
# Tal vez puedo extraer la información de otra forma
#
# Por ejemplo:
# - Listar los archivos en /app
# - Pero necesito os.listdir() o similar
# - os tiene 'o' prohibida
# - Y necesito () de todos modos
#
# ¿Puedo causar un error que revele el contenido del archivo?
# - FileNotFoundError muestra el path pero no el contenido
# - SyntaxError en import muestra el archivo pero necesito import
#
# NO HAY FORMA
#
# WAIT: Déjame pensar en el comportamiento de exec más cuidadosamente
#
# exec(code, globals, locals)
#
# Si puedo acceder a exec, ¿hay alguna forma de preparar sus argumentos
# y que se llame automáticamente?
#
# NO, necesito () para llamar
#
# ¿Puedo usar exec como un descriptor?
# class A:
#     x = exec
# A.x  # Esto retorna exec, no lo llama
#
# ¿Puedo usar exec con algún operador?
# exec - 1  # TypeError, no es válido
# exec @ something  # exec no soporta matmul
#
# NO FUNCIONA
#
# Estoy completamente atascado en el hecho de que necesito () para llamar funciones
# y () está prohibido
#
# A MENOS QUE...
#
# ¡¡¡MOMENTO!!!
#
# ¿Qué pasa si hay un BUG en cómo se parsea el código?
#
# Python tiene diferentes formas de representar ()
# Por ejemplo, en UTF-8 hay muchos caracteres que parecen paréntesis:
# - U+FF08: ＄ (fullwidth left parenthesis)
# - U+FF09: ） (fullwidth right parenthesis)
# - U+FE59: ﹙ (small left parenthesis)
# - etc.
#
# Si uso estos en el código, ¿el filtro los detecta?
# El filtro busca: '(' y ')' (ASCII 0x28 y 0x29)
# Si uso U+FF08 y U+FF09, el filtro NO los detecta
#
# Pero ¿Python los acepta?
# NO! Python solo acepta () ASCII en sintaxis
# Los caracteres Unicode fullwidth no son sintaxis válida
#
# DAMN
#
# ¿Hay algún truco de encoding?
# Por ejemplo, enviar bytes que cuando se decodifiquen sean ()?
# El input() decodifica automáticamente a UTF-8
# No hay forma de enviar bytes crudos que se interpreten diferente
#
# ESTOY REALMENTE ATASCADO
#
# Déjame revisar si hay alguna otra función builtin interesante...
#
# input() es interesante:
# - Lee del stdin
# - Retorna un string
# - No requiere argumentos (los args son opcionales)
#
# ¿Puedo llamar input sin ()? NO
#
# __import__() permite importar módulos:
# - Pero está en la lista de palabras prohibidas
# - Y necesita ()
#
# WAIT: __import__ está prohibido como keyword
# Pero ¿puedo acceder a él de otra forma?
#
# __builtins__.__import__  # __builtins__ tiene 'b' prohibida
# exec('__import__')  # exec está disponible pero necesito () y comillas
#
# NO FUNCIONA
#
# Voy a intentar una estrategia completamente diferente:
# ¿Y si hay un comportamiento especial en el exec() que puedo explotar?
#
# Por ejemplo, ¿qué pasa si el código que se ejecuta modifica el entorno
# de alguna forma que sea observable desde conexiones posteriores?
#
# NO, cada conexión es un nuevo proceso (fork en socat)
# Cada ejecución es aislada
#
# ¿Y si exploto una vulnerabilidad en Python mismo?
# Por ejemplo, un bug en el parser o en exec()?
# Esto es muy unlikely y no tengo conocimiento de tales bugs
#
# CONCLUSIÓN TEMPORAL:
# Parece imposible con las restricciones actuales
# A menos que haya algo MUY oscuro que no conozco
#
# Déjame probar algunos payloads más para ver si descubro algo...

print("=" * 60)
print("FUNCIONES DISPONIBLES Y SUS POSIBLES USOS:")
print("=" * 60)

functions = {
    'exec': 'Ejecuta código Python - NECESITA ()',
    'input': 'Lee stdin - NECESITA ()',
    'len': 'Obtiene longitud - NECESITA ()',
    'id': 'Obtiene id de objeto - NECESITA ()',
    'isinstance': 'Verifica tipo - NECESITA ()',
    'dict': 'Crea diccionario - NECESITA ()',
    'list': 'Crea lista - NECESITA ()',
    'tuple': 'Crea tupla - NECESITA ()',
    'set': 'Crea set - NECESITA ()',
    'int': 'Convierte a int - NECESITA ()',
    'ascii': 'Representación ASCII - NECESITA ()',
    'sum': 'Suma iterables - NECESITA ()',
    'max': 'Máximo - NECESITA ()',
    'min': 'Mínimo - NECESITA ()',
    'all': 'Verifica si todos True - NECESITA ()',
    'next': 'Obtiene siguiente de iterador - NECESITA ()',
    'anext': 'Async next - NECESITA ()',
    'map': 'Mapea función - NECESITA ()',
    'slice': 'Crea slice - NECESITA ()',
    'exit': 'Sale del programa - NECESITA ()',
    'Ellipsis': 'Objeto singleton ...',
    '__name__': 'Variable con nombre del módulo',
    '__spec__': 'Variable con spec del módulo',
}

for func, desc in functions.items():
    print(f"{func:15s}: {desc}")

print("=" * 60)
print("\nTODAS LAS FUNCIONES NECESITAN () PARA SER LLAMADAS")
print("Sin () no hay forma de ejecutar código en Python 3")
print("=" * 60)
