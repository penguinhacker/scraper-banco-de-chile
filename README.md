# Aclaraciones

IMPORTANTE: La prueba técnica hasta este momento no está completa. Solamente se ingresa, valida datos y se llega hasta la pestaña donde están las cartolas, pero no se analizan todas las transacciones ni se llevan a MongoDB.

El proyecto venía inicialmente con algunos comandos que son para Linux, es por eso que en algunas partes se agregaron y modificaron pequeños detalles (driver_factory.py, multi_scrape.py, scraper_base.py). Pero todo el contenido relevante de la solución de puede encontrar en app/main.py

Por lo dicho anteriormente, el código está hecho para Windows.

Para que se pudiera utilizar chrome, se debío instalar un driver, el cual se encuentra en webdriver/chromedriver.exe

Se asume que en el computador en el que se ejecute este programa está una versión de:

- Python 3.X
- Selenium
- Pyvirtualdisplay
- Selenium-stealth

Los cuales fueron los requerimientos de las carpetas en sí para que no existieran errores de importación.

# Ejecución

IMPORTANTE: Se buscarán los datos del Banco de Chile.

Para ejecutar el programa, se deben agregar los valores en multi_scrape.py:

- Fechas, en formato: "DD/MM/AAAA"
- Usuario, siendo el rut, sin puntos ni guión
- Constraseña
- Cuenta, teniendo esta el siguiente formato: "11-111-1111-11", es decir, con guiones y con todos los dígitos.

Y luego, ejecutar multi_scrape.py