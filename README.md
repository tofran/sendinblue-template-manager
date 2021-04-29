# Sendinblue Template Downloader/Uploader

Download and upload Sendinblue template's html content for ease of editing and versioning.
Env var `SENDINBLUE_API_KEY` required (v3).

Files are placed in `./templates` and named following the format:
 `<numeric-template-id>. <template name (escaped)>.html`
 ex: `1. Sample template title.html`

Usage:
 - `./sendinblue-template.py download`
   Downloads the first 1000 templates from the Sendinblue account.

 - `./sendinblue-template.py upload`
   Updates all matching templates html content in Sendinblue.