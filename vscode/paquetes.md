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
