#!/usr/bin/env python3

import subprocess
import os
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
REPORTS_DIR = BASE_DIR / "Reports"
REPORT_FILE = REPORTS_DIR / "Bash_Reports.txt"

def check_nmap_installed():
    """Verifica si nmap está instalado en el sistema"""
    try:
        subprocess.run(
            ['nmap', '--version'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def show_installation_help():
    """Muestra instrucciones para instalar nmap"""
    print("\nnmap no está instalado. Instalación:")
    print("\nDebian/Ubuntu: sudo apt install nmap")
    print("RHEL/CentOS:   sudo yum install nmap")
    print("Arch:          sudo pacman -S nmap")
    print("macOS:         brew install nmap")

def create_reports_dir():
    """Crea el directorio para guardar reportes si no existe"""
    REPORTS_DIR.mkdir(exist_ok=True)

def write_scan_report(content, scan_type):
    """Escribe los resultados en el archivo de reportes"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(REPORT_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n=== {scan_type} Scan - {timestamp} ===\n")
        f.write(content)
        f.write("\n" "**************************************************" "\n")
    print(f"\nReporte guardado en: {REPORT_FILE}")

def scan_tcp_ports(ip=None, port_range=None):
    """
    Escanea puertos TCP usando nmap
    
    Args:
        ip: Dirección IP o dominio a escanear
        port_range: Rango de puertos (ej. '1-1000')
    """
    if not check_nmap_installed():
        print("Error: nmap no está instalado.")
        show_installation_help()
        return

    if not ip:
        ip = input("Ingrese la IP o dominio a escanear: ")
    if not port_range:
        port_range = input("Ingrese el rango de puertos (ej. 1-1000): ")

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    try:

        result = subprocess.run(
            ['nmap', '-p', port_range, '-T4', ip],
            capture_output=True,
            text=True,
            check=True
        )


        report_content = f"IP/Dominio: {ip}\n"
        report_content += f"Rango de puertos: {port_range}\n"
        report_content += "--------------------------------\n"
        report_content += result.stdout


        lines = result.stdout.split('\n')
        open_ports = [line.split('/')[0] for line in lines if '/tcp' in line and 'open' in line]
        closed_ports = [line.split('/')[0] for line in lines if '/tcp' in line and 'closed' in line]


        report_content += "\nResumen:\n"
        if open_ports:
            report_content += f"Puertos TCP abiertos: {', '.join(open_ports)}\n"
        else:
            report_content += "No se encontraron puertos TCP abiertos\n"

        if closed_ports:
            report_content += f"Puertos TCP cerrados: {', '.join(closed_ports)}\n"
        else:
            report_content += "No se encontraron puertos TCP cerrados\n"

        write_scan_report(report_content, "TCP")

    except subprocess.CalledProcessError as e:
        error_msg = f"Error en el escaneo TCP: {e.stderr}"
        write_scan_report(error_msg, "TCP Error")
    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        write_scan_report(error_msg, "TCP Error")

def scan_udp_ports(ip=None, port_range=None):
    """
    Escanea puertos UDP usando nmap
    
    Args:
        ip: Dirección IP o dominio a escanear
        port_range: Rango de puertos (ej. '1-1000')
    """
    if not check_nmap_installed():
        print("Error: nmap no está instalado.")
        show_installation_help()
        return

    if not ip:
        ip = input("Ingrese la IP o dominio a escanear: ")
    if not port_range:
        port_range = input("Ingrese el rango de puertos UDP (ej. 1-1000): ")

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    try:

        result = subprocess.run(
            ['nmap', '-sU', '-p', port_range, '-T4', ip],
            capture_output=True,
            text=True,
            check=True
        )


        report_content = f"IP/Dominio: {ip}\n"
        report_content += f"Rango de puertos UDP: {port_range}\n"
        report_content += "--------------------------------\n"
        report_content += result.stdout


        lines = result.stdout.split('\n')
        open_ports = [line.split('/')[0] for line in lines if '/udp' in line and 'open' in line]
        closed_ports = [line.split('/')[0] for line in lines if '/udp' in line and 'closed' in line]


        report_content += "\nResumen:\n"
        if open_ports:
            report_content += f"Puertos UDP abiertos: {', '.join(open_ports)}\n"
        else:
            report_content += "No se encontraron puertos UDP abiertos\n"

        if closed_ports:
            report_content += f"Puertos UDP cerrados: {', '.join(closed_ports)}\n"
        else:
            report_content += "No se encontraron puertos UDP cerrados\n"

        write_scan_report(report_content, "UDP")

    except subprocess.CalledProcessError as e:
        error_msg = f"Error en el escaneo UDP: {e.stderr}"
        write_scan_report(error_msg, "UDP Error")
    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        write_scan_report(error_msg, "UDP Error")

def option6_menu():
    """Menú interactivo para el escaneo de puertos"""
    create_reports_dir()
    
    while True:
        print("\n=== MENÚ ESCANEO DE PUERTOS ===")
        print("1. Escanear puertos TCP")
        print("2. Escanear puertos UDP")
        print("3. Salir")
        
        option = input("Seleccione una opción (1-3): ")
        
        if option == "1":
            scan_tcp_ports()
        elif option == "2":
            scan_udp_ports()
        elif option == "3":
            print("Saliendo...")
            break
        else:
            print("Opción no válida")