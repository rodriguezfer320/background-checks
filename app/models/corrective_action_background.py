from .background import Background

class CorrectiveActionBackground(Background):
    
    def __init__(self, driver=None):
        super().__init__(driver)

    def search_for_background(self, data):
        # se accede a la url del antecedente
        self.driver.load_browser(data['url'])
        
        actions = self.driver.get_action_chains()

        # PÁGINA 1 - INGRESAR DATOS EN EL FORMUALRIO
        # se selecciona el tipo de documento
        select_type_doc = self.driver.get_select_by_xpath("//select[@id='ctl00_ContentPlaceHolder3_ddlTipoDoc']")
        select_type_doc.select_by_value(data['tipo-documento'])
        actions\
            .pause(2)\
            .perform()

        # se ingresa el número del documento
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='ctl00_ContentPlaceHolder3_txtExpediente']"))\
            .click_and_hold()\
            .send_keys(data['cedula'])\
            .perform()

        # se ingresa la fecha de expedición del documento
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='txtFechaexp']"))\
            .click_and_hold()\
            .send_keys(data['fecha-expedicion'])\
            .perform()

        # se da click en el icono de buscar (simbolo de la lupa)
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//a[@id='ctl00_ContentPlaceHolder3_btnConsultar2']"))\
            .click()\
            .perform()

        # PÁGINA 2 - OBTENER RESULTADO DE LA CONSULTA DE LOS ANTECEDENTES
        # se acceden al selector que contiene la información
        div = self.driver.get_element_by_xpath("//div[@id='ctl00_ContentPlaceHolder3_respuesta'] //div[@class='row']")
        
        # se obtiene el texto del elemento div
        self.text = self.text + div.text

        # se cierra el navegador
        self.driver.close_browser()