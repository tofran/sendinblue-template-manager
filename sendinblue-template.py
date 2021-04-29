#!/usr/bin/env python3

"""Sendinblue Template Downloader/Uploader

Download and upload template html content to sendinblue.
Env var `SENDINBLUE_API_KEY` required (v3).

Files are placed in `./templates` and named following the format:
 `<numeric-template-id>. <template name (escaped)>.html`
 ex: 1. `Sample template title.html`

Usage:
 ./sendinblue-template.py download
   Downloads the first 1000 templates from the sendinblue account.

 ./sendinblue-template.py upload
   Updates all matching templates html content in sendinblue.
"""

import json
import glob
import os
import re
import sys

import requests

FILE_ID_NAME_SEPARATOR = ". "
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


def download(directory):
    response = request(
        "GET",
        "/smtp/templates",
        params={  # TODO: Pagination
            "limit": "1000",
            "offset": "0",
            "sort": "asc"
        },
    ).json()

    for template in response["templates"]:
        template_id = to_safe_path(f"{template['id']:03}")
        template_name = to_safe_path(template["name"])

        filename = os.path.join(
            directory,
            f"{template_id}{FILE_ID_NAME_SEPARATOR}{template_name}.html",
        )

        print(f"Saving {filename}")

        with open(filename, "w") as f:
            f.writelines(template["htmlContent"])


def update_template(template_id, **kwargs):
    print(f"Updating template {template_id}... ", end="")

    response = request(
        "PUT",
        f"/smtp/templates/{template_id}",
        json=kwargs,
    )

    print("done!")


def upload(directory):
    for filepath in sorted(glob.glob(f"{directory}/*.html")):
        filename = os.path.basename(filepath)

        template_id, _name = filename.split(FILE_ID_NAME_SEPARATOR)
        template_id = int(template_id)

        with open(filepath, "r") as f:
            html_content = f.read()

        update_template(template_id, htmlContent=html_content)


if __name__ == "__main__":
    directory = "templates"
    operation = sys.argv[1]

    if operation == "download":
        download(directory)
    elif operation == "upload":
        upload(directory)
    else:
        print(__doc__)
