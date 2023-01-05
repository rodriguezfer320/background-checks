from .solve_recaptcha import SolveRecaptcha
import json, time

class FiscalBackground:
    
    def __init__(self, driver=None, data={}):
        self._driver = driver
        self._data = data
        self._background_text = ''

    def search_for_background(self):
        # se accede a la url del antecedente judicial
        self.driver.load_browser(self.data['url'])
        
        actions = self.driver.get_action_chains()

        # PÁGINA 1 - INGRESAR DATOS EN EL FORMUALRIO
        # se mueve el foco a la ventana Certificado Para Personas Naturales
        self.driver.change_frame_by_css_selector("iframe[src^='https://cfiscal.contraloria.gov.co/Certificados/CertificadoPersonaNatural.aspx']")

        # se selecciona el tipo de documento
        actions\
            .pause(2)\
            .perform()   
        select_type_doc = self.driver.get_select_by_xpath("//select[@id='ddlTipoDocumento']")
        select_type_doc.select_by_value(self.data['tipo-documento'])

        # se ingresa el número del documento
        actions\
            .pause(2)\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='txtNumeroDocumento']"))\
            .pause(1)\
            .click_and_hold()\
            .pause(1)\
            .send_keys(self.data['cedula'])\
            .perform()

        # se resuelve el recaptcha de la pagina
        recaptcha = SolveRecaptcha()
        recaptcha.driver = self.driver
        recaptcha.solve_by_audio(False)

        # se da click en el boton consultar
        actions\
            .pause(2)\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='btnBuscar']"))\
            .pause(1)\
            .click()\
            .pause(5)\
            .perform()

        self.background_text = "pdf descargado"

        # se cierra el navegador
        self.driver.close_browser()

    #Getters
    @property
    def driver(self):
        return self._driver

    @property
    def data(self):
        return self._data

    @property
    def background_text(self):
        return self._background_text

    #Setters
    @driver.setter
    def driver(self, driver):
        self._driver = driver

    @data.setter
    def data(self, data):
        self._data = data

    @background_text.setter
    def background_text(self, text):
        self._background_text = text

    def to_json(self):
        return json.dumps({
            'antecedente-fiscal': self.background_text
        })    