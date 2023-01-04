# Docker y desarrollo en contenedores

En ciencia los resultados deben ser transparentes y reproducibles. Por ello, cuando realizamos cálculos numéricos o simulaciones, es importante que nuestros códigos sean libres y públicos, para que cualquiera pueda ejecutarlos y comprobar su veracidad. Pero en general nuestros códigos no existen en un vacío, sino que dependen de códigos escritos por otras personas, y para asegurar la reproducibilidad, deberán ser ejecutados con la misma versión. Para esto son útiles herramientas como `poetry` para gestionar las dependencias de nuestro proyecto. Sin embargo, esto no es suficiente: los repositorios de paquetes eventualmente van eliminando versiones antiguas, e incluso las versiones de Python dejan de estar soportadas en sistemas operativos nuevos (por ejemplo, Python 3.7 solo estará soportado hasta junio de 2023).

Para evitar este problema se pueden usar los contenedores de Docker. Un contenedor encapsula nuestro código y todas sus dependencias en un entorno inmutable, de modo que siempre estará listo para ejecutarse, independientemente del sistema operativo exterior. Los contenedores funcionan en cierta medida como pequeños sistemas operativos que se ejecutan dentro del sistema. En Linux, esto es bastante directo, ya que el kernel (el componente del sistema operativo que interacciona directamente con el hardware) permite la ejecución de grupos de procesos ("namespaces") aislados entre sí, lo que simula el efecto de ejecutar varios sistemas operativos con un único kernel. La arquitectura de Windows y MacOS no permite esto: en estos sistemas operativos, para usar docker es necesario tener un kernel de Linux a través de una máquina virtual.

## WSL2

[Nota: No he usado nunca WSL2 o la versión de Docker para Windows. Espero que funcione...]

Windows 10 y Windows 11 vienen con una máquina virtual optimizada para el kernel de Linux, WSL2 (Windows Subsytem for Linux). Para activarla, abre Powershell y ejecuta

```powershell
wsl --install
```

Este comando activa WSL e instala una distribución de Linux llamada Ubuntu. Reinicia el ordenador, vuelve a abrir Powershell y ejecuta `wsl`. Esto entrará en (la versión de línea de comandos de) Ubuntu. La primera vez tendrás que crear un nombre de usuario y contraseña. Al introducir la contraseña, no aparecerá ningún caracter en la pantalla, así que asegúrate de teclear bien.

### Comandos básicos de Linux

En la consola, el principio de cada nueva línea aparecerán tres informaciones: el nombre de usuario, seguida de `@`, el identificador del sistema que está ejecutándose, seguido de `:`, y el directorio actual, seguido de `$`. Al abrir `wsl` te encontrarás en el directorio `~`, que es la abreviación de `/home/nombre-de-usuario`, el directorio `HOME`.

* Puedes ver la ruta completa del directorio actual con el comando

```bash
pwd
```

* Para ver los contenidos del directorio actual usa el comando

```bash
ls -al
```

  (o también puedes abrirlo en el explorador de Windows con el comando `explorer.exe .`). En cualquier directorio, las dos primeras líneas contendrán `.` y `..`, que se refieren al directorio actual y a su superior, respectivamente. También se pueden ver los contenidos en forma de árbol con el comando

```bash
tree
```

* Para cambiar de directorio usa el comando

```bash
cd ruta-al-directorio
```

  La ruta puede ser absoluta desde la raíz del sistema de archivos `/`, o relativa al directorio actual. Así, si quieres ir al directorio superior, puedes usar `cd ..`. Y para ir a `HOME`, puedes usar `cd ~`. Se puede acceder al sistema de archivos de Windows a través de `/mnt/`, por ejemplo la unidad `C://` se encuentra en `/mnt/c`.

* Para copiar un archivo o directorio se usa el comando

```bash
cp ruta-de-origen ruta-de-destino
```

* Para mover un archivo o directorio se usa el comando

```bash
mv ruta-de-origen ruta-de-destino
```

* Para eliminar un archivo se usa el comando

```bash
rm archivo
```

y para eliminar un directorio y su contenido,

```bash
rm -r directorio
```

* Para buscar archivos se usa el comando

