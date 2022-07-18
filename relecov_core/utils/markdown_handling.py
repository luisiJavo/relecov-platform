import os

from django.conf import settings

from markdownx.utils import markdownify


def generate_html_from_markdown_file():
    html = ""
    markdown_doc = os.path.join(
        settings.BASE_DIR, "documents", "tutorial", "markdown_files", "documentation.md"
    )
    with open(markdown_doc, "r") as fh:
        # doc = fh.readlines()
        for line in fh:
            html += markdownify(line)
    return html
