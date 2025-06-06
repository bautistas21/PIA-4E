# Descripción
Este es el entregable final de la materia de Programación para ciberseguridad, en el cual tuvimos presentes los objetivos de integrar los códigos y módulos que se habían realizado anteriormente, desarrollando así las habilidades en python, powershell y bash.
Como lenguaje principal se uso Python, donde realizamos un menú principal el cual lleva por nombre Main.py, en este script podemos encontrar 6 tareas integradas, siendo 2 de un mismo lenguaje.
Las tareas que se incluyeron fueron las siguientes:
- 1- Usuarios Administradores e Inactivos (Powershell)
- 2- Buscar archivos ocultos (Powershell)
- 3- Generar Hashes/Buscar hashes en diccionarios (Python)
- 4- Buscar Hash en HaveIBeenPwnd (Python) (Relacionada con opción 3)
- 5- Monitorear la red (Bash)
- 6- Escanear Puertos (Bash)

Dada la naturaleza de Powershell y Bash, las cuales tienen un uso exlcusivo en distintos sistemas operativos, en caso de estar ejecutando el script desde un equipo que cuenta con Windows como su sistema operativo, se mostrará un mensaje donde se indicará que las tareas 5 y 6 no estáran disponibles ya que no son compatibles, y lo mismosi estás en alguna distribución de Linux.

## Uso de Main.py
Para utilizar el script que contine le menú principal es muy sencillo, solamente se tiene que ejecutar directo desde el IDE de su agrado.
A continuación aparecerá el mensaje de la compatibilidad con el sistema operativo del cual previamente se habló, seguido de esto aparece el menú con las tareas posibles a realizar, solo es cuestión de seleccionar la deseado ingresando el número que le corresponde e iniciará su función. Cabe aclarar que los resultados de las tareas no se verán en la terminal, si no que estos serán guardados en una carpeta llamada "Reports", el reporte en el que se guardará la tarea ejecutada dependerá del ámbito al que pertenece, es decir, Powershell, Python o Bash.
## Opciones
### **1- Usuarios Administradores e Inactivos (Powershell)**
Como su nombre lo dice, nos permitirá visualizar los usuarios del dispositivo que están definidos como administradores, o, también podremos elegir ver los usuarios que an estado inactivos en un plazo de 90 días, junto a la fecha en la que el usuario inició sesión por última vez.
###  **2- Buscar archivos ocultos (Powershell)**
Esta tarea buscará los archivos ocultos que estén contenidos en alguna carpeta, la cual tendrás que ingresar su dirección.
### **3- Generar Hashes/Buscar hashes en diccionarios (Python)**
Esta opción te mostrará otro menú, en donde podrás esocger entre generar un hash de algún texto, para después decidir si guardarlo en algún diciconario o no, otra opción es consultar el diccionario, donde escribirás el nombre de algún diccionario incluyendo su extensión .txt, este dccionario necesita estar ubicado en la carpeta llamada Diccionarios, de lo contrario no lo encontrará.
### **4- Buscar Hash en HaveIBeenPwnd (Python) (Relacionada con opción 3)**
Te permite buscar algún hash en las brechas conocidas por HaveIBeenPwned, el hash puede ser personalizado, es decir tú ingresas un texto para que este después sea hasheado, o también puedes seleccionar alguno de los hashes que se encuentran almacenados en los diccionarios.
### **5- Monitorear la red (Bash)**
Esta tarea realiza un monitoreo de la red, se estará actalizando en vivo, o también puedes seleccionar cuántas veces se realizará el monitoreo.
### **6- Escanear Puertos (Bash)**
La opción 6 realiza une escaneo de puertos, este puede ser tanto un escaneo de puertos UDP, o también TCP, únicamente necesitas ingresas la dirección IP o dominio a escanear.

## Parámetros
Main.py se puede utilizar indicando parámetros de entrada, los parámetros disponibles son los siguientes:
- -op --opción: Este parámetro sirve para indicar la opción que deseas realizar del menú principal. así no te verás en la necesidad de ejecutar el script completo para ejecutar una única tarea.
- -dir --directory: Este parámetro se utiliza para que en caso de selecciónar la opción 2 del menú principal (Ver archivos ocultos de una carpeta), puedas ingresar la ruta de la carpeta y así sea más ágil el proceso.
### Ejemplo de ejecución con parámetros
```
python Main.py -op 2 -dir "C:\Program Files"
```
## Reportes
Todas las salidas al momento de la ejecución del script, se irán a un reporte dependiendo de qué tarea haya sido la ejecutada, en donde se irán añadiendo las salidas de las futuras ejecuciones del script. Estos resportes se guardarán dentro de la carpeta llamada Reports y únicamente estarán los siguientes 3 reportes:
- Python_Reports.txt
- Powershell_Reports.txx
- Bash_Reports.txt
