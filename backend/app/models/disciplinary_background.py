from . import Background, SolveCaptcha
from os import remove
import PyPDF2

class DisciplinaryBackground(Background):

    def __init__(self, driver=None):
        super().__init__(driver)
        self.path_pdf = driver.dir_download + 'Certificado.pdf'

    def search_for_background(self, data):
        # se accede a la url del antecedente
        self.driver.load_browser(data['url'])

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
            .send_keys(data['cedula'])\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='rblTipoCert_0']"))\
            .click()\
            .perform()

        # 3. se resuelve el captcha de la página
        captcha = SolveCaptcha(self.driver)
        captcha.solve_by_question(data['cedula'])

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

            # se cierra el navegador
            self.driver.close_browser()
            
            # se añade la información obtenida a una variable
            self.text['message'] = 'El ciudadano con Cédula de ciudadanía Número {}. NO REGISTRA SANCIONES NI INHABILIDADES VIGENTES'.format(data['cedula'])
        except:
            # PÁGINA 2 - DESCARGAR CERTIFICADO EN FORMATO PDF
            # se mueve el foco a la ventana que contiene el botón
            actions\
                .pause(2)\
                .perform()
            self.driver.change_frame_by_css_selector("iframe[class='embed-responsive-item'][src^='https://apps.procuraduria.gov.co/webcert/inicio.aspx?']")

            # se da click en el botón descargar
            actions\
                .pause(1)\
                .move_to_element(self.driver.get_element_by_xpath("//input[@id='btnDescargar']"))\
                .click()\
                .pause(5)\
                .perform()

            # se cierra el navegador
            self.driver.close_browser()

            # se obtiene el texto del archivo pdf
            with open(self.path_pdf, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                extract_text = pdf_reader.getPage(0).extractText()
                title = extract_text[extract_text.index('CERTIFICADO ORDINARIO'):extract_text.index('WEB')].strip()
                date = extract_text[extract_text.index('Bogotá DC'):extract_text.index('La PROCURADURIA GENERAL DE LA NACIÓN')].strip()
                message = extract_text[extract_text.index('La PROCURADURIA GENERAL DE LA NACIÓN'):extract_text.index('ADVERTENCIA:')].strip() + '.'

            # se elimina el archivo pdf descargado
            remove(self.path_pdf)

            # se añade la información obtenida a una variable
            self.text['title'] = title
            self.text['date'] = date
            self.text['message'] = message