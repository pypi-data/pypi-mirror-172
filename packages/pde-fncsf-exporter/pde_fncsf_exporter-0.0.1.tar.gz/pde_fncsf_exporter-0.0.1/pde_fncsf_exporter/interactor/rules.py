#! /usr/bin/python3
#
# rules.py
#
# Project name: fncsf.pde.exporter.
# Author: Hugo Juhel
#
# description:
"""
A list of rules to be applied to the dataframes
"""

#############################################################################
#                                 Packages                                  #
#############################################################################

from typing import List, Optional

import pandas as pd

from pde_fncsf_exporter.interactor.validator import Validator

#############################################################################
#                                 Script                                    #
#############################################################################


@Validator.register(name="has_columns")
def _expectations_has_columns(df: pd.DataFrame, columns: List[str]) -> Optional[str]:
    """
    Check that the dataframes has the provided columns

    Args:
        df (pd.DataFrame): The dataframe to check
        columns (list[str]): A list of columns to check agains the dataframe.

    Returns:
        str: The list of missing columns, if any
    """

    missing_columns = set(columns) - set(df.columns)
    if missing_columns:
        return f"The dataset is missing the following columns: {', '.join(missing_columns)}"

    surnumerary_colunmns = set(df.columns) - set(columns)
    if surnumerary_colunmns:
        return f"The dataset has the following surnumerary columns: {', '.join(surnumerary_colunmns)}"

    return None
