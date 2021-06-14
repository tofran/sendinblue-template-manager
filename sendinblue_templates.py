#!/usr/bin/env python3

"""Sendinblue Template Downloader/Uploader

Download and upload template html content to sendinblue.
Env var `SENDINBLUE_API_KEY` required (v3).

Files are named following the format:
 `<numeric-template-id>. <template name (escaped)>.html`
 ex: 1. `Sample template title.html`

Usage:
 ./sendinblue-template.py download [directory]
   Downloads the first 1000 templates from the sendinblue account.

 ./sendinblue-template.py upload [directory]
   Updates all matching templates html content in sendinblue.
"""

import glob
import os
import re
import sys

import requests

FILENAME_SEPARATOR = ". "
API_BASE_URL = "https://api.sendinblue.com/v3"
API_KEY = os.getenv("SENDINBLUE_API_KEY")
if not API_KEY:
    raise ValueError("SENDINBLUE_API_KEY env var must be set")


def request(method, path, **kwargs):
    headers = {
        "Accept": "application/json",
        "api-key": API_KEY,
    }

    response = requests.request(
        method,
        f"{API_BASE_URL}{path}",
        headers=headers,
        **kwargs,
    )

    if not response.ok:
        raise RuntimeError(response.text)

    return response


def to_safe_path(string):
    return re.sub(r'[^\w\d\-\–\ ]', '_', str(string))


def get_templates():
    return request(
        "GET",
        "/smtp/templates",
        params={  # TODO: Pagination
            "limit": "1000",
            "offset": "0",
            "sort": "asc"
        },
    ).json()


def download(directory):
    os.makedirs(directory, exist_ok=True)

    for template in get_templates()["templates"]:
        template_id = to_safe_path(f"{template['id']:03}")
        template_name = to_safe_path(template["name"])

        filename = os.path.join(
            directory,
            f"{template_id}{FILENAME_SEPARATOR}{template_name}.html",
        )

        print(f"Saving {filename}")

        with open(filename, "w") as f:
            f.writelines(template["htmlContent"])


def update_template(template_id, **kwargs):
    print(f"Updating template {template_id}... ", end="")

    request(
        "PUT",
        f"/smtp/templates/{template_id}",
        json=kwargs,
    )

    print("done!")


def get_template_ids_to_filepath(directory):
    template_ids_to_filepath = {}

    for filepath in sorted(glob.glob(f"{directory}/*.html")):
        filename = os.path.basename(filepath)
        filename_parts = filename.split(FILENAME_SEPARATOR, maxsplit=2)

        if len(filename_parts) != 2:
            raise RuntimeError(f"'{filepath}' does not follow expected naming format")

        template_id_str, _name = filename_parts
        template_id = int(template_id_str)

        if template_id in template_ids_to_filepath:
            raise RuntimeError(
                "More than one file references the same template: '{}' and '{}' reference template #{}".format(
                    template_ids_to_filepath[template_id],
                    filename,
                    template_id_str
                )
            )

        template_ids_to_filepath[template_id] = filepath

    return template_ids_to_filepath


def upload(directory):
    for template_id, filepath in get_template_ids_to_filepath(directory).items():

        with open(filepath, "r") as f:
            html_content = f.read()

        update_template(template_id, htmlContent=html_content)


def main():
    args = sys.argv
    operation = args[1]
    directory = args[2] if len(args) > 2 else "."

    if operation == "download":
        download(directory)
    elif operation == "upload":
        upload(directory)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
