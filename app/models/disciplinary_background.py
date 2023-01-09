from .background import Background
from ..models.solve_captcha import SolveCaptcha

class DisciplinaryBackground(Background):
    
    def __init__(self, driver=None):
        super().__init__(driver)

    def search_for_background(self, data):
        # se accede a la url del antecedente
        self.driver.load_browser(data['url'])
        
        actions = self.driver.get_action_chains()

        # se mueve el foco a la ventana de los campos
        self.driver.change_frame_by_css_selector("iframe[class='embed-responsive-item'][src^='https://apps.procuraduria.gov.co/webcert/inicio.aspx?']")

        # INGRESAR DATOS EN EL FORMUALRIO
        # se selecciona el tipo de documento
        select_type_doc = self.driver.get_select_by_xpath("//select[@id='ddlTipoID']")
        select_type_doc.select_by_value(data['tipo-documento'])

        # se ingresa el número del documento
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='txtNumID']"))\
            .click_and_hold()\
            .send_keys(data['cedula'])\
            .perform()

        # se da click en la opción ordinario
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='rblTipoCert_0']"))\
            .click()\
            .perform()           

        # se resuelve el captcha de la pagina
        captcha = SolveCaptcha()
        captcha.driver = self.driver
        captcha.solve_by_question(data['cedula'])

        # se da click en el boton generar
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='btnExportar']"))\
            .click()\
            .perform()

        # OBTENER RESULTADO DE LA CONSULTA DE LOS ANTECEDENTES
        # se acceden a los selectores que contienen la información
        actions\
            .pause(2)\
            .perform()
        div = self.driver.get_element_by_xpath("//div[@id='ValidationSummary1']")
        
        # se obtiene el texto del selector div
        self.text = self.text + div.text

        # se cierra el navegador
        self.driver.close_browser()