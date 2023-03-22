from ..models.background import Background
from ..models.solve_recaptcha import SolveRecaptcha

class JudicialBackground(Background):
    
    def __init__(self, driver=None):
        super().__init__(driver)

    def search_for_background(self, data):
        # se accede a la url del antecedente
        self.driver.load_browser(data['url'])
        
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
            .send_keys(data['cedula'])\
            .perform()

        # se selecciona el tipo de documento
        actions\
            .pause(2)\
            .perform()
        select_type_doc = self.driver.get_select_by_xpath("//select[@id='cedulaTipo']")
        select_type_doc.select_by_value(data['tipo-documento'])

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
        
        actions\
            .pause(2)\
            .perform()
            
        # se obtiene el texto de los selectores span
        for element in spans:
            self.text = self.text + element.text

        # se cierra el navegador
        self.driver.close_browser()