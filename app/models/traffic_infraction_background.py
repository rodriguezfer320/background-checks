from .background import Background

class TrafficInfractionBackground(Background):
    
    def __init__(self, driver=None):
        super().__init__(driver)

    def search_for_background(self, data):
        # se accede a la url del antecedente
        self.driver.load_browser(data['url'])
        
        actions = self.driver.get_action_chains()

        # PAGINA 1 - INGRESAR DATOS EN EL FORMUALRIO
        # se selecciona el tipo de documento
        select_type_doc = self.driver.get_select_by_xpath("//select[@class='cuerpoVerificar']")
        select_type_doc.select_by_value(data['tipo-documento'])

        # se ingresa el número del documento
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='identificacion']"))\
            .click_and_hold()\
            .send_keys(data['cedula'])\
            .perform()

        # se da click en la opción todos
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//input[@name='radiobutton'][@value='S']"))\
            .click()\
            .perform()           

        # se resuelve el captcha de la pagina
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='txtInput']"))\
            .click_and_hold()\
            .send_keys(self.driver.get_element_by_xpath("//input[@id='txtCaptcha']").get_attribute('value'))\
            .perform()

        # se da click en el boton generar
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//div //a"))\
            .click()\
            .perform()

        # PAGINA 2 - OBTENER RESULTADO DE LA CONSULTA DE LOS ANTECEDENTES
        # se acceden a los selectores que contienen la información
        td = self.driver.get_element_by_xpath("//td[@class='Cuadro']")
        
        # se obtiene el texto del selector td
        self.text = self.text + td.text

        # se cierra el navegador
        self.driver.close_browser()