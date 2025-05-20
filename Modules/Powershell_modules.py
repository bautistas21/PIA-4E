import subprocess
import argparse
import sys
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
REPORTS_DIR = os.path.join(BASE_DIR, "Reports")
REPORT_FILE = os.path.join(REPORTS_DIR, "Powershell_Reports.txt")

os.makedirs(REPORTS_DIR, exist_ok=True)

def write_report(content, function_name):
    """Escribe los resultados en el archivo de reportes"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(REPORT_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n--- Reporte generado el {timestamp} ---")
        f.write(f"\nFuncion ejecutada: {function_name}\n")
        f.write(content)
        f.write("\n" "**************************************************" "\n")
    print(f"\nReporte guardado en: {REPORT_FILE}")

def execute_powershell(command):
    """Ejecuta un comando PowerShell y muestra el resultado"""
    try:
        result = subprocess.run(["powershell", "-Command", command], 
                              capture_output=True, 
                              text=True, 
                              encoding='utf-8')
        if result.returncode != 0:
            print(f"\nError en PowerShell: {result.stderr}")
            return None
        return result.stdout
    except Exception as e:
        print(f"\nError al ejecutar PowerShell: {str(e)}")
        return None
    

def show_admin_users():
    """Muestra los usuarios del grupo Administradores"""
    command = """
    Get-LocalGroupMember -Group "Administradores" | 
    Select-Object Name, 
        @{Name="Origen de la cuenta"; Expression={$_.PrincipalSource}} | 
    Format-Table -AutoSize
    """
    result = execute_powershell(command)
    if result:
        report = "\n--- Usuarios Administradores ---\n" + result
        write_report(report, "show_admin_users")

def show_inactive_users():
    """Muestra usuarios inactivos según el período configurado"""
    inactive_days = 90
    command = f"""
    $DaysInactive={inactive_days}
    Get-LocalUser|ForEach-Object {{
        $LastLogon=if ($_.LastLogon) {{ $_.LastLogon }} else {{ [DateTime]::MinValue }}
        if ((Get-Date) - $LastLogon -gt (New-TimeSpan -Days $DaysInactive)) {{
            $_ | Select-Object Name, LastLogon | Format-Table -AutoSize
        }}
    }}
    """
    result = execute_powershell(command)
    if result:
        report = f"\n--- Usuarios inactivos (> {inactive_days} dias) ---\n" + (result if result.strip() else "No hay usuarios inactivos")
        write_report(report, "show_inactive_users")

def option1_menu():
    parser = argparse.ArgumentParser(description='Muestra los usuarios administradores o inactivos')
    parser.add_argument('-op', '--option', type=int, help="Contiene la opción de la tarea del menú principal")
    args = parser.parse_args()
    while True:
        print("\n --- Usuarios Administradores o Inactivos ---")
        print(" ------------ Funciones de Powershell ------------ ")
        print("1. Mostrar usuarios administradores")
        print("2. Mostrar usuarios inactivos")
        print("3. Volver al menú principal")
        option = input("Seleccione una opción (1-3): ")
        
        if option == '1':
            show_admin_users()
        elif option == '2':
            show_inactive_users()
        elif option == '3' and args.option is None:
            break
        elif option == '3' and args.option == 1:
            sys.exit()
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")
        
        input("\nPresione Enter para continuar...")


def option2_menu():
    parser = argparse.ArgumentParser(description='Muestra los archivos ocultos de una carpeta')
    parser.add_argument('-op', '--option', type=int)
    parser.add_argument('-dir', '--directory', help="Este parámetro sirve para agregar la dirección de la carpeta, en caso que desees utilizar la opción 2 del menú principal para ver los archivos ocultos de una carpeta")
    args = parser.parse_args()
    """Busca archivos ocultos en una carpeta especificada"""
    print("\n --- Buscar archivos ocultos ---")
    if args.directory is not None:
        path = args.directory
    else:
        path = input("\nIngrese la ruta de la carpeta a analizar: ")
    command = f"""
        function Get-HiddenFiles {{
            param([Parameter(Mandatory=$true)][string]$FolderPath)

            try {{
                if (-not (Test-Path -Path $FolderPath -PathType Container)) {{
                    Write-Host "La carpeta especificada no existe o no es válida."
                    return
                }}

                $hiddenFiles = Get-ChildItem -Path $FolderPath -Force -Recurse -ErrorAction SilentlyContinue | 
                            Where-Object {{ $_.Attributes -match 'Hidden' }}

                if ($hiddenFiles) {{
                    $hiddenFiles | Select-Object FullName, Attributes, LastWriteTime | Format-Table -AutoSize
                    Write-Host "`nTotal de archivos ocultos en la carpeta: $($hiddenFiles.Count)" 
                }} else {{
                    Write-Host "No se encontraron archivos ocultos en la carpeta especificada." 
                }}
            }}
            catch {{
                Write-Host "Error al buscar archivos ocultos: $_" 
            }}
        }}
        
        Get-HiddenFiles -FolderPath "{path}"
        """
    result = execute_powershell(command)
    if result:
        report = "\n--- Archivos Ocultos ---\n" + f"Directorio analizado: {path}\n" + result
        write_report(report, "menu_option2")