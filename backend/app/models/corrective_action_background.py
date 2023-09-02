from .background_web import BackgroundWeb

class CorrectiveActionBackground(BackgroundWeb):
    
    def __init__(self, driver, description):
        super().__init__(driver, description)

    def get_background_information(self, data):
        # se accede a la url del antecedente
        self.driver.load_browser(data['background'].url)
        
        # se carga el controlador de acciones de entrada de dispositivo virtualizadas
        actions = self.driver.get_action_chains()

        # PÁGINA 1 - INGRESAR DATOS EN EL FORMUALRIO
        # 1. se selecciona el tipo de documento
        select_type_doc = self.driver.get_select_by_xpath("//select[@id='ctl00_ContentPlaceHolder3_ddlTipoDoc']")
        select_type_doc.select_by_value('55')
        actions\
            .pause(4)\
            .perform()

        # 2. se ingresa el número del documento
        # 3. se ingresa la fecha de expedición del documento
        # 4. se da click en el icono de buscar (simbolo de la lupa)
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='ctl00_ContentPlaceHolder3_txtExpediente']"))\
            .click_and_hold()\
            .send_keys(data['document'])\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='txtFechaexp']"))\
            .click_and_hold()\
            .send_keys(data['date-expedition'])\
            .move_to_element(self.driver.get_element_by_xpath("//a[@id='ctl00_ContentPlaceHolder3_btnConsultar2']"))\
            .click()\
            .perform()

        # PÁGINA 2 - OBTENER RESULTADO DE LA CONSULTA DE LOS ANTECEDENTES
        # se accede al selector que contiene la información
        div = self.driver.get_element_by_xpath("//div[@id='ctl00_ContentPlaceHolder3_respuesta'] //div[@class='row']")
        self._data_web = div.text

        # se cierra el navegador
        self.driver.close_browser()

    def process_information(self, data):
        # se añade la información obtenida a una variable
        self.description['title'] = self._data_web[self._data_web.index('La Policía Nacional de Colombia informa:'):self._data_web.index('Que a la fecha')].strip()
        self.description['message'] = self._data_web[self._data_web.index('Que a la fecha'):self._data_web.index('De conformidad con la Ley')].strip()