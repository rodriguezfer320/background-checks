from . import Background

class CorrectiveActionBackground(Background):
    
    def __init__(self, driver):
        super().__init__(driver)

    def search_for_background(self, data):
        # se accede a la url del antecedente
        self.driver.load_browser(data['url'])
        
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
        div_info = self.driver.get_element_by_xpath("//div[@id='ctl00_ContentPlaceHolder3_respuesta'] //div[@class='row']").text

        # se cierra el navegador
        self.driver.close_browser()
        
        # se añade la información obtenida a una variable
        self.text['title'] = div_info[div_info.index('La Policía Nacional de Colombia informa:'):div_info.index('Que a la fecha')].strip()
        self.text['message'] = div_info[div_info.index('Que a la fecha'):div_info.index('De conformidad con la Ley')].strip()