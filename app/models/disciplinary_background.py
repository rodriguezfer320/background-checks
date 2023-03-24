from .background import Background
from ..models.solve_captcha import SolveCaptcha
from os import getcwd, remove
import PyPDF2

class DisciplinaryBackground(Background):
    
    def __init__(self, driver=None):
        super().__init__(driver)

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
        captcha = SolveCaptcha()
        captcha.driver = self.driver
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
            
            # se añade la información obtenida a una variable
            self.text = div_info.text + 'POR LO TANTO, SE CONCLUYE QUE CIUDADANO {} NO REGISTRA SANCIONES NI INHABILIDADES VIGENTES.'.format(data['cedula'])
        except:
            # PÁGINA 2 - DESCARGAR CERTIFICADO EN FORMATO PDF
            # se mueve el foco a la ventana que contiene el botón
            actions\
                .pause(1)\
                .perform()
            self.driver.change_frame_by_css_selector("iframe[class='embed-responsive-item'][src^='https://apps.procuraduria.gov.co/webcert/inicio.aspx?']")
            actions\
                .pause(1)\
                .perform()

            # se da click en el botón descargar
            actions\
                .pause(2)\
                .move_to_element(self.driver.get_element_by_xpath("//input[@id='btnDescargar']"))\
                .click()\
                .pause(5)\
                .perform()

            # se obtiene el texto del archivo pdf
            path_pdf = getcwd() + f'\\app\\static\\pdf\\Certificado.pdf'

            with open(path_pdf, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfFileReader(pdf_file)
                extract_text = pdf_reader.getPage(0).extractText().strip()
                message = extract_text[1748:1812] + '\n\n'
                message += extract_text[0:342]

            # se elimina el archivo pdf descargado
            remove(path_pdf)

            # se añade la información obtenida a una variable
            self.text = message

        # se cierra el navegador
        self.driver.close_browser()