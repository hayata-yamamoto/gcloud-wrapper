import os
from typing import Union

from google.cloud import bigquery
from google.oauth2.service_account import Credentials


def load_from_cloud_storage_uri(source_uri: str,
                                project: str,
                                dataset: str,
                                table: str,
                                credential: Union[str,
                                                  os.PathLike],
                                auto_detect: bool = True,
                                skip_leading_rows: int = 1) -> bigquery.LoadJob:
    """
    This function is only focused on load job execution via Google Cloud Storage.
    We're supporting only csv import from script.

    Args:
        source_uri (str) : cloud storage uri
        project (str) : project_id on google cloud platform
        dataset (str) : target dataset_id
        table (str) : table name created by job
        credential (str, os.PathLike) : access key location
        auto_detect (bool) : whether you use schema auto detection or not
        skip_leading_rows (int) : how many rows are skipped.

    Returns:
        bigquery.LoadJob : job result
    """

    # setup credential and client.
    credentials = Credentials.from_service_account_file(filename=credential)
    client = bigquery.Client(project=project, credentials=credentials)
    dataset_ref = client.dataset(dataset_id=dataset)

    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = auto_detect
    job_config.skip_leading_rows = skip_leading_rows

    # Send API request to BQ
    load_job = client.load_table_from_uri(
        source_uris=source_uri,
        destination=dataset_ref.table(table),
        job_config=job_config)

    return load_job.result()


class BigQuery:
    def __init__(self, project: str, dataset: str,
                 credential: Union[str, os.PathLike]):
        """

        Args:
            project (str) :
            dataset (str) :
            credential (str, os.PathLike) :
        """
        credentials = Credentials.from_service_account_file(
            filename=credential)
        self.client = bigquery.Client(project=project, credentials=credentials)
        self.dataset_ref = self.client.dataset(dataset_id=dataset)
        self.dataset = bigquery.Dataset(dataset_ref=self.dataset_ref)

    def create_table_from_gcs_uri(
            self,
            table: str,
            uri: str,
            **kwargs) -> bigquery.LoadJob:
        """

        Args:
            table (str) :
            uri (str) :
            **kwargs (str) : Load Job Attributes

        Returns:
            bigquery.LoadJob: job result
        """
        conf = bigquery.LoadJobConfig(**kwargs)

        return self.client.load_table_from_uri(
            source_uris=uri,
            destination=self.dataset_ref.table(table),
            job_config=conf).result()
