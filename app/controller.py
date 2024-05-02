from webdriver.scraper_base import ScraperBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time



class BancoScraper(ScraperBase):
    def __init__(
        self,
        date_range: dict,
        usuario: str,
        password: str,
        account:str
    ):
        self.since = date_range["since"] 
        self.until = date_range["until"]
        self.usuario = usuario
        self.password = password
        self.account = account
        self.result = {}

    def execute(self) -> dict:
        self.get_driver()
        # Desde acá tenemos un self.driver

        if self.login() and self.exists_account():
            self.obtain_documents()
        return self.result

    '''
    Método de login, en el cual se va al sitio del banco, al apartado de "Personas"
    y se ingresan las credenciales para iniciar sesión.

    Despues de presionar el botón de iniciar, se espera un tiempo para ver si se cambió la dirección url o no.

    Como el url de inicio de sesión no incluye variables y siempre es el mismo, se usa ese para ver si el
    redireccionamiento fué a ese sitio o no.
    '''
    def login(self) -> bool:

        #Vamos a la página del banco (indicada en el README)
        self.driver.get("https://portales.bancochile.cl/personas/")

        button = self.driver.find_element(By.ID, "ppp_header-link-banco_en_linea")
        button.click()

        username_field = self.driver.find_element(By.ID, "iduserName")
        password_field = self.driver.find_element(By.ID, "password")

        username_field.send_keys(self.usuario)
        password_field.send_keys(self.password)

        login_button = self.driver.find_element(By.ID, "idIngresar")

        url_before_click = self.driver.current_url

        login_button.click()

        correct_login_url = "https://portalpersonas.bancochile.cl/mibancochile-web/front/persona/index.html#/home"

        WebDriverWait(self.driver, 10).until(
            EC.url_changes(url_before_click)
        )

        url_after_click = self.driver.current_url

        if url_after_click == correct_login_url:
            return True

        else:
            return False


        
    '''
    Para ver la cuenta se utilizó la siguiente lógica:
    En la página principal del Banco de Chile, existe un apartado con las cuentas existentes del usuario.
    La manera para ver si la cuenta ingresada existe, es ver si hay alguna ocurrencia de ella en la misma página.
    Por la naturaleza de los guiones en la cuenta, no es posible que se pueda existir un elemento en la 
    pagina de inicio que simule ser una cuenta.

    Es por esto que la solución es tán simple como buscar la cuenta en el html.
    '''
    def exists_account(self) -> bool:
        # En este momento, deberíamos estar en:
        # "https://portalpersonas.bancochile.cl/mibancochile-web/front/persona/index.html#/home"

        if self.account in self.driver.page_source:
            return True
        
        else:
            return False

        
    '''
    Desde esta parte, la lógica es:

    Primero se selecciona una de todas las cuentas. Pues un usuario puede tener más de una, para eso se nota
    que donde está escrita la cuenta, hay un link, el cual se presiona al momento de buscar la cuenta.

    Luego, se va al apartado de las cartolas históricas, especialmente porque estas tienen una ventana de 12 meses.

    Luego, se ingresa el valor del rango de fechas y se presiona enter para cargar los archivos, esto último
    por la naturalidad de las páginas estáticas.
    '''
    def obtain_documents(self) -> None:
        # En este momento, deberíamos estar en:
        # "https://portalpersonas.bancochile.cl/mibancochile-web/front/persona/index.html#/home"
        a_element = self.driver.find_element(By.XPATH, "//a[p[contains(., '{}')]]".format(self.account))

        # Hacer clic en el elemento <a>
        a_element.click()

        time.sleep(5)

        #Buscar el botón por css, no se ha podido encontrar de otra manera. 
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@href="#/movimientos/cuenta/cartola-historica"]'))
        )
        button.click()

        time.sleep(5)
            
        input_dates = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "mat-datepicker-input"))
        )

        
        # Borrar el texto de los campos de fecha
        
        input_dates[0].send_keys(Keys.CONTROL + "a") # Seleccionar todo el texto en el campo
        input_dates[0].send_keys(Keys.DELETE)     
        input_dates[0].send_keys(self.since[3:])

        input_dates[1].send_keys(Keys.CONTROL + "a")  
        input_dates[1].send_keys(Keys.DELETE)     
        input_dates[1].send_keys(self.until[3:])

        input_dates[1].send_keys(Keys.ENTER)   

        time.sleep(10)
        
        
