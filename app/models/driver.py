from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import os

class Driver:

    def __init__(self):
        self.service = Service(executable_path=ChromeDriverManager(path=os.getcwd() + '/app/static/chromedriver').install())
        self.options = Options()
        self.browser = None

    def load_options(self):
        options = {
            'exp_opt': {
                'excludeSwitches': [
                    'enable-automation',
                    'ignore-certificate-errors',
                    'enable-logging',
                    'safebrowsing-disable-download-protection',
                    'safebrowsing-disable-auto-update',
                    'disable-client-side-phishing-detection'
                ],
                'prefs': {
                    'profile.default_content_setting_values.notifications': 2,
                    'intl.accept_languages': ['es-ES', 'es'],
                    'credentials_enable_service': False
                },
                'useAutomationExtension': False
            },
            'args': [
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                '--disable-popup-blocking', # deshabilita las ventanas emergentes que se muestran en el navegador
                '--incognito', # inicia el navegador en modo incógnito
                '--profile-directory=Default',
                '--disable-plugins-discovery',
                '--start-maximized', # inicia el navegador en modo maximizado
                '--disable-extensions', # deshabilita las extensiones existentes en el navegador
                '--disable-notifications',
                '--log-level=3',
                #'--no-proxy-server',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--allow-running-insecure-content',
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                #'--mute-audio',
                '--no-zygote',
                '--no-xshm',
                #'--window-size=1920,1080',
                '--no-first-run',
                '--no-default-browser-check',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--enable-webgl',
                '--ignore-certificate-errors',
                #'--lang=en-US,en;q=0.9',
                '--password-store=basic',
                '--disable-gpu-sandbox',
                '--disable-software-rasterizer',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-infobars', # evita que se muestre la notificación ‘Navegador está siendo controlado por un software automatizado
                '--disable-breakpad',
                '--disable-canvas-aa',
                '--disable-2d-canvas-clip-aa',
                '--disable-gl-drawing-for-tests',
                '--enable-low-end-device-mode',
                #'--disable-extensions-except=./plugin',
                #'--load-extension=./plugin'
            ]
        }

        self.options.page_load_strategy = 'normal'
        self.options.headless = False # inicia el navegador en segundo plano

        for (key, value) in options['exp_opt'].items():
            self.options.add_experimental_option(key, value)
        
        for arg in options['args']:
            self.options.add_argument(arg)

    def load_browser(self, url):
        self.browser = webdriver.Chrome(service=self.service, options=self.options)
        self.browser.implicitly_wait(10)
        self.browser.get(url)
    
    def close_browser(self):
        self.browser.close()

    def get_element_by_xpath(self, xpath, multiple=False):
        if multiple:
            return self.browser.find_elements(By.XPATH, xpath)
        else:
            return self.browser.find_element(By.XPATH, xpath)

    def get_select_by_xpath(self, xpath):
        return Select(self.get_element_by_xpath(xpath))

    def get_action_chains(self):
        return ActionChains(self.browser)
        
    def change_frame_by_css_selector(self, css_selector):
        self.browser.switch_to.parent_frame()

        if not css_selector == 'body':
            iframe = self.browser.find_element(By.CSS_SELECTOR, css_selector)
            self.browser.switch_to.frame(iframe)