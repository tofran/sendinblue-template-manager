# Sendinblue Template Downloader/Uploader

Download and upload Sendinblue template's html content for ease of editing and versioning.
Env var `SENDINBLUE_API_KEY` required (v3).

Files named following the format:
 `<numeric-template-id>. <template name (escaped)>.html`
 ex: `001. Sample template title.html`

## Installation

Available on [pypi as sendinblue-templates](https://pypi.org/project/sendinblue-templates/)

`pip install sendinblue-templates`

:sparkles:


## Usage
 - `sendinblue-templates download [directory]`
   Downloads the first 1000 templates from the Sendinblue account. Overriding existing files.

 - `sendinblue-templates upload [directory]`
   Updates all matching templates html content in Sendinblue.

