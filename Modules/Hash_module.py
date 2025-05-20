import hashlib
import requests
import time
import os
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
REPORTS_DIR = BASE_DIR / "Reports"
REPORT_FILE = REPORTS_DIR / "Python_Reports.txt"

REPORTS_DIR.mkdir(exist_ok=True)

def write_report(content, function_name):
    """Escribe los resultados en el archivo de reportes"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(REPORT_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n--- Reporte generado el {timestamp} ---")
        f.write(f"\nFunción ejecutada: {function_name}\n")
        f.write(content)
        f.write("\n" "**************************************************" "\n")
    print(f"\nReporte guardado en: {REPORT_FILE}")


def generate_hash(text, algorithm='sha256'):
    """Genera el hash de un texto usando el algoritmo especificado."""
    hasher = hashlib.new(algorithm)
    hasher.update(text.encode('utf-8'))
    return hasher.hexdigest()

def save_hash(hash_value, original_text, filename="hashes.txt"):
    """
    Guarda el hash y texto original en una wordlist personalizada.
    Si el archivo no existe, lo crea en la carpeta 'Diccionarios'.
    """
    dictionaries_dir = BASE_DIR / "Diccionarios"
    dictionaries_dir.mkdir(exist_ok=True)
    
    file_path = dictionaries_dir / filename
    
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(f"{hash_value}:{original_text}\n")
    
    report_content = f"Hash generado y guardado en: {file_path}\n"
    report_content += f"Texto original: {original_text}\n"
    report_content += f"Hash: {hash_value}"
    write_report(report_content, "save_hash")

def verify_hash(text, target_hash, algorithm='sha256'):
    """Verifica si el texto coincide con el hash proporcionado."""
    return generate_hash(text, algorithm) == target_hash

def search_hash(target_hash, wordlist_path, algorithm='sha256'):
    """Intenta descifrar un hash usando una wordlist."""
    if not os.path.exists(wordlist_path):
        print("Archivo de wordlist no encontrado.")
        return None
    
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            if ':' in line:
                stored_hash, text = line.strip().split(':', 1)
                if stored_hash == target_hash:
                    report_content = f"Hash encontrado en el diccionario\n"
                    report_content += f"Hash buscado: {target_hash}\n"
                    report_content += f"Texto encontrado: {text}\n"
                    report_content += f"Archivo diccionario: {wordlist_path}"
                    write_report(report_content, "search_hash")
                    return text
            else:
                word = line.strip()
                if verify_hash(word, target_hash, algorithm):
                    report_content = f"Hash encontrado en el diccionario\n"
                    report_content += f"Hash buscado: {target_hash}\n"
                    report_content += f"Texto encontrado: {word}\n"
                    report_content += f"Archivo diccionario: {wordlist_path}"
                    write_report(report_content, "search_hash")
                    return word
    
    report_content = f"Hash no encontrado en el diccionario\n"
    report_content += f"Hash buscado: {target_hash}\n"
    report_content += f"Archivo diccionario: {wordlist_path}"
    write_report(report_content, "search_hash")
    return None

def show_hashes(filename="hashes.txt", max_hashes=None):
    """Muestra los hashes que hay en el diccionario"""
    file_path = BASE_DIR / "Diccionarios" / filename
    
    if not file_path.exists():
        print(f"\n El archivo {file_path} no existe.")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if not lines:
        print("\n El archivo no contiene hashes.")
        return
    
    total = len(lines)
    show_all = True
    
    if max_hashes is None and total > 50:
        answer = input(f"\n Quieres mostrar todos los {total} hashes? (s/n): ").lower()
        if answer != 's':
            max_hashes = 50
            show_all = False


    report_content = f"\n--- Hashes almacenados ({total} registros) ---\n"
    report_content += f"Archivo diccionario: {file_path}\n"
    
    for i, line in enumerate(lines[:max_hashes], 1):
        if ':' in line:
            hash_val, text = line.split(':', 1)
            report_content += f"{i}. {hash_val} : {text}\n"
        else:
            report_content += f"{i}. {line}\n"
    
    if not show_all and max_hashes < total:
        report_content += f"\n[Mostrando {max_hashes} de {total} hashes.]\n"
    
    write_report(report_content, "show_hashes")
    

    print(f"\n--- Hashes almacenados ({total} registros) ---\n")
    for i, line in enumerate(lines[:max_hashes], 1):
        if ':' in line:
            hash_val, text = line.split(':', 1)
            print(f"{i}. {hash_val} : {text}")
        else:
            print(f"{i}. {line}")

    if not show_all and max_hashes < total:
        print(f"\n[Mostrando {max_hashes} de {total} hashes.")

def option3_menu():
    print("--- Generar o Buscar Hashes ---")
    print("""\n Opciones:
            1- Generar Hash
            2- Consultar Diccionario  
            3- Buscar Hash dentro de un diccionario
            """)
    while True:
        try:
            option = int(input("Ingresa la opción a realizar: "))
            if 1 <= option <= 3:
                break
        except:
            print("Opción no válida")
    
    if option == 1:
        text = input("Ingrese el texto a hashear: ")
        algorithm = input("Algoritmo (md5/sha1/sha256/sha512): ").lower() or 'sha256'
        hash_value = generate_hash(text, algorithm)
        print(f"\nHash ({algorithm.upper()}): {hash_value}")
        save = input("\n ¿Quieres guardar el hash en un diccionario? (s/n): ").lower()
        if save == 's':
            dictionary = input("Nombre del archivo con .txt: ") or "hashes.txt"
            save_hash(hash_value, text, dictionary)
            print("Hash guardado con éxito")
            input("Presiona enter para continuar\n")
        
    elif option == 2:
        name = input("Ingresa el nombre del diccionario: ")
        count = int(input("Ingresa cuántos hashes quieres ver: "))
        show_hashes(name, count)
        input("Presiona enter para continuar\n")
        
    elif option == 3:
        dictionary = input("Ruta completa a el diccionario (con txt): ")
        hash_value = input("Ingrese el hash a buscar: ")
        algorithm = input("Algoritmo (md5/sha1/sha256/sha512): ").lower() or 'sha256'
        found_text = search_hash(hash_value, dictionary, algorithm)
        if found_text:
            print(f"\nContraseña encontrada: '{found_text}'")
        else:
            print("\nContraseña no encontrada en el diccionario.")
        input("Presiona enter para continuar\n")