from pathlib import Path
from typing import Optional, NoReturn, Union

from google.cloud.texttospeech import TextToSpeechClient, enums, types


class TextToSpeech:
    def __init__(self, credential: Optional[Union[str, Path]] = None) -> NoReturn:
        if credential is None:
            self.client = TextToSpeechClient()
        else:
            self.client = TextToSpeechClient.from_service_account_file(filename=credential)

    def synthesize(self,
                   text: str,
                   language: str = 'en-US',
                   gender: int = 1,
                   encoding: enums.AudioEncoding = enums.AudioEncoding.MP3) -> types.SynthesizeSpeechResponse:
        """
        Args:
            text:
            language:
            gender:
            encoding:
        Returns:
        """
        if gender == 0:
            ssml_gender = enums.SsmlVoiceGender.FEMALE
        elif gender == 1:
            ssml_gender = enums.SsmlVoiceGender.MALE
        else:
            ssml_gender = enums.SsmlVoiceGender.NEUTRAL

        synthesis_data = types.SynthesisInput(text=text)
        voice = types.VoiceSelectionParams(language_code=language, ssml_gender=ssml_gender)
        audio_config = types.AudioConfig(audio_encoding=encoding)

        return self.client.synthesize_speech(input_=synthesis_data, voice=voice, audio_config=audio_config)

    @staticmethod
    def save(response: types.SynthesizeSpeechResponse, filename: Union[str, Path]) -> NoReturn:
        """
        Args:
            response:
            filename:
        Returns:
        """
        with open(filename, 'wb') as audio_file:
            audio_file.write(response.audio_content)