from .background import Background
from .solve_recaptcha import SolveRecaptcha
from os import getcwd, remove
import PyPDF2

class FiscalBackground(Background):
    
    def __init__(self, driver=None):
        super().__init__(driver)

    def search_for_background(self, data):
        # se accede a la url del antecedente
        self.driver.load_browser(data['url'])
        
        # se carga el controlador de acciones de entrada de dispositivo virtualizadas
        actions = self.driver.get_action_chains()

        # PÁGINA 1 - INGRESAR DATOS EN EL FORMUALRIO
        # se mueve el foco a la ventana Certificado Para Personas Naturales
        self.driver.change_frame_by_css_selector("iframe[src^='https://cfiscal.contraloria.gov.co/Certificados/CertificadoPersonaNatural.aspx']")

        # 1. se selecciona el tipo de documento
        actions\
            .pause(2)\
            .perform()   
        select_type_doc = self.driver.get_select_by_xpath("//select[@id='ddlTipoDocumento']")
        select_type_doc.select_by_value('CC')

        # 2. se ingresa el número del documento
        actions\
            .pause(2)\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='txtNumeroDocumento']"))\
            .click_and_hold()\
            .send_keys(data['cedula'])\
            .perform()

        # 3. se resuelve el recaptcha de la pagina
        recaptcha = SolveRecaptcha()
        recaptcha.driver = self.driver
        recaptcha.solve_by_audio(False)

        # 4. se da click en el botón consultar
        actions\
            .pause(2)\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='btnBuscar']"))\
            .click()\
            .pause(5)\
            .perform()
        
        # se cierra el navegador
        self.driver.close_browser()
        
        # se obtiene el texto del archivo pdf
        path_pdf = getcwd() + f'\\app\\static\\pdf\\{data["cedula"]}.pdf'

        with open(path_pdf, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            extract_text = pdf_reader.getPage(0).extractText().strip()

            message = extract_text[0:363]  + '\n'
            message += extract_text[738:753] + ':' + extract_text[753:775]
            message += extract_text[775:793] + ':' + extract_text[793:804]
            message += extract_text[803:827] + ':' + extract_text[827:850] + '\n\n'
            message += extract_text[366:729]

        # se elimina el archivo pdf descargado
        remove(path_pdf)

        # se añade la información obtenida a una variable
        self.text = message