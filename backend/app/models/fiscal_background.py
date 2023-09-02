from .background_web import BackgroundWeb
from .solve_recaptcha import SolveRecaptcha
from os import remove
import PyPDF2

class FiscalBackground(BackgroundWeb):
    
    def __init__(self, driver, description):
        super().__init__(driver, description)

    def get_background_information(self, data):
        # se accede a la url del antecedente
        self.driver.load_browser(data['background'].url)
        
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

    def process_information(self, data):
        path_pdf = self.dir_download + f'{data["document"]}.pdf'
        
        try:
            # se obtiene el texto del archivo pdf
            with open(path_pdf, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                extract_text = pdf_reader.getPage(0).extractText().strip()
                title = extract_text[extract_text.index('LA CONTRALORÍA'):extract_text.index('Que una vez consultado')].strip()
                message = extract_text[extract_text.index('Que una vez consultado'):extract_text.index('Esta Certificación es válida')].strip()
                dataDoc = extract_text[extract_text.index('Tipo Documento'):extract_text.index('Generó: WEB')].strip()

            # se añade la información obtenida a una variable
            self.description['title'] = title
            self.description['message'] = message
            self.description['data'] = dataDoc                
        except:
            raise Exception('Error al procesar la información del antecedente fiscal')
        finally:
            # se elimina el archivo pdf descargado
            remove(path_pdf) 