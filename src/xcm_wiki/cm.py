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
        :param model_fname: Path to the model (.xcm) file
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

        self.format_classes()

    def format_classes(self):
        for c in self.model.classes:
            if c.get('import'):
                continue  # Skip all imported classes
            text = "<description>\n\n"
            text = text + "### Identifiers\n"
            id_text = self.build_id_list(c['attributes'])
            text = text + id_text + "\n"
            text = text + "\n### Attributes\n\n"
            asect = self.build_attr_section(c['attributes'])
            text = text + asect


            pass

    def build_attr_section(self, attributes) -> str:
        non_ref_attrs = [a for a in attributes if not a.get('R')]
        if not non_ref_attrs:
            return "No non-referential attributes.\n"
        pass

    def build_id_list(self, attributes) -> str:
        identifiers = dict()  # Dictionary keyed by id number
        for a in attributes:
            if not a.get('I'):
                continue # This attribute is not part of any identifier
            for i in a['I']:
                # For each identifier in which this attribute participates...
                inum = i.number
                if not identifiers.get(inum):
                    # Create a new
                    identifiers[inum] = [a['name']]
                else:
                    identifiers[inum].append(a['name'])
            # id_lines = [f"{i}. {line}\n" for i in identifiers for line in i]
        id_lines = []
        for i in sorted(identifiers):
            names = " + ".join(identifiers[i])
            id_lines.append(f"{i}. {names}")
        id_block = "\n".join(id_lines)
        return id_block





if __name__ == "__main__":
    x = ClassModelFile()

