import io
import os
from typing import Union

from google.api_core import exceptions
from google.cloud.speech import SpeechClient, enums, types
from google.oauth2.service_account import Credentials


def parse_response(response: types.RecognizeResponse) -> tuple:
    """

    Args:
        response (types.RecognizeResponse) :

    Returns:
        tuple : (transcript, confidence)
    """
    transcript = []
    confidence = []
    for result in response.results:
        for alternative in result.alternatives:
            transcript.append(alternative.transcript)
            confidence.append(alternative.confidence)
    return transcript, confidence


def recognize_audio_from_uri(uri: str,
                             credential: Union[str,
                                               os.PathLike,
                                               None] = None,
                             language_code: str = 'en-US',
                             encoding: enums.RecognitionConfig.AudioEncoding = enums.RecognitionConfig.AudioEncoding.FLAC,
                             sampling_rate_hertz: int = 44100,
                             ) -> types.RecognizeResponse:
    """

    Args:
        uri (str) : Cloud
        credential (str, os.PathLike, None) :
        language_code:
        encoding (enums.RecognitionConfig.AudioEncoding) :
        sampling_rate_hertz (int) :

    Returns:
        types.RecognizeResponse
    """
    if credential is None:
        client = SpeechClient()
    else:
        credentials = Credentials.from_service_account_file(filename=credential)
        client = SpeechClient(credentials=credentials)

    config = types.RecognitionConfig(
        encoding=encoding,
        language_code=language_code,
        sample_rate_hertz=sampling_rate_hertz

    )
    audio = types.RecognitionAudio(uri=uri)

    try:
        result = client.recognize(config=config, audio=audio)
    except exceptions.InvalidArgument:
        print('cannot synchronize recognition. switched asynchronized recognition')
        operartion = client.long_running_recognize(config=config, audio=audio)
        result = operartion.result()
    return result


def recognize_audio_from_file(file: Union[str, os.PathLike],
                              credential: Union[str,
                                                os.PathLike,
                                                None] = None,
                              language_code: str = 'en-US',
                              encoding: enums.RecognitionConfig.AudioEncoding = enums.RecognitionConfig.AudioEncoding.FLAC,
                              sampling_rate_hertz: int = 44100,
                              ) -> types.RecognizeResponse:
    """

    Args:
        file (str, os.PathLike) :
        credential (str) :
        language_code (str) :
        encoding (str) :
        sampling_rate_hertz (int) :

    Returns:
        types.RecognizeResponse
    """
    if credential is None:
        client = SpeechClient()
    else:
        credentials = Credentials.from_service_account_file(filename=credential)
        client = SpeechClient(credentials=credentials)

    config = types.RecognitionConfig(
        encoding=encoding,
        language_code=language_code,
        sampling_rate_hertz=sampling_rate_hertz
    )
    with io.open(file, 'rb') as audio:
        content = audio.read()
    audio = types.RecognitionAudio(content=content)

    return client.recognize(config, audio)


class SpeechToText:
    def __init__(self, credential: Union[str, os.PathLike, None] = None):
        """

        Args:
            credential (str, os.PathLike, None) :
        """
        if credential is None:
            self.client = SpeechClient()
        else:
            credentials = Credentials.from_service_account_file(filename=credential)
            self.client = SpeechClient(credentials=credentials)

    def recognize_from_uri(
            self,
            uri: str,
            encoding: enums.RecognitionConfig.AudioEncoding = enums.RecognitionConfig.AudioEncoding.FLAC,
            language_code: str = 'en-US',
            sampling_rate_hertz: int = 44100) -> types.RecognizeResponse:
        """

        Args:
            uri (str) :
            encoding (enums.RecognitionConfig.AudioEncoding) :
            language_code (str) :
            sampling_rate_hertz (int) :

        Returns:
            types.RecognizeResponse
        """
        config = types.RecognitionConfig(
            encoding=encoding,
            language_code=language_code,
            sampling_rate_hertz=sampling_rate_hertz)
        audio = types.RecognitionAudio(uri=uri)

        return self.client.recognize(config, audio)

    def recognize_from_file(self,
                            file: Union[str, os.PathLike],
                            encoding: enums.RecognitionConfig.AudioEncoding = enums.RecognitionConfig.AudioEncoding.FLAC,
                            language_code: str = 'en-US',
                            sampling_rate_hertz: int = 44100) -> types.RecognizeResponse:
        """

        Args:
            file (str, os.PathLike) :
            encoding (enums.RecognitionConfig.AudioEncoding) :
            language_code (str) :
            sampling_rate_hertz (int) :

        Returns:
            types.RecognizeResponse
        """
        config = types.RecognitionConfig(
            encoding=encoding,
            language_code=language_code,
            sampling_rate_hertz=sampling_rate_hertz)
        with io.open(file, 'rb') as audio:
            content = audio.read()
        audio = types.RecognitionAudio(content=content)
        return self.client.recognize(config, audio)
