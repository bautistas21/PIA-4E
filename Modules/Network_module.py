#!/usr/bin/env python3

import subprocess
import time
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
REPORTS_DIR = BASE_DIR / "Reports"
REPORT_FILE = REPORTS_DIR / "Bash_Reports.txt"

def check_ifstat_installed():
    """Verifica si ifstat está instalado en el sistema"""
    try:
        subprocess.run(
            ['ifstat', '-h'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def show_installation_help():
    """Muestra instrucciones para instalar ifstat"""
    print("\nifstat no está instalado. Instalación:")
    print("\nDebian/Ubuntu: sudo apt install ifstat")
    print("RHEL/CentOS:   sudo yum install ifstat")
    print("Arch:          sudo pacman -S ifstat")

def create_reports_dir():
    """Crea el directorio para guardar reportes si no existe"""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def write_network_report(content, monitor_type):
    """Escribe los resultados en el archivo de reportes"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(REPORT_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n=== Monitoreo de Red - {timestamp} ===\n")
        f.write(f"Tipo: {monitor_type}\n")
        f.write(content)
        f.write("\n" "**************************************************" "\n")
    print(f"\nReporte guardado en: {REPORT_FILE}")

def live_monitoring():
    """Monitorea la red en tiempo real hasta presionar Enter"""
    if not check_ifstat_installed():
        print("Error: ifstat no está instalado.")
        show_installation_help()
        return

    try:
        process = subprocess.Popen(['ifstat'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("\nMonitoreo en vivo (presiona Enter para detener)...")
        input()
        
        process.terminate()
        try:
            stdout, stderr = process.communicate(timeout=5)
            report_content = stdout.decode('utf-8') if stdout else "No se obtuvieron datos"
            write_network_report(report_content, "Monitoreo en vivo")
        except subprocess.TimeoutExpired:
            process.kill()
            write_network_report("El monitoreo fue terminado forzosamente", "Monitoreo en vivo (interrumpido)")
            
    except KeyboardInterrupt:
        write_network_report("Monitoreo cancelado por el usuario", "Monitoreo en vivo (cancelado)")
    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        write_network_report(error_msg, "Monitoreo en vivo (error)")

def fixed_iterations_monitoring(iterations, interval=5):
    """
    Monitorea la red un número específico de veces
    
    Args:
        iterations: Número de veces a monitorear
        interval: Segundos entre mediciones (default: 5)
    """
    if not check_ifstat_installed():
        print("Error: ifstat no está instalado.")
        show_installation_help()
        return

    try:
        report_content = f"Configuración:\nIteraciones: {iterations}\nIntervalo: {interval} segundos\n\n"
        
        for i in range(1, iterations + 1):
            result = subprocess.run(
                ['ifstat', str(interval), '1'], 
                capture_output=True, 
                text=True,
                check=True
            )
            
            report_content += f"\nIteración {i}/{iterations}:\n"
            report_content += result.stdout
            
            if i < iterations:
                time.sleep(interval)
        
        write_network_report(report_content, f"Monitoreo por iteraciones ({iterations}x)")

    except subprocess.CalledProcessError as e:
        error_msg = f"Error al ejecutar ifstat: {e.stderr}"
        write_network_report(error_msg, "Monitoreo por iteraciones (error)")
    except KeyboardInterrupt:
        write_network_report("Monitoreo interrumpido por el usuario", "Monitoreo por iteraciones (interrumpido)")
    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        write_network_report(error_msg, "Monitoreo por iteraciones (error)")

def option5_menu():
    """Muestra el menú interactivo de opciones"""
    create_reports_dir()
    
    while True:
        print("\n --- Monitor de Red ---")
        print("1. Monitoreo en vivo")
        print("2. Monitoreo por iteraciones")
        print("3. Salir")

        option = input("Seleccione una opción (1-3): ")
        
        if option == "1":
            live_monitoring()
            break
        elif option == "2":
            try:
                iterations = int(input("Iteraciones a monitorear: "))
                seconds = int(input("Intervalo en segundos [5]: ") or 5)
                fixed_iterations_monitoring(iterations, seconds)
                break
            except ValueError:
                print("Error: Ingrese números válidos")
        elif option == "3":
            print("Saliendo...")
            break
        else:
            print("Opción no válida")