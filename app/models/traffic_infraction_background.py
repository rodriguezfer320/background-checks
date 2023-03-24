from .background import Background

class TrafficInfractionBackground(Background):
    
    def __init__(self, driver=None):
        super().__init__(driver)

    def search_for_background(self, data):
        # se accede a la url del antecedente
        self.driver.load_browser(data['url'])
        
        # se carga el controlador de acciones de entrada de dispositivo virtualizadas
        actions = self.driver.get_action_chains()

        # acciones para consultar la información
        # 1. se ingresa el número del documento en el campo de búsqueda
        # 2. se da click en botón de buscar (icono de una lupa)
        actions\
            .pause(10)\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='txtBusqueda']"))\
            .click_and_hold()\
            .send_keys(data['cedula'])\
            .move_to_element(self.driver.get_element_by_xpath("//button[@id='consultar']"))\
            .click()\
            .perform()

        # se obtiene la información consultada en la página
        try: div_abstract = self.driver.get_element_by_xpath("//div[@class='card bg-estado-section border-0 box-shadow-sm']")
        except: div_abstract = self.driver.get_element_by_xpath("//div[@id='resumenEstadoCuenta']")
        finally: info = div_abstract.text.split('\n')

        # se cierra el navegador
        self.driver.close_browser()

        # cantidad de multas y comparendos que presenta el candidato
        comparendos = int(info[1].split(' ')[1])
        fines = int(info[2].split(' ')[1])

        # redacción del mensaje del antecedente con la información obtiene del sitio web        
        message = 'El ciudadano identificado con el número de documento {}, '.format(data['cedula'])
        
        if fines > 0:
            message += 'posee {} multa(s) a la fecha pendientes de pago'.format(fines)
        else:
            message += 'no posee a la fecha pendientes de pago por concepto de multas'
        
        if comparendos > 0:
            message += ' y' if fines > 0 else ', pero'
            message += ' tiene {} comparendo(s)'.format(comparendos)
        else:
            message += ' y no tiene comparendos'

        message +=  ' registrado(s) en los Organismos de Tránsito conectados a Simit.'

        if fines > 0 or comparendos > 0:
            message += '\nPara más información sobre las multas y/o comparendos que presenta el candidato '
            message += 'consulte el siguiente link: https://www.fcm.org.co/simit/#/estado-cuenta?numDocPlacaProp={}'.format(data['cedula'])

        # se añade la información obtenida a una variable
        self.text = message