from . import Background, SolveRecaptcha
from os import remove
import PyPDF2

class FiscalBackground(Background):
    
    def __init__(self, driver):
        super().__init__(driver)
        self.path_pdf = self.dir_download + '{filename}.pdf'

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
            .send_keys(data['document'])\
            .perform()

        # 3. se resuelve el recaptcha de la pagina
        recaptcha = SolveRecaptcha(self.driver, self.dir_download)
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
        with open(self.path_pdf.format(filename=data["document"]), 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            extract_text = pdf_reader.getPage(0).extractText().strip()
            title = extract_text[extract_text.index('LA CONTRALORÍA'):extract_text.index('Que una vez consultado')].strip()
            message = extract_text[extract_text.index('Que una vez consultado'):extract_text.index('Esta Certificación es válida')].strip()
            dataDoc = extract_text[extract_text.index('Tipo Documento'):extract_text.index('Generó: WEB')].strip()

        # se elimina el archivo pdf descargado
        remove(self.path_pdf.format(filename=data["document"]))

        # se añade la información obtenida a una variable
        self.text['title'] = title
        self.text['message'] = message
        self.text['data'] = dataDoc