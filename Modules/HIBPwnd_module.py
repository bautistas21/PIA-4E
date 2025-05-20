import hashlib
import time
import requests
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

def check_password_breach(password):
    """Consulta en HIBP si el hash aparece en algún breach"""
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    
    try:
        response = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefix}",
            headers={"User-Agent": "MyPasswordChecker"}
        )
        response.raise_for_status()
        
        for line in response.text.splitlines():
            if line.split(":")[0] == suffix:
                return int(line.split(":")[1])
        return 0
    
    except requests.exceptions.RequestException as e:
        print(f"Error al consultar HIBP: {e}")
        return -1
    finally:
        time.sleep(1.6) 

def option4_menu():    
    print(" --- Buscar Hashes en HaveIBeenPwnd --- ")
    print("\nOpciones de búsqueda:")
    print("1. Buscar hash de un diccionario")
    print("2. Buscar hash de una contraseña manual")
        
    while True:
        try:
            option = int(input("\nSeleccione una opción (1-2): "))
            if option in [1, 2]:
                break
            else:
                print("Opción no válida. Intente nuevamente.")
        except ValueError:
            print("Por favor ingrese un número válido.")
        
    if option == 1:
        dict_name = input("\nIngrese el nombre del diccionario (ej. hashes.txt): ")
        try:
            with open(BASE_DIR / "Diccionarios" / dict_name, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            
            if not lines:
                report = "El diccionario está vacío o no contiene hashes válidos."
                write_report(report, "password_breach_menu")
            else:
                selected_hash = None
                print("\nSeleccione el hash a verificar:")
                for i, line in enumerate(lines[:10], 1):
                    print(f"{i}. {line.split(':')[0] if ':' in line else line}")
                    
                while True:
                    try:
                        selection = int(input("\nIngrese el número del hash a verificar (0 para cancelar): "))
                        if 0 <= selection <= min(10, len(lines)):
                            break
                        else:
                            print("Número fuera de rango.")
                    except ValueError:
                        print("Ingrese un número válido.")
                    
                if selection != 0:
                    selected_hash = lines[selection-1].split(':')[0] if ':' in lines[selection-1] else lines[selection-1]
                    breaches = check_password_breach(selected_hash)
                    
                    report = f"Hash verificado: {selected_hash}\n"
                    if breaches > 0:
                        report += f"Esta contraseña apareció en {breaches} brechas de datos."
                    elif breaches == 0:
                        report += "Contraseña no encontrada en brechas conocidas."
                    else:
                        report += "No se pudo verificar (error de conexión)."
                    
                    write_report(report, "password_breach_menu")
            
        except FileNotFoundError:
            report = f"El archivo 'Diccionarios/{dict_name}' no existe."
            write_report(report, "password_breach_menu")
        
    elif option == 2:
        password = input("\nIngrese la contraseña a verificar: ")
        if password.strip():
            breaches = check_password_breach(password)
            
            report = f"Contraseña verificada: {password}\n"
            if breaches > 0:
                report += f"Esta contraseña apareció en {breaches} brechas de datos."
            elif breaches == 0:
                report += "Contraseña no encontrada en brechas conocidas."
            else:
                report += "No se pudo verificar (error de conexión)."
            
            write_report(report, "password_breach_menu")
        else:
            report = "No se ingresó ninguna contraseña."
            write_report(report, "password_breach_menu")
    
    input("\nPresione Enter para continuar...")