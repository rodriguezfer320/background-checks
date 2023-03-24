from urllib.request import urlretrieve
from urllib.error import HTTPError
from os import getcwd
import speech_recognition as sr, soundfile as sf

class SolveRecaptcha:

    def __init__(self, driver=None):
        self._driver = driver
        self._path_audio = getcwd() + '\\app\\static\\audio_recaptcha\\audio.{}'

    def solve_by_audio(self, default=True): 
        if not self.solve_check_box(default, True):
            # se carga el controlador de acciones de entrada de dispositivo virtualizadas
            actions = self.driver.get_action_chains()
            
            # se mueve el foco a la ventana del desafio por imagenes
            self.driver.change_frame_by_css_selector("iframe[name^='c-'][src^='https://www.google.com/recaptcha/api2/bframe?']")

            # se da click el botón del dasafio por audio
            actions\
                .pause(2)\
                .move_to_element(self.driver.get_element_by_xpath("//button[@id='recaptcha-audio-button']"))\
                .click()\
                .perform()

            # se verifica que el desafio ha sido superado
            while not self.solve_check_box(True, False):
                # se mueve el foco a la venatana del desafio por audio
                self.driver.change_frame_by_css_selector("iframe[name^='c-'][src^='https://www.google.com/recaptcha/api2/bframe?']")

                # se obtiene la url del audio del desafio
                actions\
                    .pause(2)\
                    .perform()
                src = self.driver.get_element_by_xpath("//a[@class='rc-audiochallenge-tdownload-link']").get_attribute('href')

                solution_text = ''
                try:
                    # se descarga el audio del desafio
                    self.download_audio_test_recapcha(src)

                    # se obtiene el texto del audio del desafio
                    solution_text = self.speech_to_text()
                except (HTTPError, sr.UnknownValueError):
                    # se busca otro desafio de audio
                    actions\
                        .pause(2)\
                        .move_to_element(self.driver.get_element_by_xpath("//button[@class='rc-button goog-inline-block rc-button-reload']"))\
                        .click()\
                        .perform()
                    continue
            
                # se ingresa el texto obtenido del audio
                # se da click en el botón de verificar
                actions\
                    .pause(2)\
                    .move_to_element(self.driver.get_element_by_xpath("//input[@id='audio-response']"))\
                    .click_and_hold()\
                    .send_keys(solution_text)\
                    .move_to_element(self.driver.get_element_by_xpath("//button[@id='recaptcha-verify-button']"))\
                    .click()\
                    .perform()

        # se mueve el foco al body
        self.driver.change_frame_by_css_selector("body")

    def solve_check_box(self, default, click):
        # se mueve el foco a la ventana del checkbox
        self.driver.change_frame_by_css_selector("iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']", default)
        check_box = self.driver.get_element_by_xpath("//span[@id='recaptcha-anchor']")

        # se da click en el checkbox
        if click:
            self.driver.get_action_chains()\
                .pause(2)\
                .move_to_element(check_box)\
                .click()\
                .perform()
        
        # se verifica si el recaptcha fue resuelto
        return check_box.get_attribute('aria-checked') == 'true'

    def download_audio_test_recapcha(self, src):
        # se descarga el archivo de audio
        urlretrieve(src, self._path_audio.format('mp3'))

        # se lee el archivo de audio 
        data, sample_rate = sf.read(self._path_audio.format('mp3'))

        # se convierte al archivo de audio de .mp3 a .wav
        sf.write(self._path_audio.format('wav'), data, sample_rate)

    def speech_to_text(self):
        # se carga el archivo de audio
        sample_audio = sr.AudioFile(self._path_audio.format('wav'))

        # se inicia el reconocedor de audio
        recognizer = sr.Recognizer()

        # se inicia la conversión de audio a texto
        with sample_audio as source:
            # se obtiene la información del audio
            audio = recognizer.record(source)

            # se reconoce el texto del audio
            text = recognizer.recognize_google(audio, language='es-ES')

        return text

    #Getters
    @property
    def driver(self):
        return self._driver

    #Setters
    @driver.setter
    def driver(self, driver):
        self._driver = driver