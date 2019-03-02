from pathlib import Path
from typing import Optional, Sequence, Tuple, Union

from google.api_core.gapic_v1.method import DEFAULT
from google.api_core.retry import Retry
from google.cloud.language import LanguageServiceClient, types
from google.oauth2.service_account import Credentials


class CloudLanguage:
    def __init__(self, credentials: Optional[Union[str, Path]]):
        if credentials is None:
            self.client = LanguageServiceClient()
        else:
            self.client = LanguageServiceClient(
                credentials=Credentials.from_service_account_file(credentials))

    @staticmethod
    def create_document(
            source: Optional[str] = None,
            uri: Optional[str] = None,
            language: str = 'en',
            document_type: str = 'PLANE_TEXT') -> types.Document:

        assert source is None or uri is None, f"Input sources are ambiguous. You must choose {source} or {uri}."
        assert source is not None or uri is not None, f"You choose input."

        if source is None:
            return types.Document(
                gcs_content_uri=uri,
                language=language,
                type=document_type)
        return types.Document(source, language=language, type=document_type)

    def analyze_entities(self,
                         document: Optional[Union[dict, str]],
                         uri: Optional[str] = None,
                         encoding_type: str = 'UTF32',
                         retry: Optional[Retry] = DEFAULT,
                         timeout: Optional[float] = DEFAULT,
                         metadata: Optional[Sequence[Tuple[str, str]]] = None,
                         language: str = 'en',
                         document_type: str = 'PLANE_TEXT'
                         ) -> types.AnalytizeEntitiesResponse:
        assert document is not None or uri is not None, 'You must select single input source.'
        assert document is None or uri is None, 'You must need input source.'

        if isinstance(document, str):
            document = self.create_document(
                document, language=language, document_type=document_type)
        if isinstance(uri, str):
            document = self.create_document(
                uri=uri, language=language, document_type=document_type)

        return self.client.analyze_entities(
            document=document,
            encoding_type=encoding_type,
            retry=retry,
            timeout=timeout,
            metadata=metadata)

