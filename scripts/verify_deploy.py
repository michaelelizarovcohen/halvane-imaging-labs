#!/usr/bin/env python3
"""Post-deployment integrity check: download every published evidence file from the live site and compare it,
byte for byte (SHA-256) and tag for tag (ExifTool JSON), with the local publication copies.

Usage: python3 scripts/verify_deploy.py BASE_URL [REPORT_PATH]
  e.g. python3 scripts/verify_deploy.py https://<user>.github.io/halvane-imaging-labs/
"""
import hashlib, json, os, subprocess, sys, tempfile, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = sys.argv[1].rstrip("/") + "/"
REPORT = sys.argv[2] if len(sys.argv) > 2 else None
ASSETS = json.load(open(os.path.join(ROOT, "data", "assets.json")))
LOCAL = os.path.join(ROOT, "docs", "evidence", "originals")
IGNORE = ("System:", "File:FileName", "File:Directory", "File:FilePermissions", "SourceFile", "ExifTool:ExifToolVersion")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def meta(path):
    r = subprocess.run(["exiftool", "-j", "-G1", "-a", "-n", "-q", "-q", path], capture_output=True, text=True)
    d = json.loads(r.stdout)[0]
    return {k: v for k, v in d.items() if not k.startswith(IGNORE)}


def fetch(url, dest):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "halvane-verify/1.0", "Accept-Encoding": "identity"})
            with urllib.request.urlopen(req, timeout=300) as r, open(dest, "wb") as f:
                while True:
                    b = r.read(1 << 20)
                    if not b:
                        break
                    f.write(b)
                return r.status, r.headers.get("Content-Type", "")
        except Exception as e:
            err = e
            time.sleep(5 * (attempt + 1))
    raise err


def main():
    lines, ok_all = [], True
    sums = {}
    with tempfile.TemporaryDirectory() as td:
        sp = os.path.join(td, "SHA256SUMS.txt")
        fetch(BASE + "evidence/SHA256SUMS.txt", sp)
        for ln in open(sp):
            h, p = ln.split()
            sums[p.replace("originals/", "")] = h
        for a in ASSETS:
            dest = os.path.join(td, a["file"])
            status, ctype = fetch(BASE + "evidence/originals/" + a["file"], dest)
            remote_sha, local_sha = sha(dest), sha(os.path.join(LOCAL, a["file"]))
            m_ok = meta(dest) == meta(os.path.join(LOCAL, a["file"]))
            ok = status == 200 and remote_sha == local_sha == a["sha256"] == sums.get(a["file"]) and m_ok
            ok_all &= ok
            lines.append(f"{'OK ' if ok else 'BAD'} {a['file']:16} http={status} bytes={os.path.getsize(dest)} sha256_match={remote_sha == local_sha} "
                         f"manifest_match={remote_sha == a['sha256']} sums_match={remote_sha == sums.get(a['file'])} exif_match={m_ok} type={ctype}")
            os.remove(dest)
    summary = f"{sum(1 for l in lines if l.startswith('OK'))}/{len(lines)} published evidence files verified against {BASE}"
    out = "\n".join([summary, time.strftime("checked %Y-%m-%dT%H:%M:%SZ", time.gmtime()), ""] + lines) + "\n"
    if REPORT:
        open(REPORT, "w").write(out)
    print(summary)
    for l in lines:
        if not l.startswith("OK"):
            print(l)
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