```bash
find ruta-del-directorio -name nombre-del-archivo
```

Es posible buscar varios archivo que tengan partes del nombre en común, sustituyendo las partes diferentes por `*`. Por ejemplo, para buscar todos los archivos de python en la carpeta actual:

```bash
find . -name *.py
```

* Para crear un directorio, se usa el comando

```bash
mkdir nombre-del-directorio
```

* Para crear un archivo vacío, se usa el comando

```bash
touch nombre-del-archivo
```

Si el archivo existía antes, este comando no lo modifica pero cambia la fecha de última edición.

* Para ver el contenido de un archivo de texto se usa el comando

```bash
cat archivo
```

* Para buscar texto en un archivo de texto se usa el comando

```bash
grep "texto buscado" archivo
```

* Para editar un archivo de texto, una posibilidad es usar

```bash
nano archivo
```

También lo puedes abrir con programas de Windows, por ejemplo con el bloc de notas

```bash
notepad.exe archivo
```

o con VSCode

```bash
code archivo
```

* Puedes ejecutar varios comandos en una sola línea uniéndolos mediante `&&`. Se ejecutarán en orden, y solamente si el comando anterior no ha tenido ningún error.
* Puedes redirigir el output de un comando hacia un archivo mediante `>`. Por ejemplo, si quieres buscar todos los archivos de Python en el directorio actual y guardar la lista en un archivo, se usa el comando

```bash
find . -name *.py > archivos_py.txt
```

* También se puede redirigir el output de un programa para usarlo como input de otro mediante `|`. Por ejemplo, si quieres buscar todos los archivos del directorio actual que se han modificado el día 10 de enero,

```bash
ls -al | grep "ene 10"
```

* Si necesitas ejecutar un comando como usuario `root` (equivalente al Administrador en Windows), hay que usar `sudo` antes del comando, por ejemplo

```bash
sudo nano /etc/bashrc
```

 Tendrás que escribir tu contraseña, que de nuevo no verás en pantalla. Típicamente se necesita `sudo` para crear/modificar/eliminar archivos fuera de `~`, y para instalar aplicaciones.

* En Ubuntu, las aplicaciones se instalan a través del gestor de paquetes `apt`. Antes de nada, deberás actualizar el gestor de paquetes con el comando

```bash
sudo apt update && sudo apt upgrade
```

Vamos a probar a instalar un programa llamado `neofetch` que imprime en pantalla información sobre el sistema operativo

```bash
sudo apt install neofetch
```

Si no ha pasado demasiado tiempo desde el comando anterior, `sudo` no te volverá a pedir la contraseña. `apt` te pedirá la confirmación para instalar, escribe `y` y pulsa intro. Cuando acabe la instalación, comprueba que ha funcionado usando el comando

```bash
neofetch
```

Finalmente, comprueba si `python` y `git` están instalados con

```bash
git -v
python3 -V
```

Si no están instalados, vamos a instalarlos. Lo primero es saber cómo se llaman los paquetes que tenemos que instalar. Para ello usamos

```bash
apt search git
```

Este comando basca la expresión "git" en el nombre y la descripción de los paquetes. En algunas ocasiones, como esta, puede generar demasiados resultados. Vamos a acotar un poco la búsqueda únicamente a los paquetes cuyo nombre empieza por "git":

```bash
apt search git | grep "^git"
```

donde `^` sirve para buscar solo al principio de cada línea. La lista debería ser ahora bastante más corta, y el primer paquete que aparece se llama simplemente `git`. Veamos si es el paquete que buscamos usando

```bash
apt show git
```

Esto mostrará bastante información sobre el paquete. Combrueba que la descripción sea "fast, scalable, distributed revision control system", y si es así, instálalo con

```bash
sudo apt install git -y
```

La opción `-y` sirve para que `apt` no pida confirmación.

Si `python3` no está instalado, haz el mismo proceso. En este caso, es mejor usar `grep` con el texto de búsqueda `"^python3\."`, y esto mostrará solamente las versiones de Python. Elige la más actual.

### Usar WSL desde VSCode

Para usar WSL2 desde VSCode, instla la [extensión de desarrollo remoto](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack).

