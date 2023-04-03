from .background import Background

class MilitarySituationBackground(Background):
    
    def __init__(self, driver=None):
        super().__init__(driver)

    def search_for_background(self, data):
        # se accede a la url del antecedente judicial
        self.driver.load_browser(data['url'])
        
        # se carga el controlador de acciones de entrada de dispositivo virtualizadas
        actions = self.driver.get_action_chains()

        # INGRESAR DATOS EN EL FORMUALRIO
        # 1. se selecciona el tipo de documento
        select_type_doc = self.driver.get_select_by_xpath("//select[@id='ctl00_MainContent_drpDocumentType']")
        select_type_doc.select_by_value('100000001')

        # 2. se ingresa el número del documento
        # 3. se da click en el botón generar certificado
        actions\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='ctl00_MainContent_txtNumberDocument']"))\
            .click_and_hold()\
            .send_keys(data['cedula'])\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='ctl00_MainContent_btnGenerate']"))\
            .click()\
            .perform()

        # OBTENER RESULTADO DE LA CONSULTA DE LOS ANTECEDENTES
        actions\
            .pause(1)\
            .perform()        
        div_result = self.driver.get_element_by_xpath("//div[@id='divResult']")
        display_prop = div_result.value_of_css_property('display')

        # redacción del mensaje del antecedente con la información obtiene del sitio web        
        message = 'El ciudadano identificado con el número de documento {}, '.format(data['cedula'])

        if display_prop == 'none':
            message += 'NO TIENE DEFINIDA SU SITUACIÓN MILITAR.\n'
            message += 'Motivos:\n'
            message += '• La libreta militar no se encontró o fue expedida antes del año de 1990.\n'
            message += '• El trámite se pudo haber realizado con la tarjeta de identidad.\n'
            message += '• El ciudadano no ha terminado el proceso de definición de su situación militar.\n'
            message += '• El documento pertenece a una mujer y la ley establece que no es obligatorio el servicio militar, sino que es voluntario.'
        else:
            message += 'TIENE DEFINIDA SU SITUACIÓN MILITAR.\n'
            message += 'Datos refrentes:\n'
            message += '• Nombres y apellidos: {}\n'.format(self.driver.get_element_by_xpath("//span[@id='ctl00_MainContent_lblCitizenName']").text)
            message += '• Tipo de documento: {}\n'.format(self.driver.get_element_by_xpath("//span[@id='ctl00_MainContent_lblTypeDocumentText']").text)
            message += '• Documento: {}\n'.format(self.driver.get_element_by_xpath("//span[@id='ctl00_MainContent_lblNumberDocumentText']").text)
            message += '• Clase de libreta militar: {}'.format(self.driver.get_element_by_xpath("//span[@id='ctl00_MainContent_lblCitizenState']").text)

        # se añade la información obtenida a una variable
        self.text = message

        # se cierra el navegador
        self.driver.close_browser()  