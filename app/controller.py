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
        #Desde acá tenemos un self.driver

        if self.login() and self.exists_account():
        #if self.login():
            self.obtain_documents()
        return self.result

    def login(self) -> bool:
        is_valid = False

        #Vamos a la página del banco (indicada en el README)
        self.driver.get("https://portales.bancochile.cl/personas/")

        boton = self.driver.find_element(By.ID, "ppp_header-link-banco_en_linea")
        boton.click()

        username_field = self.driver.find_element(By.ID, "iduserName")
        password_field = self.driver.find_element(By.ID, "password")

        username_field.send_keys(self.usuario)
        password_field.send_keys(self.password)

        boton_ingresar = self.driver.find_element(By.ID, "idIngresar")

        url_before_click = self.driver.current_url

        boton_ingresar.click()

        print("url before: ", url_before_click)

        correct_login_url = "https://portalpersonas.bancochile.cl/mibancochile-web/front/persona/index.html#/home"

        WebDriverWait(self.driver, 10).until(
            EC.url_changes(url_before_click)
        )

        url_after_click = self.driver.current_url
        print("url after:", url_after_click)

        if url_after_click == correct_login_url:
            print("Ingresó con éxito")
            return True

        else:
            print("Falla al ingresar")
            return False


        

    def exists_account(self) -> bool:
        #En este momento, deberíamos estar en:
        # "https://portalpersonas.bancochile.cl/mibancochile-web/front/persona/index.html#/home"

        if self.account in self.driver.page_source:
            print("--- CUENTA EN LA PÁGINA ---")
            return True
        
        else:
            print("--- CUENTA NO EN LA PÁGINA ---")
            return False

        
    def obtain_documents(self) -> None:
        #aqui tcodigo para obtener los movimientos
        #En este momento, deberíamos estar en:
        # "https://portalpersonas.bancochile.cl/mibancochile-web/front/persona/index.html#/home"
        elemento_a = self.driver.find_element(By.XPATH, "//a[p[contains(., '{}')]]".format(self.account))

        # Hacer clic en el elemento <a>
        elemento_a.click()

        time.sleep(5)


       
        #elemento_historia = self.driver.find_element(By.XPATH, "//a[contains('Cartola histórica')]]")


        #Buscar el botón por css, no se ha podido encontrar de otra manera. 
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@href="#/movimientos/cuenta/cartola-historica"]'))
        )
        button.click()




        time.sleep(5)
            
        inputs_fechas = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "mat-datepicker-input"))
        )

        

        #final_date_field = self.driver.find_element(By.CLASS_NAME, "mat-datepicker-input")

        
        # Borrar el texto de los campos de fecha
        
        inputs_fechas[0].send_keys(Keys.CONTROL + "a")  # Seleccionar todo el texto en el campo
        inputs_fechas[0].send_keys(Keys.DELETE)     
        

        
        inputs_fechas[0].send_keys(self.since[3:])

        inputs_fechas[1].send_keys(Keys.CONTROL + "a")  # Seleccionar todo el texto en el campo
        inputs_fechas[1].send_keys(Keys.DELETE)     
        inputs_fechas[1].send_keys(self.until[3:])

        inputs_fechas[1].send_keys(Keys.ENTER)   

        botones_descargar = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "mat-button-base"))
        )

        # Hacer clic en cada botón
        for boton in botones_descargar:
            boton.click()
            time.sleep(10)

        while True:
            print("---")
            a = 1
        
        #filter_button = self.driver.find_element(By.XPATH,"//button[contains(text(), 'Filtrar')]")
       

        #print("URL:",self.driver.current_url)

        #filter_button.click()




        while True:
            a = 1
        pass
