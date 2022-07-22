import os

from django.conf import settings

from markdownx.utils import markdownify


def generate_html_from_markdown_file(markdown_file):
    html_dict = {}
    html_list = []
    html = ""
    try:
        markdown_doc = os.path.join(
            settings.BASE_DIR, "relecov_documentation", "markdown_files", markdown_file
        )
        with open(markdown_doc, "r") as fh:
            for line in fh:
                html_list.append(line)
                # html += markdownify(line)

    except FileNotFoundError:
        print("File doesn't exists")
        return "ERROR FILE NOT FOUND"
    for html_line in html_list[4:]:
        html += markdownify(html_line)

    html_dict["title"] = markdownify(html_list[0])
    html_dict["sub_title"] = markdownify(html_list[2])
    html_dict["body"] = html

    return html_dict