Una vez instalada, pulsa en el botón `><` de la esquina inferior izquierda, y busca la opción para conectar con `WSL`. Algunas de las extensiones de VSCode, como `Python`, necesitarán ser instaladas dentro de WSL. Si abres o creas un nuevo proyecto, lo harás en el sistema de archivos de WSL.

## Instalar Docker

Una vez que WSL2 esté instalado, procede a [descargar e instalar Docker Desktop](https://docs.docker.com/desktop/install/windows-install/), asegurándote de elegir la opción de usar WSL2. Abre la aplicación de Docker, elige la opción de cuenta gratuita, y acepta los términos.

## Contenedores de desarrollo

Los contenedores de desarrollo son una herramienta de VSCode que permite crear de manera sencilla y personalizable contenedores de Docker que contengan las aplicaciones y extensiones necesarias para un determindo proyecto. Esto permite, por ejemplo, que en un proyecto colaborativo todos los participantes usen exactamente el mismo entorno de programación, independientemente de sus ordenadores y sistemas operativos.

Asegúrate de tener instalada la [extensión de desarrollo remoto](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack), pulsa en el botón `><` de la esquina inferior izquierda, y elige la opción de Reabrir en un contenedor de desarrollo. Pulsa en mostrar todas las definiciones y elige `Python 3`. Pulsa en opciones adicionales, elige la versión de Python `3.10` (uno de los paquetes que vamos a usar, `h5py`, aún no está disponible para `3.11`), y en el siguiente cuadro de diálogo busca `poetry` y `GitHub Cli` y selecciónalos.

Tardará un poco en crear el contenedor. Una vez que esté listo, verás que en la esquina imferior izquierda aparece junto a `><` el contenedor de desarrollo. Además, se abrá creado una carpeta llamada `.devcontainer` con un archivo `devcontainer.json`. Es importante que sincronices este archivo en GitHub, y así cualquiera que clone el proyecto tendrá acceso al mismo contenedor. De hecho, cada vez que abras en VSCode un proyecto con un archivo `devcontainer.json`, aparecerá un cuadro de diálogo sugiriendo conectar con el contenedor.

Sal del contenedor pulsando el botón `><` de la esquina inferior izquierda y selecciona cerrar conexión remota. Abre el archivo `devcontainer.json` y des-comenta la siguiente línea
```json
    "remoteUser": "root",
```
y posiblemente tengas que añadir una coma en la última línea no comentada. Vuelve a reabrir en el contenedor, y acepta la opción para reconstruirlo.

A diferencia de WSL, los contenedores son desechables, así que cualquier cambio que realices no se conservará la próxima vez que reconstruyas el contenedor. La única excepción es el directorio `/workspaces`, que contiene el proyecto actual, y que está sincronizado con el directorio de tu sistema de archivos. Cualquier cambio permanente que quieras hacer hay que especificarlo en `devcontainer.json` o en la imagen de Docker que se usa com base. El contenedor ya tiene instalado `python`, `pip`, `git`, `jupyter` y `poetry`, así como varias extensiones de VSCode.

Abre el panel de extensiones de VSCode. Verás que hay algunas que están instaladas en Local (es decir, en tu sistema operativo), y otras en el contenedor de desarrollo. En la sección de Local, puede que algunas extensiones estén desactivadas. Si ves alguna que te interese usar en el contenedor, pulsa con el botón derecho del ratón, y selecciona Añadir a `devcontainer.json`. Cuando las tengas todas listas, sal del contenedor y vuelve a entrar para reconstruirlo.

En `devcontainer.json` también se pueden especificar comandos que se ejecutan al reconstruir el contenedor. Vamos a añadir un comando que instale los paquetes registrados en `poetry`. Para ello, después de `"remoteUser": "root",` añade la siguiente línea:
```json
    "postCreateCommand": "cd /workspaces/nombre-del-proyecto && poetry run poetry install",
```

Reconstruye una vez más el contenedor, y verás cómo se instalan los paquetes. Cuando acabe la instalación, comprueba que ha funcionado correctamente usando el comando `poetry run pip list`. Ya está todo listo para sincronizar `devcontainer.json` con GitHub y trabajar dentro del contenedor.
