from .background import Background

class MilitarySituationBackground(Background):
    
    def __init__(self, driver=None):
        super().__init__(driver)

    def search_for_background(self, data):
        # se accede a la url del antecedente judicial
        self.driver.load_browser(data['url'])
        
        actions = self.driver.get_action_chains()

        # INGRESAR DATOS EN EL FORMUALRIO
        # se selecciona el tipo de documento
        select_type_doc = self.driver.get_select_by_xpath("//select[@id='ctl00_MainContent_drpDocumentType']")
        select_type_doc.select_by_value(data['tipo-documento'])

        # se ingresa el número del documento
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='ctl00_MainContent_txtNumberDocument']"))\
            .click_and_hold()\
            .send_keys(data['cedula'])\
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
            self.text = self.text + div_error_messages.text + '\n' + div_warning_messages.text
        else: # se acceden al selector que contiene la información
            ids = ['divEnrollment', 'divCited', 'divSuitable', 'divLiquidation', 'divDefined']

            for id in ids:
                try:
                    self.driver.get_element_by_xpath(f"//div[@id='{id}'][@style='display: none']")
                except:
                    div = self.driver.get_element_by_xpath(f"//div[@id='{id}'] //div[@class='col-md-6 col-md-offset-3']")
                    self.text = self.text + div.text
                    break

        # se cierra el navegador
        self.driver.close_browser()  