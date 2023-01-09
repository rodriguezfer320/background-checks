from ..models.background import Background
from .solve_recaptcha import SolveRecaptcha

class FiscalBackground(Background):
    
    def __init__(self, driver=None):
        super().__init__(driver)

    def search_for_background(self, data):
        # se accede a la url del antecedente
        self.driver.load_browser(data['url'])
        
        actions = self.driver.get_action_chains()

        # PÁGINA 1 - INGRESAR DATOS EN EL FORMUALRIO
        # se mueve el foco a la ventana Certificado Para Personas Naturales
        self.driver.change_frame_by_css_selector("iframe[src^='https://cfiscal.contraloria.gov.co/Certificados/CertificadoPersonaNatural.aspx']")

        # se selecciona el tipo de documento
        actions\
            .pause(2)\
            .perform()   
        select_type_doc = self.driver.get_select_by_xpath("//select[@id='ddlTipoDocumento']")
        select_type_doc.select_by_value(data['tipo-documento'])

        # se ingresa el número del documento
        actions\
            .pause(2)\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='txtNumeroDocumento']"))\
            .pause(1)\
            .click_and_hold()\
            .pause(1)\
            .send_keys(data['cedula'])\
            .perform()

        # se resuelve el recaptcha de la pagina
        recaptcha = SolveRecaptcha()
        recaptcha.driver = self.driver
        recaptcha.solve_by_audio(False)

        # se da click en el boton consultar
        actions\
            .pause(2)\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='btnBuscar']"))\
            .pause(1)\
            .click()\
            .pause(5)\
            .perform()

        self.text = "pdf descargado"

        # se cierra el navegador
        self.driver.close_browser()