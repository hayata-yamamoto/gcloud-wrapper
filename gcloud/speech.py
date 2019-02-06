import os
from typing import Union

from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from google.oauth2.service_account import Credentials


def recognize_audio_from_uri(uri: str,
                             credential: Union[str,
                                               os.PathLike],
                             language_code: str = 'en-US',
                             encoding: enums.RecognitionConfig.AudioEncoding = enums.RecognitionConfig.AudioEncoding.FLAC):
    credentials = Credentials.from_service_account_file(filename=credential)
    client = speech_v1.SpeechClient(credentials=credentials)

    config = {
        'encoding': encoding,
        'sample_rate_hertz': 96000,
        'language_code': language_code}
    audio = {'uri': uri}

    return client.recognize(config, audio)

