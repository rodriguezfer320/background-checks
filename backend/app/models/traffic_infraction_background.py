from .background_web import BackgroundWeb

class TrafficInfractionBackground(BackgroundWeb):
    
    def __init__(self, driver, description):
        super().__init__(driver, description)

    def get_background_information(self, data):
        # se accede a la url del antecedente
        self.driver.load_browser(data['background'].url)
        
        # se carga el controlador de acciones de entrada de dispositivo virtualizadas
        actions = self.driver.get_action_chains()

        # acciones para consultar la información
        # 1. se ingresa el número del documento en el campo de búsqueda
        # 2. se da click en botón de buscar (icono de una lupa)
        actions\
            .pause(10)\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='txtBusqueda']"))\
            .click_and_hold()\
            .send_keys(data['document'])\
            .move_to_element(self.driver.get_element_by_xpath("//button[@id='consultar']"))\
            .click()\
            .perform()

        actions\
            .pause(2)\
            .perform()

        # se obtiene la información consultada en la página
        try: div_abstract = self.driver.get_element_by_xpath("//div[@class='card bg-estado-section border-0 box-shadow-sm']")
        except: div_abstract = self.driver.get_element_by_xpath("//div[@id='resumenEstadoCuenta']")
        finally: self._data_web = div_abstract.text.split('\n')

        # se cierra el navegador
        self.driver.close_browser()        

    def process_information(self, data):
        # cantidad de multas y comparendos que presenta el candidato
        comparendos = int(self._data_web[1].split(' ')[1])
        fines = int(self._data_web[2].split(' ')[1])

        # redacción del mensaje del antecedente con la información obtiene del sitio web        
        message = f'El ciudadano identificado con el número de documento {data["document"]}, '
        
        if fines > 0:
            message += f'posee {fines} multa(s) a la fecha pendientes de pago'
        else:
            message += 'no posee a la fecha pendientes de pago por concepto de multas'
        
        if comparendos > 0:
            message += ' y' if fines > 0 else ', pero'
            message += f' tiene {comparendos} comparendo(s)'
        else:
            message += ' y no tiene comparendos'

        message +=  ' registrado(s) en los Organismos de Tránsito conectados a Simit. '

        if fines > 0 or comparendos > 0:
            message += '\nPara más información sobre las multas y/o comparendos que presenta el candidato '
            message += f'consulte el siguiente link: https://www.fcm.org.co/simit/#/estado-cuenta?numDocPlacaProp={data["document"]}'

        # se añade la información obtenida a una variable
        self.description['title'] = 'Sistema Integrado de información sobre multas y sanciones por infracciones de tránsito'
        self.description['message'] = message