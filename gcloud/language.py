from pathlib import Path
from typing import Optional, Sequence, Tuple, Union

from google.api_core.gapic_v1.method import DEFAULT
from google.api_core.retry import Retry
from google.cloud.language import LanguageServiceClient, types
from google.cloud.language.enums import Document, EncodingType


class CloudLanguage:
    def __init__(self, credentials: Optional[Union[str, Path]]):
        if credentials is None:
            self.client = LanguageServiceClient()
        else:
            self.client = LanguageServiceClient.from_service_account_file(filename=credentials)

    def annotate_text_from_string(
            self,
            content: str,
            encoding_type: str = EncodingType.UTF32,
            retry: Optional[Retry] = DEFAULT,
            timeout: Optional[float] = DEFAULT,
            metadata: Optional[Sequence[Tuple[str, str]]] = None,
            language: str = 'en',
            document_type: str = Document.Type.PLAIN_TEXT,
            syntax: bool = True,
            entities: bool = True,
            document_sentiment: bool = True,
            entity_sentiment: bool = True,
            classify: bool = True) -> types.AnnotateTextResponse:
        """
        Args:
            content:
            encoding_type:
            retry:
            timeout:
            metadata:
            language:
            document_type:
            syntax:
            entities:
            document_sentiment:
            entity_sentiment:
            classify:
        Returns:
        """

        features = {"extractSyntax": syntax,
                    "extractEntities": entities,
                    "extractDocumentSentiment": document_sentiment,
                    "extractEntitySentiment": entity_sentiment,
                    "classifyText": classify
                    }

        document = types.Document(content=content, language=language, type=document_type)

        return self.client.annotate_text(
            document=document,
            features=features,
            encoding_type=encoding_type,
            retry=retry,
            timeout=timeout,
            metadata=metadata)