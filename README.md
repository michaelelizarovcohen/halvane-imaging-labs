# Halvane Imaging Labs — OSINT metadata training site

**Halvane Imaging Labs is a fictional company.** This repository is a static GitHub Pages site built as an
OSINT and digital-forensics training environment. Students investigate real EXIF / XMP / IPTC / maker-note
metadata in 86 real photographs (RAW, HEIF/HEIC and JPEG from about 50 different devices), correlating it with
an invented corporate website: team pages, projects, a news archive, a public equipment register and a client
report under review.

- Live site: https://michaelelizarovcohen.github.io/halvane-imaging-labs/
- Start with the lab notice: `docs/lab-notice/index.html` (`/lab-notice/` on the live site), then the student worksheet.
- No forms, accounts, analytics, cookies or third-party scripts. `robots.txt` disallows crawling and pages carry `noindex`.

## Evidence integrity

Investigation files live in `docs/evidence/originals/` and are served byte-for-byte. Their SHA-256 values are in
`docs/evidence/SHA256SUMS.txt`, `manifest.csv` and `data/assets.json`.

- No build step, CDN, optimiser or Jekyll touches them (`.nojekyll`, `.gitattributes` with `* -text`, no Git LFS).
- Previews/thumbnails in `docs/evidence/{previews,thumbs}/` are separate resized JPEGs with no metadata.
- `scripts/verify_deploy.py BASE_URL` downloads every published original from the live site and compares SHA-256
  and the full ExifTool tag set with the local copies.

```
sha256sum -c docs/evidence/SHA256SUMS.txt   # run from docs/evidence
```

## Building

Requirements: Python 3.10+, ExifTool, Pillow, pillow-heif, rawpy; GoPro `gpr_tools` (https://github.com/gopro/gpr) for GPR previews.

```
pip install pillow pillow-heif rawpy
GPR_TOOLS=/path/to/gpr_tools python3 build/build_site.py   # regenerates HTML, previews (cached), CREDITS.md, manifest.csv
python3 scripts/check_links.py                               # internal link check
```

The build verifies every original against `data/assets.json` before and after generating pages and never writes to
`docs/evidence/originals/`.

## Safety checks before every push

```
sh scripts/install-hooks.sh        # installs .git/hooks/pre-push
python3 scripts/prepush_check.py   # run manually at any time
```

The gate scans tracked, staged and pushed content (text and embedded image metadata) for private or unpublished
material, secrets, disclosure markers, oversize files and Git LFS usage, and blocks the push on any finding.

## Sources and licences

All photographs come from open test collections: raw.pixls.us (CC0), Immich test-assets (public domain per README;
repository AGPL-3.0), metadata-extractor-images (free-use grant), ianare/exif-samples (CC BY-SA 4.0) and the VISION
dataset (CC BY-SA 4.0, Shullani et al., EURASIP J. on Information Security 2017, doi:10.1186/s13635-017-0067-2).
See `CREDITS.md` for per-file attribution and `LICENSES.md` for terms. Metadata in some files has been added or edited for the
training scenario; pixel data is unchanged.

Site code and original text: CC BY-SA 4.0. Custom domain: none (`CUSTOM_DOMAIN=(none)`).
