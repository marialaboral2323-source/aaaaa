#!/usr/bin/env python3
# coding: utf-8

# ¡¡¡EUREKA!!!
# Puedo usar caracteres Unicode fullwidth y cyrillic que:
# 1. NO son detectados por el filtro de letras prohibidas (que solo busca ASCII)
# 2. SON aceptados por Python como identificadores válidos
# 3. Bypassean el filtro de keywords (porque son diferentes caracteres)
#
# ESTRATEGIA:
# Usar caracteres confusables para escribir código que bypassee el filtro
#
# Confusables disponibles:
# a -> ａ (U+FF41 fullwidth) o а (U+0430 cyrillic)
# e -> ｅ (U+FF45 fullwidth) o е (U+0435 cyrillic)
# i -> ｉ (U+FF49 fullwidth) o і (U+0456 cyrillic)
# o -> ｏ (U+FF4F fullwidth) o о (U+043E cyrillic)
# b -> ｂ (U+FF42 fullwidth)
# f -> ｆ (U+FF46 fullwidth)
# h -> ｈ (U+FF48 fullwidth)
# r -> ｒ (U+FF52 fullwidth) o г (U+0433 cyrillic)
# k -> ｋ (U+FF4B fullwidth)
# v -> ｖ (U+FF56 fullwidth)
# y -> ｙ (U+FF59 fullwidth) o у (U+0443 cyrillic)
# z -> ｚ (U+FF5A fullwidth)
#
# PERO EL PROBLEMA SIGUE SIENDO:
# Necesito () para llamar funciones
# Y () está en chrban, no puedo bypassearlo con Unicode
# porque Python NO acepta fullwidth () como sintaxis
#
# WAIT WAIT WAIT:
# ¿Qué pasa si uso 'for' con caracteres confusables?
#
# for -> ｆｏｒ (fullwidth)
# Esto NO está prohibido por el filtro!
# Y Python lo acepta como keyword válido? 
# NO! Python solo acepta ASCII keywords
#
# Damn, keywords deben ser ASCII en Python
#
# ¿Qué puedo hacer entonces con los confusables?
# - Puedo escribir IDENTIFICADORES (nombres de variables/funciones)
# - NO puedo escribir KEYWORDS
#
# PERO:
# Puedo escribir identificadores de funciones builtin!
# Por ejemplo:
# - print -> ᵖｒｉｎｔ (confusable)
# - open -> ｏｐｅｎ (confusable)
# - etc.
#
# PERO el problema es que estos son identificadores DIFERENTES
# ᵖｒｉｎｔ != print
# No son la misma función!
#
# Cuando escribo ᵖｒｉｎｔ, Python busca una variable llamada ᵖｒｉｎｔ
# NO la función builtin print
#
# A MENOS QUE... yo asigne primero:
# ᵖｒｉｎｔ = print  # Pero 'print' tiene 'r' prohibida en ASCII
#
# CIRCULAR DE NUEVO
#
# PERO WAIT:
# ¿Puedo acceder a las funciones builtin de otra forma?
#
# Sí! __builtins__['print']
# Pero necesito [] que está prohibido
# Y comillas que están prohibidas
# Y __builtins__ tiene 'b' prohibida
#
# ¿Qué tal getattr(__builtins__, 'print')?
# - getattr tiene 'r' prohibida
# - __builtins__ tiene 'b' prohibida
# - Necesito () para llamar getattr
# - Necesito comillas para el string
#
# TODO ESTÁ PROHIBIDO
#
# ÚLTIMA IDEA:
# ¿Qué pasa si el uso de caracteres confusables me permite
# usar alguna keyword o función que antes no podía?
#
# Revisemos las funciones builtin que tienen letras prohibidas:
# - bool: tiene 'b' y 'o' prohibidas -> ｂｏｏｌ
# - bytearray: tiene 'b', 'y' prohibidas -> bytearray
# - bytes: tiene 'b', 'y' prohibidas
# - chr: tiene 'h', 'r' prohibidas -> ｃｈｒ  
# - complex: tiene 'o' prohibida
# - float: tiene 'f', 'o' prohibidas
# - format: tiene 'f', 'o', 'r' prohibidas
# - frozenset: muchas prohibidas
# - hash: tiene 'h' prohibida -> ｈａｓｈ
# - hex: tiene 'h' prohibida
# - iter: tiene 'r' prohibida
# - oct: tiene 'o' prohibida
# - open: tiene 'o' prohibida -> ｏｐｅｎ
# - ord: tiene 'o', 'r' prohibidas
# - print: tiene 'r' prohibida -> ᵖｒｉｎｔ
# - range: tiene 'r' prohibidas
# - repr: tiene 'r' prohibidas
# - reversed: tiene 'r', 'v' prohibidas
# - round: tiene 'o', 'r' prohibidas
# - sorted: tiene 'o', 'r' prohibidas
# - str: tiene 'r' prohibida
# - type: tiene 'y' prohibida
# - vars: tiene 'v', 'r' prohibidas
# - zip: tiene 'z' prohibida
#
# OPEN es la más importante!
# ｏｐｅｎ usando fullwidth
#
# Pero de nuevo, ｏｐｅｎ es un identificador diferente a open
# No es la función builtin
#
# A MENOS QUE...
#
# ¡¡¡MOMENTO!!!
# ¿Qué pasa con eval/exec?
#
# Puedo usar exec para ejecutar código que tenga las funciones builtin reales!
# 
# Pero:
# 1. exec necesita () para llamarlo
# 2. exec necesita un string de código, que requiere comillas
#
# AMBOS PROHIBIDOS
#
# ¿HAY ALGUNA FORMA DE CREAR UN STRING SIN COMILLAS?
#
# En Python:
# - 'string' o "string" -> necesita comillas
# - '''string''' o \"\"\"string\"\"\" -> necesita comillas
# - str() -> necesita () y 'str' tiene 'r'
# - chr() -> necesita () y 'chr' tiene 'h', 'r'
# - bytes.decode() -> necesita ()
#
# ¿Hay algún literal de string sin comillas en Python?
# NO! No existe
#
# ¿Puedo construir un string de otra forma?
# - Concatenación: 'a' + 'b' -> necesita comillas y + prohibido
# - F-strings: f'{expr}' -> necesita comillas
# - Format: '{}'.format() -> necesita comillas y ()
#
# NO HAY FORMA
#
# CONCLUSIÓN:
# Aunque los caracteres confusables Unicode me permiten bypassear
# el filtro de keywords y letras prohibidas, SIGO necesitando:
# 1. () para llamar funciones -> PROHIBIDO
# 2. Comillas para crear strings -> PROHIBIDO
# 3. [] para indexar -> PROHIBIDO
#
# Sin estos, no puedo ejecutar código útil
#
# A MENOS QUE...
#
# Estoy teniendo una idea loca:
# ¿Qué pasa si hay caracteres Unicode que Python interprete como () pero
# el filtro no detecte?
#
# Fullwidth parens: （ ）(U+FF08, U+FF09)
# Ya probé estos y Python los rechaza como SyntaxError
#
# ¿Hay otros?
# - Diferentes tipos de paréntesis Unicode
# - Caracteres que se normalicen a ()
# - etc.
#
# Voy a probar sistemáticamente...

import unicodedata

# Buscar todos los caracteres Unicode relacionados con paréntesis
paren_chars = []
for i in range(0x10000):  # BMP
    char = chr(i)
    name = unicodedata.name(char, '')
    if 'PARENTHES' in name or 'BRACKET' in name:
        paren_chars.append((char, hex(i), name))

print('Unicode parenthesis-like characters:')
for char, code, name in paren_chars[:20]:  # Primeros 20
    # Verificar si Python lo acepta
    try:
        test = f'len{char}1{chr(ord(char)+1)}'
        compile(test, '<string>', 'eval')
        status = 'ACCEPTED'
    except:
        status = 'REJECTED'
    
    # Verificar si el filtro lo detecta
    if char == '(' or char == ')':
        filtered = 'FILTERED'
    else:
        filtered = 'NOT FILTERED'
    
    print(f'  {char} {code:8s} {filtered:15s} Python: {status:10s} {name}')
