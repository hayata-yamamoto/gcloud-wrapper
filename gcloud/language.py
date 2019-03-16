import json
from pathlib import Path
from typing import Optional, Sequence, Tuple, Union, Dict, List, Mapping

from google.api_core.retry import Retry
from google.cloud.language import LanguageServiceClient, types, enums
from google.protobuf.json_format import MessageToJson


class CloudLanguage:
    def __init__(self, credentials: Optional[Union[str, Path]] = None) -> None:
        if credentials is None:
            self.client = LanguageServiceClient()
        else:
            self.client = LanguageServiceClient.from_service_account_file(filename=credentials)

    def annotate_text_from_string(
            self,
            content: str,
            encoding_type: str = enums.EncodingType.UTF32,
            retry: Optional[Retry] = None,
            timeout: Optional[float] = None,
            metadata: Optional[Sequence[Tuple[str, str]]] = None,
            language: str = "en",
            document_type: str = enums.Document.Type.PLAIN_TEXT,
            syntax: bool = True,
            entities: bool = True,
            document_sentiment: bool = True,
            entity_sentiment: bool = True,
            classify: bool = True) -> str:
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

        features = {"extract_syntax": syntax,
                    "extract_entities": entities,
                    "extract_document_sentiment": document_sentiment,
                    "extract_entity_sentiment": entity_sentiment,
                    "classify_text": classify
                    }

        document = types.Document(content=content, language=language, type=document_type)
        response = self.client.annotate_text(
            document=document,
            features=features,
            encoding_type=encoding_type,
            retry=retry,
            timeout=timeout,
            metadata=metadata)
        return json.loads(MessageToJson(response))

    @staticmethod
    def parse(response: Dict) -> Dict:
        results = CloudLanguage.parse_sentences(response)
        results.update(CloudLanguage.parse_tokens(response))
        results.update(CloudLanguage.parse_document_sentiment(response))
        results.update(CloudLanguage.parse_entity(response))
        results.update(CloudLanguage.parse_categories(response))
        results.update({'language': response['language']})
        return results

    @staticmethod
    def parse_sentences(response: Dict) -> Dict[str, List[Union[str, float]]]:

        results = {
            'sentence_content': [],
            'sentence_begin_offset': [],
            'sentence_sentiment_magnitude': [],
            'sentence_sentiment_score': []
        }
        for sentence in response['sentences']:
            try:
                results['sentence_begin_offset'].append(sentence['text']['beginOffset'])
            except KeyError:
                results['sentence_begin_offset'].append(None)

            results['sentence_content'].append(sentence['text']['content'])
            results['sentence_sentiment_magnitude'].append(sentence['sentiment']['magnitude'])
            results['sentence_sentiment_score'].append(sentence['sentiment']['score'])

        return results

    @staticmethod
    def parse_tokens(response: Dict) -> Mapping[str, List[Union[str, float]]]:
        results = {
            'token_content': [],
            'token_begin_offset': [],
            'token_pos_tag': [],
            'token_pos_number': [],
            'token_dependency_edge_head_token_index': [],
            'token_dependency_edge_label': [],
            'token_lemma': []
        }

        for token in response['tokens']:
            try:
                results['token_begin_offset'].append(token['text']['beginOffset'])
            except KeyError:
                results['token_begin_offset'].append(None)

            try:
                results['token_pos_number'].append(token['partOfSpeech']['number'])
            except KeyError:
                results['token_pos_number'].append(None)

            results['token_content'].append(token['text']['content'])
            results['token_pos_tag'].append(token['partOfSpeech']['tag'])
            results['token_dependency_edge_head_token_index'].append(token['dependencyEdge']['headTokenIndex'])
            results['token_dependency_edge_label'].append(token['dependencyEdge']['label'])
            results['token_lemma'].append(token['lemma'])

        return results

    @staticmethod
    def parse_entity(response: Dict) -> Mapping[str, List[Union[str, float]]]:

        results = {
            'entity_name': [],
            'entity_type': [],
            'entity_salience': [],
            'entity_mention_content': [],
            'entity_mention_begin_offset': [],
            'entity_mention_type': [],
            'entity_sentiment_magnitude': [],
            'entity_sentiment_score': []
        }

        for entity in response['entities']:
            results['entity_name'].append(entity['name'])
            results['entity_type'].append(entity['type'])
            results['entity_salience'].append(entity['salience'])
            for mention in entity['mentions']:
                try:
                    results['entity_mention_begin_offset'].append(mention['text']['beginOffset'])
                except KeyError:
                    results['entity_mention_begin_offset'].append(None)

                try:
                    results['entity_sentiment_magnitude'].append(mention['sentiment']['magnitude'])
                except KeyError:
                    results['entity_sentiment_magnitude'].append(None)

                try:
                    results['entity_sentiment_score'].append(mention['sentiment']['score'])
                except KeyError:
                    results['entity_sentiment_score'].append(None)

                results['entity_mention_content'].append(mention['text']['content'])
                results['entity_mention_type'].append(mention['type'])

        return results

    @staticmethod
    def parse_document_sentiment(response: Dict) -> Dict[str, float]:

        results = {
            'document_sentiment_magnitude': response['documentSentiment']['magnitude'],
            'document_sentiment_score': response['documentSentiment']['score']
        }
        return results

    @staticmethod
    def parse_categories(response: Dict) -> Dict:
        results = {
            'category_name': [],
            'category_confidence': []
        }
        for category in response['categories']:
            results['category_name'].append(category['name'])
            results['category_confidence'].append(category['confidence'])

        return results