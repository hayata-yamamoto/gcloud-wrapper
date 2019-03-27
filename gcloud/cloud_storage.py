from pathlib import Path
from typing import Union, Optional

from google.cloud.storage import Client, Blob
from google.oauth2.service_account import Credentials


def _get_client(project: str,
                credential: Optional[Union[str, Path]] = None) -> Client:
    """

    Args:
        project (str) :
        credential (str, None) :

    Returns:
        Client
    """
    if credential is None:
        return Client(project=project)

    credential = Credentials.from_service_account_file(filename=credential)
    return Client(project=project, credentials=credential)


def upload_from_filename(filename: Union[str, Path],
                         project: str,
                         bucket: str,
                         blob: str,
                         credential: Optional[str] = None,
                         content_type: Optional[str] = None) -> str:
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
    client = _get_client(project=project, credential=credential)

    bkt = client.get_bucket(bucket_name=bucket)

    bl = bkt.blob(blob_name=blob)
    bl.upload_from_filename(filename=filename, content_type=content_type)

    return bl.public_url


def download_from_blob(filename: str,
                       project: str,
                       bucket: str,
                       blob: str,
                       credential: Optional[Union[str, Path]] = None):
    """

    Args:
        filename (str) :
        project (str) :
        bucket (str) :
        blob (str) :
        credential (str, None) :

    Returns:
        None
    """
    client = _get_client(project=project, credential=credential)
    bkt = client.bucket(bucket_name=bucket)
    bkt.blob(blob_name=blob).download_to_filename(filename=filename)


class CloudStorage:
    def __init__(self, project: str, bucket: str,
                 credential: Optional[Union[str, Path]] = None):
        """
        Args:
            project (str) :
            bucket (str) :
            credential (str, None) :
        """
        self.client = _get_client(project, credential=credential)
        self.bucket = self.client.bucket(bucket_name=bucket)

    def bucket_exist(self) -> bool:
        """
        Returns:
            bool
        """
        return self.bucket.exists()

    def get_blob_list(self) -> list:
        """

        Returns:
            list
        """
        return [b for b in self.bucket.list_blobs()]

    def get_blob_url(self, blob: str) -> str:
        """

        Args:
            blob:

        Returns:

        """
        return self.bucket.blob(blob_name=blob).public_url

    def upload_from_filename(self,
                             filename: Union[str, Path],
                             blob: str,
                             content_type: Optional[str] = None) -> str:
        """
        Args:
            filename (str, os.PathLike) :
            blob (str) :
            content_type (str, None) :
        Returns:
            str : public url
        """
        bl = self.bucket.blob(blob_name=blob)
        bl.upload_from_filename(
            filename=filename,
            content_type=content_type,
            client=self.client)
        return bl.public_url

    def download_from_blob(self, filename: str, blob: str) -> None:
        """

        Args:
            filename (str) :
            blob (str) :

        Returns:
            None
        """
        self.bucket.blob(
            blob_name=blob).download_to_filename(
            filename=filename)

