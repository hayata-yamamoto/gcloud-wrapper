import os
from typing import Union

from google.cloud import storage
from google.oauth2.service_account import Credentials


def upload_from_filename(filename: Union[str, os.PathLike],
                         project: str,
                         bucket: str,
                         blob: str,
                         credential: Union[str, None] = None,
                         content_type: Union[str, None] = None) -> str:
    """
    Args:
        filename (str, os.PathLike) :
        project (str) :
        bucket (str) :
        blob (str) :
        credential (str, None) :
        content_type (str, None) :

    Returns:
        str : public storage url
    """
    if credential is None:
        client = storage.Client(project=project)
    else:
        credential = Credentials.from_service_account_file(filename=credential)
        client = storage.Client(project=project, credentials=credential)

    bkt = client.get_bucket(bucket_name=bucket)
    assert bkt.exists(), 'bucket is not exist.'

    bl = bkt.blob(blob_name=blob)
    bl.upload_from_filename(filename=filename, content_type=content_type)

    return bl.public_url


class CloudStorage:
    def __init__(self, project: str, bucket: str,
                 credential: Union[str, None] = None):
        """

        Args:
            project (str) :
            bucket (str) :
            credential (str, None) :
        """
        if credential is None:
            self.client = storage.Client(project=project)
        else:
            credentials = Credentials.from_service_account_file(
                filename=credential)
            self.client = storage.Client(
                project=project, credentials=credentials)
        self.bucket = self.client.bucket(bucket_name=bucket)

    def bucket_exist(self) -> bool:
        """

        Returns:
            bool
        """
        return self.bucket.exists()

    def upload_from_filename(self,
                             filename: Union[str, os.PathLike],
                             blob: str,
                             content_type: Union[str, None] = None) -> str:
        """

        Args:
            filename (str, os.PathLike) :
            blob (str) :
            content_type (str, None) :

        Returns:
            str : public url
        """
        blob = self.bucket.blob(blob_name=blob)
        blob.upload_from_filename(
            filename=filename,
            content_type=content_type,
            client=self.client)
        return blob.public_url
