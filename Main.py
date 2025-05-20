import platform
import sys
import argparse
from time import sleep
from Modules.Powershell_modules import option1_menu,option2_menu
from Modules.Hash_module import  option3_menu
from Modules.HIBPwnd_module import option4_menu
from Modules.Network_module import option5_menu
from Modules.Ports_module import option6_menu

def os():
    """
    Identifica el sistema operativo actual y devuelve 'Windows' o 'Linux'.
    
    Returns:
        str: 'Windows' si el SO es Windows, 'Linux' si es Linux, o 'Desconocido' para otros sistemas.
    """
    sistema = platform.system().lower()
    
    if sistema == 'windows':
        print(" ------------ NOTA IMPORTANTE ------------")
        print("Tu sistema operativo es windows, por lo que las opciones 5 y 6 no funcionarán")
        print(" ------------------------------------")
        return 'windows'
    elif sistema == 'linux':
        print(" ------------ NOTA IMPORTANTE ------------")
        print("Tu sistema operativo es linux, por lo que las opciones 1 y 2 no funcionarán")
        print(" ------------------------------------")
        return 'linux'
    else:
        print("No se ha podido identificar el sistema operativo")
        return None

parser = argparse.ArgumentParser(description='Menú principal que contiene todas las tareas que peuden realizarse con los distintos módulos')
parser.add_argument('-op', '--option', type=int, help="""Este script cuenta con varias opciones: 
                        1- Usuarios Administradores e Inactivos (Powershell)
                        2- Buscar archivos ocultos (Powershell)
                        3- Generar Hashes/Buscar hashes en diccionarios (Python)
                        4- Buscar Hash en HaveIBeenPwnd (Python) (Relacionada con opción 3)
                        5- Monitorear la red (Bash)
                        6- Escanear Puertos (Bash)
                        7- Salir""")
parser.add_argument('-dir', '--directory', help="Este parámetro sirve para agregar la dirección de la carpeta, en caso que desees utilizar la opción 2 del menú principal para ver los archivos ocultos de una carpeta, por ejemplo "'python Main.py -op 2 -dir "C:\Program Files"')
args = parser.parse_args()

#Execution Examples with arguments:
#   python Main.py -op 1
#   python Main.py -op 2 -dir "C:\Program Files"

if args.option is not None:
    if 1 <= args.option <= 7:
        if args.option == 1:
            option1_menu()
        elif args.option == 2:
            option2_menu()
        elif args.option == 3:
            option3_menu()
            pass
        elif args.option == 4:
            option4_menu()
            pass
        elif args.option == 5:
            option5_menu()
            pass
        elif args.option == 6:
            option6_menu()
        elif args.option == 7:
            print("\nSaliendo del programa...")
            sleep(1)
            sys.exit(0)
    else:
        print("Error: La opción debe ser un número entre 1 y 7")
        sys.exit(1)
else:
    while True:
            os()
            print(" ------------ MENÚ PRINCIPAL ------------ ")
            print("1. Usuarios Administradores e Inactivos (Powershell)")
            print("2. Buscar archivos ocultos (Powershell)")
            print("3. Generar Hashes/Buscar hashes en diccionarios (Python)")
            print("4. Buscar Hash en HaveIBeenPwnd (Python) (Relacionada con opción 3)" )#
            print("5. Monitorear la red (Bash)")
            print("6. Escanear Puertos (Bash)")
            print("7. Salir \n")
            opcion = input("Seleccione una opción (1-7): ")
            
            if opcion == '1':
                if(os()!='windows'):
                    print("No se puede ejecutar debido a que el sistema operativo no es windows")
                else:
                    option1_menu()
            
            elif opcion == '2':
                if(os()!='windows'):
                    print("No se puede ejecutar debido a que el sistema operativo no es windows")
                else:
                    option2_menu()
            
            elif opcion == '3':
                option3_menu()

            elif opcion == '4':
                option4_menu()
                
            elif opcion == '5':
                if(os()!='linux'):
                    print("No se puede ejecutar debido a que el sistema operativo no es linux")
                else:
                    option5_menu()
            
            elif opcion == '6':
                if(os()!='linux'):
                    print("No se puede ejecutar debido a que el sistema operativo no es linux")
                else:
                    option6_menu()
            
            elif opcion == '7':
                print("\nSaliendo del programa...")
                sleep(1)
                break

            else:
                print("\nOpción no válida. Intente nuevamente.")
            
            input("\nPresione Enter para continuar...")
