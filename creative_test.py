#!/usr/bin/env python3
# coding: utf-8

import socket
import time

host = "host8.dreamhack.games"
port = 16340

# Payloads creativos para probar
# Voy a intentar cosas que tal vez revelen información o tengan comportamiento inesperado

creative_payloads = [
    # Payload 1: Multilinea simple
    ("class A:\n pass", "Clase simple multilinea"),
    
    # Payload 2: Acceso a __name__
    ("__name__", "Acceso a __name__"),
    
    # Payload 3: Ellipsis
    ("...", "Ellipsis literal"),
    
    # Payload 4: Assignment
    ("a=__name__", "Assignment simple"),
    
    # Payload 5: Expresión matemática
    ("~-~-~-~-~-~-~-~-~-~", "Operaciones bit a bit anidadas (será muy largo pero probemos)"),
    
    # Payload 6: Del
    ("del __name__", "Intentar eliminar __name__"),
    
    # Payload 7: Annotation
    ("a:exec=...", "Variable annotation con exec"),
    
    # Payload 8: Class con annotation
    ("class A:\n a:exec=...", "Clase con annotation"),
    
    # Payload 9: Unicode confusables para 'print'
    ("ᵖʳⁱⁿᵗ", "Print con caracteres Unicode"),
    
    # Payload 10: Fullwidth 'open'
    ("ｏｐｅｎ", "Open con fullwidth"),
    
    # Payload 11: Assignment de exec
    ("a=exec", "Asignar exec a variable"),
    
    # Payload 12: Class con exec como atributo
    ("class A:\n e=exec", "Clase con exec como atributo"),
    
    # Payload 13: Multiple assignments
    ("a=...;a", "Assignment y referencia"),
    
    # Payload 14: Is operator
    ("... is ...", "Comparación de Ellipsis"),
    
    # Payload 15: In operator  
    ("a in __name__", "Membresía (causará error)"),
    
    # Payload 16: Operadores de comparación encadenados
    ("...>...<...", "Comparaciones encadenadas"),
]

def send_payload(payload, description):
    print(f"\n{'='*70}")
    print(f"Payload: {description}")
    print(f"Code: {repr(payload)}")
    print(f"Length: {len(payload)}")
    print('-'*70)
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((host, port))
        
        # Enviar payload + línea vacía
        s.sendall((payload + "\n\n").encode('utf-8'))
        
        # Recibir respuesta
        response = b""
        while True:
            try:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk
            except socket.timeout:
                break
        
        s.close()
        
        result = response.decode('utf-8', errors='ignore')
        print(f"Response:\n{result}")
        print('='*70)
        
        return result
    except Exception as e:
        print(f"Error: {e}")
        print('='*70)
        return None

# Ejecutar payloads
results = []
for payload, desc in creative_payloads:
    result = send_payload(payload, desc)
    results.append((payload, desc, result))
    time.sleep(0.5)  # Pequeña pausa entre requests

print("\n\n" + "="*70)
print("RESUMEN DE RESULTADOS:")
print("="*70)
for payload, desc, result in results:
    status = "OK" if result and "ok" in result.lower() else "FAILED"
    print(f"{status:10s} {desc:50s}")
