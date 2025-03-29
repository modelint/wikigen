"""
cm.py – Process the xcm file
"""

# System
import sys
import logging
from pathlib import Path

# Model Integration
from xcm_parser.exceptions import ModelInputFileOpen as XCM_ModelInputFileOpen
from xcm_parser.class_model_parser import ClassModelParser

from xcm_wiki.exceptions import WGFileException


class ClassModelFile:
    """
    """

    def __init__(self, model_fname: str):
        """
        :param xcm_path: Path to the model (.xcm) file

        """
        self.logger = logging.getLogger(__name__)
        self.xuml_model_path = Path(model_fname).resolve()

        # First we parse both the model and layout files

        # Model
        self.logger.info("Parsing the class model")
        try:
            self.model = ClassModelParser.parse_file(file_input=self.xuml_model_path, debug=False)
        except WGFileException as e:
            self.logger.error(f"Cannot open class model file: {self.xuml_model_path}")
            sys.exit(str(e))



if __name__ == "__main__":
    x = ClassModelFile()

