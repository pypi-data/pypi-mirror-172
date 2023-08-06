#! /usr/bin/python3
#
# targets.py
#
# Project name: fncsf.pde.exporter.
# Author: Hugo Juhel
#
# description:
"""
Specify the rules to be applied to the dataset.
"""

#############################################################################
#                                 Packages                                  #
#############################################################################

from pde_fncsf_exporter.interactor.validator import Validator

#############################################################################
#                                  Script                                   #
#############################################################################

# Define the test suits
_TARGETS = {
    "schools.csv": Validator(
        ("has_columns", {"columns": ["id", "name"]}),
    ),
}
