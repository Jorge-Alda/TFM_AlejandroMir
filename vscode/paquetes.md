# Gestión de paquetes de Python

## Instalación de paquetes de Python

El gestor de paquetes de Python nativo es `pip`, aunque también existen otras opciones, como `conda`. La instalación básica es

```Bash
pip install flavio
```

`pip` instala tanto el paquete solicitado como sus dependencias, es decir, otros paquetes que son necesarios para su funcionamiento. Si hay un entorno virtual activado, `pip` solamente tiene acceso a los paquetes propios del entorno. Eso permite, por ejemplo, tener varias versiones de un mismo paquete en entornos distintos. Se puede instalar una versión concreta de un paquete usando

```bash
pip install flavio==2.3.1
```

También es posible especificar una versión mínima, o una versión máxima

```bash
pip install "flavio >= 2.3"
pip install "flavio < 2.4"
```

`pip` obtiene los paquetes del repositorio [PyPi](https://pypi.org). Alternativamente, se pueden obtener paquetes de otras fuentes, como un repositorio git. Para instalar desde el commit más reciente de la rama principal, hay que usar como identificador del paquete `git+{Dirección del repositorio}.git#egg={Nombre del paquete}`, por ejemplo

```bash
pip install git+https://github.com/flav-io/flavio.git#egg=flavio
```

Para instalar desde una rama o commit concretos, hay que añadir entre `.git` y `#egg` una `@` y el identificador correspondiente,

```bash
pip install git+https://github.com/flav-io/flavio.git@lhcb-measurements#egg=flavio
pip install git+https://github.com/flav-io/flavio.git@b7ac308ac83cd7168d80c3382b5d65415bc64679#egg=flavio
```

Se puede automatizar el proceso de instalación, y asegurarse de que todos los paquetes están en la misma versión que has usado, hay que crear un archivo llamado `requirements.txt`, en la que se incluyan, en cada línea, los paquetes instalados y su versión, identificada con `==`. Para los paquetes instalados desde git, hay que usar la misma notación con `git+...`. Los paquetes especificados en `requirements.txt`(más sus dependencias) se pueden instalar con un solo comando,

```bash
pip install -r requirements.txt
```

## Gestión de paquetes y entornos virtuales con poetry

`poetry` es una herramienta que automáticamente crea un entorno virtual y gestiona los paquetes que se instalan en él. Puedes obtener `poetry` [aquí](https://python-poetry.org/docs/)

Para empezar a usarlo, abre la terminal en python en la carpeta del proyecto, y ejecuta

```bash
poetry new nombre-del-proyecto
```

El programa te irá preguntando datos del programa. Cuando te pregunte si quieres definir las dependencias, di que no. Esto crea un archivo llamado `pyproject.toml` que contiene los metadatos y la información necesaria para instalar tu paquete, y una estructura de directorios como la que se explica a continuación. A continuación, para crear el entorno virtual, usa el comando

```bash
poetry shell
```

Recuerda seleccionar el entorno como predeterminado para el proyecto, y crear un kernel de Jupyter si es necesario, como se explicó [aquí](venv.md).

Cuando quieras añadir un paquete, usa el comando

```bash
poetry add flavio
poetry install
```

El comando `poetry add` simplemente marca el paquete para instalar, es necesario hacer `poetry install` después. La forma de especificar las versiones es igual que en `pip`. Sin embargo, para instalar desde `git` hay pequeñas diferencias:

```bash
poetry add git+https://github.com/flav-io/flavio.git
poetry install
```

y para instalar desde una rama,

```bash
poetry add git+https://github.com/flav-io/flavio.git#lhcb-measurements
poetry install
```

Además de instalar las dependencias, estos comandos modifican el archivo `pyproject.toml` y crean un archivo `poetry.lock` en el que se detallan las versiones exactas de los paquetes instalados y de sus dependencias.

Una vez especificadas todas las dependencias con `poetry`, y subidos los archivos `pyproject.toml` y `poetry.lock`, cualquiera puede instalar el paquete que has creado usando `pip` en el modo `git+...`.

## Estructura del proyecto

Un paquete de Python se estructura en módulos (y sub-módulos, sub-sub-módulos, etc). Por ejemplo, si queremos usar la función de `flavio` para calcular el nivel de confianza correspondiente a un número de sigmas,

```python
import flavio
cl = flavio.statistics.functions.confidence_level(2.3)
```

estamos usando la función `confidence_level()` definida en el archivo `functions.py` del módulo `statistics` de `flavio`. Puedes ver los contenidos de un paquete, módulo o sub-módulo, con la función `dir()`

```python
dir(flavio.statistics.functions)
```

Cada módulo se corresponde con una carpeta (sub-módulos con sub-carpetas) que contenga un archivo llamado `__init__.py`. El cometido de este archivo es importar todas las clases y funciones que aparecerán en `dir()`, y albergar el [docstring](annotations.md#doctrings) del módulo. En el caso de `flavio`, por ejemplo, tenemos la siguiente estructura:

```
flavio/
  |- statistics/
  |   |- probability.py
  |   |- functions.py
  |   |- __init__.py
  |- __init__.py
```

En el archivo `flavio/statistics/functions.py` hay algo similar a esto:

```python
def confidence_level(nsigma):
    r"""Return the confidence level corresponding to a number of sigmas,
    i.e. the probability contained in the normal distribution between $-n\sigma$
    and $+n\sigma$.
    Example: `confidence_level(1)` returns approximately 0.68."""
    ...

def delta_chi2(nsigma, dof):
    ...
```

mientras que en el archivo `flavio/statistics/__init__.py` están los imports de los archivos,

```python
"""Module containing everything needed for statistical analyses, fitting, etc."""

from . import probability
from . import functions
```

El `.` en el import hace referencia a la carpeta en la que se encuentra `__init__.py`. Por su parte, también es necesario importar el módulo `statistics`, desde el archivo `flavio/__init__.py`:

```python
from . import statistics
```
