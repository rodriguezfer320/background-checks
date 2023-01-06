import json

class CorrectiveActionCertificate:
    
    def __init__(self, driver=None, data={}):
        self._driver = driver
        self._data = data
        self._background_text = ''

    def search_for_background(self):
        # se accede a la url del antecedente judicial
        self.driver.load_browser(self.data['url'])
        
        actions = self.driver.get_action_chains()

        # PÁGINA 1 - INGRESAR DATOS EN EL FORMUALRIO
        # se selecciona el tipo de documento
        select_type_doc = self.driver.get_select_by_xpath("//select[@id='ctl00_ContentPlaceHolder3_ddlTipoDoc']")
        select_type_doc.select_by_value(self.data['tipo-documento'])
        actions\
            .pause(2)\
            .perform()

        # se ingresa el número del documento
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='ctl00_ContentPlaceHolder3_txtExpediente']"))\
            .click_and_hold()\
            .send_keys(self.data['cedula'])\
            .perform()

        # se ingresa la fecha de expedición del documento
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='txtFechaexp']"))\
            .click_and_hold()\
            .send_keys(self.data['fecha-expedicion'])\
            .perform()

        # se da click en el icono de buscar (simbolo de la lupa)
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//a[@id='ctl00_ContentPlaceHolder3_btnConsultar2']"))\
            .click()\
            .perform()

        # PÁGINA 2 - OBTENER RESULTADO DE LA CONSULTA DE LOS ANTECEDENTES
        # se acceden al selector que contienen la información
        div = self.driver.get_element_by_xpath("//div[@id='ctl00_ContentPlaceHolder3_respuesta'] //div[@class='row']")
        
        # se obtiene el texto del elemento div
        self.background_text = self.background_text + div.text

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
            'certificado-medidas-corretivas': self.background_text
        })    