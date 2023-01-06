import json

class MilitarySituation:
    
    def __init__(self, driver=None, data={}):
        self._driver = driver
        self._data = data
        self._background_text = ''

    def search_for_background(self):
        # se accede a la url del antecedente judicial
        self.driver.load_browser(self.data['url'])
        
        actions = self.driver.get_action_chains()

        # INGRESAR DATOS EN EL FORMUALRIO
        # se selecciona el tipo de documento
        select_type_doc = self.driver.get_select_by_xpath("//select[@id='ctl00_MainContent_drpDocumentType']")
        select_type_doc.select_by_value(self.data['tipo-documento'])

        # se ingresa el número del documento
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='ctl00_MainContent_txtNumberDocument']"))\
            .click_and_hold()\
            .send_keys(self.data['cedula'])\
            .perform()

        # se da click en el boton consultar
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='ctl00_MainContent_btnConsult']"))\
            .click()\
            .perform()

        # OBTENER RESULTADO DE LA CONSULTA DE LOS ANTECEDENTES
        div_error_messages = self.driver.get_element_by_xpath("//div[@id='divErrorMessages'] //p")
        div_warning_messages = self.driver.get_element_by_xpath("//div[@id='divWarningMessages'] //p")

        # se obtiene el texto del elemento div
        if div_error_messages.text != '' or div_warning_messages.text != '':
            self.background_text = self.background_text + div_error_messages.text + '\n' + div_warning_messages.text
        else: # se acceden al selector que contiene la información
            ids = ['divEnrollment', 'divCited', 'divSuitable', 'divLiquidation', 'divDefined']

            for id in ids:
                try:
                    self.driver.get_element_by_xpath(f"//div[@id='{id}'][@style='display: none']")
                except:
                    div = self.driver.get_element_by_xpath(f"//div[@id='{id}'] //div[@class='col-md-6 col-md-offset-3']")
                    self.background_text = self.background_text + div.text
                    break

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
            'situacion-militar': self.background_text
        })    