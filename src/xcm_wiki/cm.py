"""
cm.py – Process the xcm file
"""

# System
import sys
import logging
from pathlib import Path

# Model Integration
from xcm_parser.class_model_parser import ClassModelParser

from xcm_wiki.exceptions import *

_logger = logging.getLogger(__name__)

# Given two multiplicity/conditionality pairs,
# we try to keep the c condtionality on the right
# and the 1 on the left using the following pattern
# purely as a matter of consistent style.

# It's a bit arbitrary, yet consistent, so we express the
# rule with a mapping rather than attempt to enforce it with
# logic. Also makes it easier to change if we want.
_format_rule = {
    ("1", "1"): "1:1",
    ("1", "1c"): "1:1c",
    ("1c", "1"): "1:1c",  # **
    ("1c", "1c"): "1c:1c",
    ("1", "M"): "1:M",
    ("1c", "M"): "1c:M",
    ("1", "Mc"): "1:Mc",
    ("1c", "Mc"): "1c:Mc",
    ("M", "1"): "1:M",  # **
    ("M", "1c"): "1c:M",  # **
    ("Mc", "1"): "1:Mc",  # **
    ("Mc", "1c"): "1c:Mc",  # **
    ("M", "M"): "M:M",
    ("M", "Mc"): "M:Mc",
    ("Mc", "M"): "M:Mc",  # **
    ("Mc", "Mc"): "Mc:Mc"
}

# We like to spell out the multiplicity/conditionality
# in the relationship headers for easier reading.
_mult_name = {
    "1" : "exactly one",
    "1c" : "zero or one",
    "M" : "at least one",
    "Mc" : "zero, one or many"
}


