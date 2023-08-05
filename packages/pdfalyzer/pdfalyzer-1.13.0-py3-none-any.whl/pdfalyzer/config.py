from argparse import Namespace
import importlib.resources
import logging
from os import environ, pardir, path

from yaralyzer.config import YaralyzerConfig, is_env_var_set_and_not_false, is_invoked_by_pytest
from yaralyzer.util.logging import log, set_log_level

PDFALYZE = 'pdfalyze'
PROJECT_ROOT = path.join(str(importlib.resources.files('pdfalyzer')), pardir)
PYTEST_FLAG = 'INVOKED_BY_PYTEST'

# Configuring PDFALYZER_LOG_DIR has side effects; see .pdfalyzer.example in repo for specifics.
LOG_LEVEL_ENV_VAR = 'PDFALYZER_LOG_LEVEL'
LOG_DIR_ENV_VAR = 'PDFALYZER_LOG_DIR'

# 3rd part pdf-parser.py
PDF_PARSER_EXECUTABLE_ENV_VAR = 'PDFALYZER_PDF_PARSER_PY_PATH'
DEFAULT_PDF_PARSER_EXECUTABLE = path.join(PROJECT_ROOT, 'tools', 'pdf-parser.py')

YaralyzerConfig.LOG_DIR = environ.get(LOG_DIR_ENV_VAR)
YaralyzerConfig.LOG_LEVEL = logging.getLevelName(environ.get(LOG_LEVEL_ENV_VAR, 'WARN'))


class PdfalyzerConfig:
    _parsed_args: Namespace = Namespace()

    @classmethod
    def args(cls):
        """Args parsed by argparse at startup."""
        return cls._parsed_args

    # Path to Didier Stevens's pdf-parser.py
    if is_env_var_set_and_not_false(PDF_PARSER_EXECUTABLE_ENV_VAR):
        PDF_PARSER_EXECUTABLE = path.join(environ[PDF_PARSER_EXECUTABLE_ENV_VAR], 'pdf-parser.py')
    elif is_invoked_by_pytest():
        PDF_PARSER_EXECUTABLE = DEFAULT_PDF_PARSER_EXECUTABLE
    else:
        if path.exists(DEFAULT_PDF_PARSER_EXECUTABLE):
            PDF_PARSER_EXECUTABLE = DEFAULT_PDF_PARSER_EXECUTABLE
        else:
            PDF_PARSER_EXECUTABLE = None
