from pathlib import Path
from typing import Optional, Sequence, Tuple, Union

from google.api_core.gapic_v1.method import DEFAULT
from google.api_core.retry import Retry
from google.cloud.language import LanguageServiceClient, types
from google.cloud.language.enums import Document, EncodingType
from google.oauth2.service_account import Credentials


class CloudLanguage:
    def __init__(self, credentials: Optional[Union[str, Path]]):
        if credentials is None:
            self.client = LanguageServiceClient()
        else:
            self.client = LanguageServiceClient(credentials=Credentials.from_service_account_file(credentials))

    def analyze_entities_from_string(self,
                                     content: str,
                                     encoding_type: str = EncodingType.UTF32,
                                     retry: Optional[Retry] = DEFAULT,
                                     timeout: Optional[float] = DEFAULT,
                                     metadata: Optional[Sequence[Tuple[str, str]]] = None,
                                     language: str = 'en',
                                     type: str = Document.Type.PLAIN_TEXT) -> types.AnalytizeEntitiesResponse:
        """

        Args:
            content:
            encoding_type:
            retry:
            timeout:
            metadata:
            language:
            type:

        Returns:

        """
        document = types.Document(content=content, language=language, type=type)

        return self.client.analyze_entities(
            document=document,
            encoding_type=encoding_type,
            retry=retry,
            timeout=timeout,
            metadata=metadata)

    def analyze_entities_from_uri(self,
                                  uri: str,
                                  encoding_type: str = EncodingType.UTF32,
                                  retry: Optional[Retry] = DEFAULT,
                                  timeout: Optional[float] = DEFAULT,
                                  metadata: Optional[Sequence[Tuple[str, str]]] = None,
                                  language: str = 'en',
                                  type: str = Document.Type.PLAIN_TEXT) -> types.AnalytizeEntitiesResponse:
        """

        Args:
            uri:
            encoding_type:
            retry:
            timeout:
            metadata:
            language:
            type:

        Returns:

        """
        document = types.Document(gcs_content_uri=uri, language=language, type=type)

        return self.client.analyze_entities(
            document=document,
            encoding_type=encoding_type,
            retry=retry,
            timeout=timeout,
            metadata=metadata)
