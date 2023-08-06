#! /usr/bin/python3
#
# uploader.py
#
# Project name: fncsf.pde.exporter.
# Author: Hugo Juhel
#
# description:
"""
Collections of functions to be binded to the CLI
"""

#############################################################################
#                                 Packages                                  #
#############################################################################


from pathlib import Path

import awswrangler as wr
import boto3
import pandas as pd

from pde_fncsf_exporter.api.credentials import get_credentials
from pde_fncsf_exporter.errors import Errors
from pde_fncsf_exporter.interactor import validate_csv
from pde_fncsf_exporter.interactor.targets import _TARGETS
from pde_fncsf_exporter.logger import get_module_logger

#############################################################################
#                                  Script                                   #
#############################################################################


_LOGGER = get_module_logger("uploader")
_BUCKET = "pde-integration"


def _upload_to_s3(df: pd.DataFrame, key: str) -> None:
    """
    Upload the file to s3
    """

    # Fetch the credentials
    credentials = get_credentials()

    # Prepare the dataframe by adding the required fields
    df["id_org"] = credentials.id_org
    df["inserted_date"] = pd.Timestamp.now()

    # Storing data on Data Lake
    try:
        wr.s3.to_parquet(
            df=df,
            boto3_session=boto3.Session(aws_access_key_id=credentials.access_key, aws_secret_access_key=credentials.secret_key),
            path=f"s3://{_BUCKET}/{credentials.username}/{key}",
            dataset=True,
            mode="overwrite",
            sanitize_columns=True,
            index=False,
            compression="gzip",
        )
    except BaseException as error:
        raise Errors.E040() from error  # type: ignore


def upload(path: Path) -> None:
    """
    Run the validations on the dataframes

    Args:
        path (Path): The base path to be used
    """

    for target, validator in _TARGETS.items():

        target_name = target.split(".")[0]
        target_path = path / target

        _LOGGER.info(f"\U00002699 Processing {target} ...")
        if not target_path.exists():
            raise Errors.E010(path=path)  # type: ignore

        try:
            df = pd.read_csv(target_path, encoding="utf-8")
        except BaseException as err:
            raise Errors.E022(path=target_path) from err  # type: ignore

        out = validate_csv(df, validator)
        if out is not None:
            _LOGGER.error(f'\U0000274C Validation failed for "{target}" \U0000274C')
            _LOGGER.error(" - \t" + out)
            return
        _LOGGER.info(f"\U00002728 {target} has been validated.")

        _upload_to_s3(df, target_name)
        _LOGGER.info(f"\U0001F680 {target} has been synced with the platform.")


if __name__ == "__main__":
    upload(Path.cwd())
