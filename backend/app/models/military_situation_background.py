from .background_web import BackgroundWeb

class MilitarySituationBackground(BackgroundWeb):
    
    def __init__(self, driver, description):
        super().__init__(driver, description)

    def get_background_information(self, data):
        # se accede a la url del antecedente judicial
        self.driver.load_browser(data['background'].url)
        
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
            .send_keys(data['document'])\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='ctl00_MainContent_btnGenerate']"))\
            .click()\
            .perform()

        # OBTENER RESULTADO DE LA CONSULTA DE LOS ANTECEDENTES
        actions\
            .pause(1)\
            .perform()        
        div_result = self.driver.get_element_by_xpath("//div[@id='divResult']")
        display_prop = div_result.value_of_css_property('display')
        
        if display_prop != 'none':
            self._data_web = [
                self.driver.get_element_by_xpath("//span[@id='ctl00_MainContent_lblCitizenName']").text,
                self.driver.get_element_by_xpath("//span[@id='ctl00_MainContent_lblTypeDocumentText']").text,
                self.driver.get_element_by_xpath("//span[@id='ctl00_MainContent_lblNumberDocumentText']").text,
                self.driver.get_element_by_xpath("//span[@id='ctl00_MainContent_lblCitizenState']").text
            ]     

        # se cierra el navegador
        self.driver.close_browser()

    def process_information(self, data):
        # redacción del mensaje del antecedente con la información obtiene del sitio web        
        message = f'El ciudadano identificado con el número de documento {data["document"]}, '
        dataDoc = ''
        
        if self._data_web:
            message += 'TIENE DEFINIDA SU SITUACIÓN MILITAR.'
            dataDoc = 'Datos referentes:\n'
            dataDoc += f'• Nombres y apellidos: {self._data_web[0]}\n'
            dataDoc += f'• Tipo de documento: {self._data_web[1]}\n'
            dataDoc += f'• Documento: {self._data_web[2]}\n'
            dataDoc += f'• Clase de libreta militar: {self._data_web[3]}'        
        else:
            message += 'NO TIENE DEFINIDA SU SITUACIÓN MILITAR.'
            dataDoc = 'Motivos:\n'
            dataDoc += '• La libreta militar no se encontró o fue expedida antes del año de 1990.\n'
            dataDoc += '• El trámite se pudo haber realizado con la tarjeta de identidad.\n'
            dataDoc += '• El ciudadano no ha terminado el proceso de definición de su situación militar.\n'
            dataDoc += '• El documento pertenece a una mujer y la ley establece que no es obligatorio el servicio militar, sino que es voluntario.'

        # se añade la información obtenida a una variable
        self.description['title'] = 'FUERZAS MILITARES DE COLOMBIA - COMANDO DE RECLUTAMIENTO Y CONTROL RESERVAS'
        self.description['message'] = message
        self.description['data'] = dataDoc