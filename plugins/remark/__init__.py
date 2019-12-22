import os
import re

from markdown import Markdown
from pelican import signals
from pelican.readers import MarkdownReader
from pelican.utils import pelican_open
from pelican.contents import Content

INTRASITE_LINK_REGEX = '[{|](?P<what>.*?)[|}]' # TODO: fetch from Content

def my_regex_matcher(self):
    """
    Match internal pelican links found in markdown content

    Markdown links are of the form:
        [text](link)
        ![](image.png)
        ![alt text](image.png)
    """
    regex = (
        r"(?P<markup>"
        r"!?"
        r"\[.*?\]"  # Markdown links start with brackets, Eg: [], [link name]
        r")"  # End markup group

        r"(?P<quote>"
        r"\("  # Open parenthesis
        r")"  # End group quote


        # TODO: quote needs to be open close paren ( ), but it can't match both

        # r"\[.*?\]"  # Markdown links start with brackets, Eg: [], [link name]
        # r"\("  # Open parenthesis
        + "(?P<path>{0}".format(INTRASITE_LINK_REGEX)  # {...} or |...| to denote an internal link
        + r"(?P<value>.*?))"  # Then the link path, relative to the site
        r"\)"  # Finally, close the parenthesis

        r".*"  # Capture everything else, we just don't care
    )
    print(regex)
    return re.compile(regex, re.X)

Content._get_intrasite_link_regex = my_regex_matcher


class RemarkReader(MarkdownReader):
    file_extensions = ["remark"]

    def read(self, source_path):
        # content is returned as HTML, but we don't want that.
        content, metadata = super().read(source_path)

        if metadata.get("template") is None:
            metadata["template"] = "remark"

        # Instead, replace content with the original markdown source
        with pelican_open(source_path) as text:
            md_content = text.strip()

            # Remove initial metadata at the top of the file
            delimeter = "\n\n"
            content = md_content[md_content.find(delimeter) + len(delimeter):]

        # content = "![]({static}/images/git-status.png)"
        # content = "<a src='{static}/images/git-status.png'></a>"
        # content = '<textarea id="source">![]({static}/images/git-status.png)</textarea>'
        return content, metadata


def add_reader(readers):
    for extension in RemarkReader.file_extensions:
        readers.reader_classes[extension] = RemarkReader


def register():
    signals.readers_init.connect(add_reader)
