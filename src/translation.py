import deepl

from .util import get_config


class Translator:

    def __init__(self,source_language,target_language):
        self.source_language = source_language
        self.target_language = target_language

        # Deepl
        auth_key = get_config()["deepl"]["api_key"]
        self.translator = deepl.Translator(auth_key)

    def translate(self,phrase):
        """ Translate given phrase with deepl
        return the translation
        """
        #Translate with deepl
        result = self.translator.translate_text(phrase, source_lang=self.source_language,target_lang=self.target_language)
        return result.text
