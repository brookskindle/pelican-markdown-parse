import os

from markdown import Markdown
from pelican import signals
from pelican.readers import MarkdownReader
from pelican.utils import pelican_open


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

        return content, metadata


def add_reader(readers):
    for extension in RemarkReader.file_extensions:
        readers.reader_classes[extension] = RemarkReader


def register():
    signals.readers_init.connect(add_reader)