class ClassModelFile:
    """
    Manage formatting and output of class and relationship description wiki templates
    """

    def __init__(self, model_fname: str, dir_name: str, debug=False):
        """
        Parse the model file and generate a markdown (*.md) wiki template file for each class
        and relationship.

        For class descriptions, use the file name pattern: <class_name>.md with hyphens in place of spaces
        in the class name. Ex: Shaft-Level.md

        For relationship descriptions, use file name pattern: <rnum>.md  Ex: R21.md

        :param model_fname: Name of the class model *.xcm file
        :param dir_name: The markdown files will be created/updated in this directory
        """

        # Resolve directories to absolute paths
        self.wiki_path = Path(dir_name).resolve()
        self.wiki_path.mkdir(exist_ok=True)  # Create the wiki dir if it does not exist
        self.xcm_model_path = Path(model_fname).resolve()

        # Parse the model .xcm file

        # Model
        _logger.info(f"Parsing the class model: {self.xcm_model_path}")
        try:
            self.model = ClassModelParser.parse_file(file_input=self.xcm_model_path, debug=debug)
        except WGFileException as e:
            _logger.error(f"Cannot open class model file: {self.xcm_model_path}")
            sys.exit(str(e))
        _logger.info("Parsing complete")

        self.format_classes()
        self.format_relationships()

    def format_classes(self):
        """
        Here is the wiki template we want to create for each class,
        shown between the --- borders which are not part of the generated template:

        Example 1 - where all of attributes are referential
        ---
        <description>

        ### Identifiers
        1. ID + Domain
        2. Name + Number + Domain

        ### Attributes

        No non-referential attributes.
        ---

        Notes:
            <description> will be replaced later by the user, all <> items are to be filled in by the user
            Two identifiers were found and filled based on the model parse
            In this case, all of the attributes were referential, so no entries appear in the Attributes
            section.

        Example 2: Two non-referential attributes found:
        ---
        <description>

        ### Identifiers
        1. ID

        ### Attributes

        #### Tail number

        <description>

        **Type:** Tail Number, based on <basetype>

        #### Altitude

        <description>

        **Type:** Altitude MSL, based on <basetype>
        ---
        """
        for c in self.model.classes:
            lines = []
            if c.get('import'):
                continue  # Skip all imported classes

            _logger.info(f"Formatting class: {c['name']}")
            # Class description: User will paste in this part
            lines.append("<description>")  # User will fill this in
            lines.append("")  # Blank line (OS independent newlines added when file is written out)

            # Identifiers: Generated from parse
            lines.append("### Identifiers")
            lines.append("")
            id_text = ClassModelFile.build_id_list(c['attributes'])
            lines.extend(id_text)  # id_text is a list of identiifer strings and we append those strings to our lines

            # Attributes
            lines.append("")
            lines.append("### Attributes")
            attr_text = ClassModelFile.build_attr_section(cname=c['name'], attributes=c['attributes'])
            lines.extend(attr_text)

            # Generate the wiki class md file
            self.gen_md_file(name=c['name'], content=lines)

    @staticmethod
    def build_id_list(attributes) -> list[str]:
        """
        Create a list of identifiers from the model parse

        :param attributes: Attribute parse for a single class
        :return: A list of identifier entries ordered by id number
        """

        # For reference, here is an example attribute record:

        # {'I': [ID_a(number=1, superid=False)], 'OR': [], 'R': [(2018, False)], 'derived': False, 'name': 'Action'}

        # All we care about here is the 'I' section
        # The value of the 'I' key is a list of ID_a tuples
        # If this list is empty, this is not an identifier attribute and we move on to the next attribute

        # Otherwise, we care only about the .number value in each ID_a tuple
        # The same identifier attribute may be a member of more than one identifier

        identifiers = dict()  # Dictionary keyed by id number
        for a in attributes:
            if not a.get('I'):
                continue  # This attribute is not part of any identifier, move on to the next attribute
            for i in a['I']:
                # For each identifier in which this attribute participates...
                inum = i.number
                if not identifiers.get(inum):
                    # First time we encounter this number, make a new entr for the id num with this attr name
                    identifiers[inum] = [a['name']]
                else:
                    # Add this attr name to the existing identifier number entry
                    identifiers[inum].append(a['name'])
        id_lines = [f"{i}. {" + ".join(identifiers[i])}" for i in sorted(identifiers)]
        return id_lines

    @staticmethod
    def build_attr_section(cname: str, attributes) -> list[str]:
        """
        We either state that there are no non-referential attributes or
        we add a name/type entry per non-referential attribute

        :param cname: Name of the class, for the warning message
        :param attributes: Attribute parse for a single class
        :return: All lines of text in the attribute definitions (under the attribute section header)
        """
        non_ref_attrs = [a for a in attributes if not a.get('R')]
        if not non_ref_attrs:
            return ["\nNo non-referential attributes."]
        else:
            text = []
            for nr in non_ref_attrs:
                try:
                    text.append(f"\n#### {nr['name']}\n\n**Type:** {nr['type']}, based on String")
                except KeyError as e:
                    if nr.get('name'):
                        _logger.warning(f"No type specified for attribute: {cname}.{nr['name']} -- inserting <tbd>")
                        text.append(f"\n#### {nr['name']}\n\n**Type:** <tbd>, based on String")
            return text

    def format_relationships(self):
        """
        We generate a different wiki template for each relationship type: association, ordinal, generalization
        """
        for r in self.model.rels:
            _logger.info(f"Formatting relationship: {r['rnum']}")
            if r.get('t_side'):
                # Association
                rtext = ClassModelFile.format_assoc(r)
            elif r.get('ascend'):
                # Ordinal
                rtext = ClassModelFile.format_ordinal(r)
            else:
                # Generalization
                rtext = ClassModelFile.format_gen(r)

            # Header boundary
            rtext.append("")
            rtext.append("---")

            # Description section
            rtext.append("")
            rtext.append("<description>")

            # Generate the wiki relationship md file
            self.gen_md_file(name=r['rnum'], content=rtext)

    @staticmethod
    def format_ordinal(r) -> list[str]:
        """
        Generate the text for an ordinal relationship description

        :param r: The relationship parse
        :return: All text lines in the ordinal description
        """
        return [
            f"## {r['rnum']} / Ordinal",
            "",
            f"[[{r['ascend']['cname']}]] {r['ascend']['highval']}, "
            f"{r['ascend']['lowval']}"
        ]

    @staticmethod
    def format_gen(r) -> list[str]:
        """
        Generate the text for a generalization description

        :param r: The relationship parse
        :return: All text lines in the generalization description
        """
        subs = r['subclasses']  # The list of subclass names
        sub1 = subs[0]  # We use "is a" or "is an" based on the first character in the first subclass name
        n = "n" if sub1[0].lower() in 'aeiou' else ""
        # We wrap each name in [[ ]] braces so each class name is a link to its class description page
        h_isa = f"[[{r['superclass']}]] is a{n} "
        br_subs = [f"[[{s}]]" for s in subs]

        if len(subs) == 2:
            # With only two classes we say: SubclassA or SubclassB
            h_subnames = f"{br_subs[0]} or {br_subs[1]}"
        else:
            # Otherwise we say: SubclassA, SubclassB, ... or Subclass<x>
            h_subnames = f"{', '.join(br_subs[:-1])}, or {br_subs[-1]}"

        return [
            f"### {r['rnum']} / Generalization",
            "",
            h_isa + h_subnames,
            ]

    @staticmethod
    def format_assoc(r) -> list[str]:
        """
        :param r: The relationship parse
        :return: All text lines in the association description
        """
        # Relationship header
        text: list[str] = []
        amult = r.get('assoc_mult', '')  # This only applies if there is an association class
        amult = f"-{amult}" if amult else ""
        mult = f"{_format_rule[(r['t_side']['mult'], r['p_side']['mult'])]}{amult}"  # Put multipicity in standard form
        text.append(f"## {r['rnum']} / {mult}")
        text.append("")

        # Relationship phrases
        text.append(f"[[{r['t_side']['cname']}]] {r['t_side']['phrase']} _{_mult_name[r['t_side']['mult']]}_ [[{r['p_side']['cname']}]]")
        text.append("")
        text.append(f"[[{r['p_side']['cname']}]] {r['p_side']['phrase']} _{_mult_name[r['p_side']['mult']]}_ [[{r['t_side']['cname']}]]")

        return text

    def gen_md_file(self, name: str, content: list[str]):
        """
        Writes content out to a markdown file

        :param name: The basename of the file, the .md suffix will be appended
        :param content: A list of newline terminates strings to be written out to the file
        """

        # Replace any spaces with the hyphen character, no change to case
        file_path = self.wiki_path / f"{name.replace(' ', '-')}.md"

        with file_path.open("w", encoding="utf-8") as f:
            f.writelines("\n".join(content))

        _logger.info(f"Created: {file_path}")
