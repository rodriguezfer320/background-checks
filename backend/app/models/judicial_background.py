from .background_web import BackgroundWeb
from .solve_recaptcha import SolveRecaptcha

class JudicialBackground(BackgroundWeb):
    
    def __init__(self, driver, description):
        super().__init__(driver, description)

    def get_background_information(self, data):
        # se accede a la url del antecedente
        self.driver.load_browser(data['background'].url)
        
        # se carga el controlador de acciones de entrada de dispositivo virtualizadas
        actions = self.driver.get_action_chains()

        # PÁGINA 1 - TÉRMINOS DE USO
        # 1. se da click en la opción aceptar
        # 2. se da click en el botón enviar
        actions\
            .pause(2)\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='aceptaOption:0']"))\
            .click()\
            .move_to_element(self.driver.get_element_by_xpath("//button[@id='continuarBtn']"))\
            .click()\
            .perform()

        # PÁGINA 2 - INGRESAR DATOS EN EL FORMUALRIO
        # 1. se ingresa el número del documento
        actions\
            .pause(2)\
            .move_to_element(self.driver.get_element_by_xpath("//input[@id='cedulaInput']"))\
            .click_and_hold()\
            .send_keys(data['document'])\
            .perform()

        # 2. se selecciona el tipo de documento
        select_type_doc = self.driver.get_select_by_xpath("//select[@id='cedulaTipo']")
        select_type_doc.select_by_value('cc')

        # 3. se resuelve el recaptcha de la pagina
        recaptcha = SolveRecaptcha(self.driver, self.dir_download)
        recaptcha.solve_by_audio()

        # 4. se da click en el botón consultar
        actions\
            .pause(2)\
            .move_to_element(self.driver.get_element_by_xpath("//button[@id='j_idt17']"))\
            .click()\
            .perform()

        # PÁGINA 3 - OBTENER RESULTADO DE LA CONSULTA DE LOS ANTECEDENTES
        # se accede al selector que contiene la información
        actions\
            .pause(2)\
            .perform()
        div = self.driver.get_element_by_xpath("//section[@id='antecedentes'] //div[@class='ui-panel ui-widget ui-widget-content ui-corner-all']")
        self._data_web = div.text

        # se cierra el navegador
        self.driver.close_browser()

    def process_information(self, data):
        # se añade la información obtenida a una variable
        self.description['title'] = self._data_web[self._data_web.index('La Policía Nacional de Colombia informa:'):self._data_web.index('Que siendo')].strip()
        self.description['message'] = self._data_web[self._data_web.index('Que siendo'):self._data_web.index('En cumplimiento de la Sentencia')].strip()