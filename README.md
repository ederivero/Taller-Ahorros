<p align="center">
  <a href="https://www.tecsup.edu.pe/desarrolloweb/" target="blank"><img src="https://www.tecsup.edu.pe/desarrolloweb/img/logo-cod.svg" width="320" alt="CodiGo Logo" /></a>
</p>

# <div align="center">Taller de Sistema de Ahorros con balance mensual de CodiGo</div>

Bienvenido al repositorio 📂️ donde podrás encontrar el codigo del taller de **Sistema de Ahorros con balance mensual** 🤓️

Para comenzar es muy sencillo solamente sigue los siguientes pasos de instalación y podrás ejecutar el proyecto en tu máquina 💻️! 🤩️🤩️

# 📝 Indice

- [Instalación](#instalacion)
  - [Paso 1](#paso1)
  - [Paso 2](#paso2)
  - [Paso 3](#paso3)
  - [Paso 4](#paso4)
  - [Paso 5](#paso5)
  - [Paso 6](#paso6)
- [Extras](#extras)
- [Licencia](#licencia)

# ⚙️ Instalación<a name = "instalacion"></a>

## Paso 1<a name = "paso1"></a>

Este repositorio requiere que tengas instalado [Python3](https://www.python.org/) v3.7+ para funcionar.
Una vez que tengas Python instalado, para comprobar ejecuta el siguiente comando en una _terminal_ o _power shell_

- En Windows

  ```
  $ python --version
  ```

- En Mac / Linux

  ```
  $ python3 --version
  ```

## Paso 2<a name = "paso2"></a>

Descarga este repositorio mediante [Git](https://git-scm.com/) con el siguiente comando:

```
$ git clone https://github.com/ederivero/Taller-Ahorros.git
```

O si no tienes instalado _Git_ en tu máquina, descarga el repositorio desde un _zip_ haciendo click [aquí](https://github.com/ederivero/Taller-Ahorros/archive/refs/heads/main.zip) y luego descomprimiendolo.

Sin importar el metodo que escogas ya deberás tener el repositorio en tu máquina.

## Paso 3<a name = "paso3"></a>

Una vez descargado el repositorio, ahora, crea un entorno virtual para que solamente las librerías que vayamos a usar en este proyecto sean locales y no interfieran con el funcionamiento global de [Python](https://www.python.org/) de la siguiente forma:

- En Windows

  ```
  $ python -m venv entorno_taller
  ```

- En Mac / Linux

  ```
  $ python3 -m venv entorno_taller
  ```

## Paso 4<a name = "paso4"></a>

Una vez creado el entorno virtual, ahora procederemos a activarlo de la siguiente manera:

- En Windows

  ```
  $ entorno_taller/Scripts/activate
  ```

- En Mac / Linux

  ```
  $ source entorno_taller/bin/activate
  ```

## Paso 4<a name = "paso4"></a>

Ejecuta el siguiente comando:

```
$ pip install -r requirements_dev.txt
```

Que es lo que hace este comando?

- Dentro del proyecto hay un archivo llamado `requirements_dev.txt` es ahi donde estan declaradas todas las librerias que necesitamos para que el proyecto funcione exitosamente con sus respectivas versiones.

## Paso 5<a name = "paso5"></a>

Ahora tendremos que crear el archivo `.env` y copiar todo el contenido del archivo `.env.example` ya que ahi se ubican las variables de entorno de nuestro proyecto

- Nota: si quieres pasar a [MySQL](https://www.mysql.com/) entonces deberas definir tu conección en la variable `DATABASE_URI`

## Paso 6<a name = "paso6"></a>

Luego procederemos a levantar el proyecto 🚀

- En Windows

  ```
  $ python app.py
  ```

- En Mac / Linux

  ```
  $ python3 app.py
  ```

Ya estámos! Ya podemos levantar nuestro proyecto, no necesitas preocuparte de las bases de datos 🗄️ ya que estamos usando [SQLITE](https://www.sqlite.org/index.html) que es una base de datos muy ligera y generará un archivo llamado `test.db` dentro de la carpeta `db/`. 💯

# 🎯 Extras<a name = "extras"></a>

Si quieres visualizar los datos que se han almacenado en la base de datos, te recomiendo descargarte el siguiente software ultra ligero ➡️ [SQLite Browser](https://sqlitebrowser.org/dl/)

# 📜 Licencia<a name = "licencia"></a>

[MIT](https://opensource.org/licenses/MIT)

**Software Libre, Happy Coding!💻**
