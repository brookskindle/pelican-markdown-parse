import os

from markdown import Markdown
from pelican import signals
from pelican.readers import MarkdownReader
from pelican.utils import pelican_open


class RemarkReader(MarkdownReader):
    templates = ["remark"]
    file_extensions = MarkdownReader.file_extensions + ["remark"]

    def read(self, source_path):
        content, metadata = super().read(source_path)
        print(metadata)
        if source_path.endswith(".remark"):
            metadata["template"] = "remark"
        if metadata.get("template") in self.templates:
            with pelican_open(source_path) as text:
                md_content = text.strip()
                # Remove the initial metadata at the top of the file
                delimeter = "\n\n"
                content = md_content[md_content.find(delimeter) + len(delimeter):]
        return content, metadata


def add_reader(readers):
    for extension in RemarkReader.file_extensions:
        readers.reader_classes[extension] = RemarkReader


def after_write(path, context):
    return
    print("\n\n")
    print(path, context)
    print("\n\n")


def register():
    signals.readers_init.connect(add_reader)
    signals.content_written.connect(after_write)
