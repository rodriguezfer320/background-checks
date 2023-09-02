from .background_web import BackgroundWeb
from .solve_captcha import SolveCaptcha
from os import remove
import PyPDF2, re

class DisciplinaryBackground(BackgroundWeb):

    def __init__(self,  driver, description):
        super().__init__(driver, description)

    def get_background_information(self, data):
        # se accede a la url del antecedente
        self.driver.load_browser(data['background'].url)
        
        # se carga el controlador de acciones de entrada de dispositivo virtualizadas
        actions = self.driver.get_action_chains()

        # se mueve el foco a la ventana del formulario
        self.driver.change_frame_by_css_selector("iframe[class='embed-responsive-item'][src^='https://apps.procuraduria.gov.co/webcert/inicio.aspx?']")

        # INGRESAR DATOS EN EL FORMUALRIO
        # 1. se selecciona el tipo de documento
        select_type_doc = self.driver.get_select_by_xpath("//select[@id='ddlTipoID']")
        select_type_doc.select_by_value('1')

        # 2. se ingresa el número del documento
        # 3. se da click en la opción ordinario
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='txtNumID']"))\
            .click_and_hold()\
            .send_keys(data['document'])\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='rblTipoCert_0']"))\
            .click()\
            .perform()

        # 3. se resuelve el captcha de la página
        captcha = SolveCaptcha(self.driver)
        captcha.solve_by_question(data['document'])

        # 3. se da click en el botón generar
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='btnExportar']"))\
            .click()\
            .perform()

        # OBTENER RESULTADO DE LA CONSULTA DE LOS ANTECEDENTES
        try:
            # se acceden a los selectores que contienen la información
            actions\
                .pause(1)\
                .perform()
            div_info = self.driver.get_element_by_xpath("//div[@id='ValidationSummary1']")

            # se lanza exception si falla el assert
            assert div_info.text == 'EL NÚMERO DE IDENTIFICACIÓN INGRESADO NO SE ENCUENTRA REGISTRADO EN EL SISTEMA.'
        
            self._data_web = ''
        except:
            # PÁGINA 2 - DESCARGAR CERTIFICADO EN FORMATO PDF
            # se da click en el botón descargar
            actions\
                .pause(1)\
                .move_to_element(self.driver.get_element_by_xpath("//input[@id='btnDescargar']"))\
                .click()\
                .pause(5)\
                .perform()
        finally:
            # se cierra el navegador
            self.driver.close_browser()            

    def process_information(self, data):
        if self._data_web:
            # se añade la información obtenida a una variable
            self.description['message'] = 'El ciudadano con Cédula de ciudadanía Número {}. NO REGISTRA SANCIONES NI INHABILIDADES VIGENTES'.format(data['cedula'])
        else:
            path_pdf = self.dir_download + 'Certificado.pdf'
            
            try:
                # se obtiene el texto del archivo pdf
                with open(path_pdf, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                    extract_text = pdf_reader.getPage(0).extractText()
                    title_end_index = 'WEB' if re.search('WEB', extract_text) else 'PIB'
                    title = extract_text[extract_text.index('CERTIFICADO ORDINARIO'):extract_text.index(title_end_index)].strip()
                    date = extract_text[extract_text.index('Bogotá DC'):extract_text.index('La PROCURADURIA GENERAL DE LA NACIÓN')].strip()
                    message = extract_text[extract_text.index('La PROCURADURIA GENERAL DE LA NACIÓN'):extract_text.index('ADVERTENCIA:')].strip() + '.'

                # se añade la información obtenida a una variable
                self.description['title'] = title
                self.description['date'] = date
                self.description['message'] = message                
            except:
                raise Exception('Error al procesar la información del antecedente disciplinario')
            finally:
                # se elimina el archivo pdf descargado
                remove(path_pdf)