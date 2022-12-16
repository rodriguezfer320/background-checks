from ..models.solve_recaptcha import SolveRecaptcha
import json

class JudicialBackground:
    
    def __init__(self, driver=None, data={}):
        self._driver = driver
        self._data = data
        self._background_text = ''

    def search_for_background(self):
        # se accede a la url del antecedente judicial
        self.driver.load_browser(self.data['url'])
        
        actions = self.driver.get_action_chains()

        # PÁGINA 1 - TÉRMINOS DE USO
        # se da click en la opción aceptar
        actions\
            .pause(2)\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='aceptaOption:0']"))\
            .pause(1)\
            .click()\
            .pause(2)\
            .perform()
        
        # se da click en el botón enviar
        actions\
            .pause(2)\
            .move_to_element(self.driver.get_element_by_xpath("//button[@id='continuarBtn']"))\
            .pause(1)\
            .click()\
            .perform()

        # PÁGINA 2 - INGRESAR DATOS EN EL FORMUALRIO
        # se ingresa el número del documento
        actions\
            .pause(2)\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='cedulaInput']"))\
            .pause(1)\
            .click_and_hold()\
            .pause(1)\
            .send_keys(self.data['cedula'])\
            .perform()

        # se selecciona el tipo de documento
        actions\
            .pause(2)\
            .perform()
        select_type_doc = self.driver.get_select_by_xpath("//select[@id='cedulaTipo']")
        select_type_doc.select_by_value(self.data['tipo-documento'])

        # se resuelve el recaptcha de la pagina
        recaptcha = SolveRecaptcha()
        recaptcha.driver = self.driver
        recaptcha.solve_by_audio()

        # se da click en el boton consultar
        actions\
            .pause(2)\
            .move_to_element(self.driver.get_element_by_xpath("//button[@id='j_idt17']"))\
            .pause(1)\
            .click()\
            .perform()

        # PÁGINA 3 - OBTENER RESULTADO DE LA CONSULTA DE LOS ANTECEDENTES
        # se acceden a los selectores que contienen la información
        actions\
            .pause(2)\
            .perform()
        spans = self.driver.get_element_by_xpath("//div[@id='form:j_idt8_content'] //span", True)
        
        # se obtiene el texto de los selectores span
        for element in spans:
            self.background_text = self.background_text + element.text

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
            'antecedente-judicial': self.background_text
        })    