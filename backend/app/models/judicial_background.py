from . import Background, SolveRecaptcha

class JudicialBackground(Background):
    
    def __init__(self, driver):
        super().__init__(driver)

    def search_for_background(self, data):
        # se accede a la url del antecedente
        self.driver.load_browser(data['url'])
        
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
        div_info = self.driver.get_element_by_xpath("//section[@id='antecedentes'] //div[@class='ui-panel ui-widget ui-widget-content ui-corner-all']").text

        # se cierra el navegador
        self.driver.close_browser()

        # se añade la información obtenida a una variable
        self.text['title'] = div_info[div_info.index('La Policía Nacional de Colombia informa:'):div_info.index('Que siendo')].strip()
        self.text['message'] = div_info[div_info.index('Que siendo'):div_info.index('En cumplimiento de la Sentencia')].strip()