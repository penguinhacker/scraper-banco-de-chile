import os
from .constants import (
    SERVER_ENVS,
    TEMP_FOLDER
)
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service
from .mime_type import MIME_TYPE
from selenium_stealth import stealth
from selenium.webdriver import Chrome, ChromeOptions


class Singleton(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
        return self._instances[self]


class DriverFactory:

    __metaclass__ = Singleton

    server_envs = SERVER_ENVS

    def get_driver(self,
                   browser: str,
                   options: webdriver.ChromeOptions = None,
                   prefs: dict = None
                   ) -> webdriver:
        if os.environ.get('ENV') in self.server_envs:
            self.setup()
        driver = None
        if browser == 'chrome':
            driver = self.build_chrome(options=options, prefs=prefs)
        if browser == 'firefox':
            driver = self.build_firefox()
        if not driver:
            raise ValueError(f'{browser} is not supported')
        return driver

    def setup(self):
        for dir in ['/tmp/bin', '/tmp/bin/lib', '/tmp/download']:
            if not os.path.exists(dir):
                os.makedirs(dir)

        self.tmp_folder = TEMP_FOLDER

        for dir in ['', '/user-data', '/data-path',  '/cache-dir']:
            if not os.path.exists(f'{self.tmp_folder}{dir}'):
                os.makedirs(f'{self.tmp_folder}{dir}')
    
    def build_firefox(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", "/tmp/download")
        profile.set_preference("plugins.always_open_pdf_externally,", True)
        profile.set_preference("browser.download.manager.useWindow", False)
        profile.set_preference("pdfjs.disabled", True)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", MIME_TYPE)
        options = Options()
        if os.environ.get('ENV') in self.server_envs:
            options.headless = bool(os.environ.get('HEADLESS'))
            return webdriver.Firefox(
                firefox_profile=profile,
                options=options,
                executable_path='/opt/drivers/geckodriver',
                service_log_path='/tmp/geckodriver.log')
        else:
            return webdriver.Firefox(
                firefox_profile=profile,
                options=options,
                executable_path='/usr/share/geckodriver')

    def build_chrome(self, options: webdriver.ChromeOptions = None, prefs: dict = None):
        if not prefs:
            prefs = {
                "download.default_directory": "/tmp/download",
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "profile.default_content_setting_values.automatic_downloads": 1,
            }

        # Se obtiene la ruta absoluta del directorio actual.
        current_directory = os.path.dirname(os.path.abspath(__file__))
        # Se concatena el ejecutable para obtener el directorio total.
        chrome_driver_path = os.path.join(current_directory, 'chromedriver.exe')
        # Se genera el servicio.
        service = Service(executable_path=chrome_driver_path)

        if not options:
            options = webdriver.ChromeOptions()
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--window-size=1280,768')
            options.add_argument('--disable-popup-blocking')
            options.add_argument("--disable-setuid-sandbox")
            options.add_argument("--remote-debugging-port=9222")  # this
            options.add_argument("--start-maximized")  # this
            options.add_argument('--enable-logging')
            options.add_argument('--log-level=0')
            options.add_argument('--v=99')
            options.add_experimental_option('prefs', prefs)
            options.add_argument("--incognito")
            if os.environ.get('ENV') in self.server_envs:
                if bool(os.environ.get('HEADLESS')):
                    options.add_argument('--headless')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument(f'--homedir=~{self.tmp_folder}')
                options.add_argument(f'--user-data-dir={self.tmp_folder}/user-data')
                options.add_argument(f'--data-path={self.tmp_folder}/data-path')
                options.add_argument(f'--disk-cache-dir={self.tmp_folder}/cache-dir')
                options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 "
                                    "(KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                chrome = webdriver.Chrome(service=service, options=options)
                self._stealth_mode_chrome(chrome=chrome)
            else:
                chrome = webdriver.Chrome(service=service, options=options)
        else:
            chrome = webdriver.Chrome(service=service, options=options)
            if os.environ.get('ENV') in self.server_envs:
                self._stealth_mode_chrome(chrome=chrome)
        return chrome
    
    def _stealth_mode_chrome(self, chrome: webdriver.Chrome):
        stealth(chrome,
            languages=["es-CL", "es"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
