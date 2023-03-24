class SolveCaptcha:

    def __init__(self, driver=None):
        self._driver = driver

    def solve_by_question(self, document):
        questions = {
            '¿Escriba los tres primeros digitos del documento a consultar?': document[0:3],  
            '¿Escriba los dos ultimos digitos del documento a consultar?': document[-2:],
            '¿ Cual es la Capital del Vallle del Cauca?': 'cali',
            '¿ Cual es la Capital del Atlantico?': 'barranquilla',
            '¿ Cual es la Capital de Colombia (sin tilde)?': 'bogota',
            '¿ Cual es la Capital de Antioquia (sin tilde)?': 'medellin'
        }

        # se carga el controlador de acciones de entrada de dispositivo virtualizadas
        actions = self.driver.get_action_chains()

        while True:
            question = self.driver.get_element_by_xpath("//span[@id='lblPregunta']").text
            result = None

            if question.startswith("Cuanto es", 2, 11):
                data = question.split(' ')
                a = int(data[3].strip())
                b = int(data[5].strip())

                if data[4] == '+': result = a + b
                elif data[4] == '-': result = a - b
                elif data[4] == 'X': result = a * b
                elif b > 0: result = a / b
            else:
                for (key, value) in questions.items():
                    if question == key:
                        result = value
                        break

            if result is None:
                # se busca una nueva pregunta
                actions\
                    .move_to_element(self.driver.get_element_by_xpath("//input[@id='ImageButton1']"))\
                    .click()\
                    .perform()
            else:
                # se ingresa la respuesta de la pregunta
                actions\
                    .move_to_element(self.driver.get_element_by_xpath("//input[@id='txtRespuestaPregunta']"))\
                    .click_and_hold()\
                    .send_keys(str(result))\
                    .perform()
                break
    
    #Getters
    @property
    def driver(self):
        return self._driver

    #Setters
    @driver.setter
    def driver(self, driver):
        self._driver = driver