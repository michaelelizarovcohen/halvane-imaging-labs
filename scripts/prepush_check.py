#!/usr/bin/env python3
"""Pre-push content gate for the Halvane training site.

Blocks the push if the tracked tree, the staged index or the commits being pushed contain:
  * private/local-only material (instructor files, keys to exercises, modification records, raw source dumps)
  * secrets (tokens, private keys, .env files)
  * disclosure markers in text or in embedded image metadata (see MARKERS)
  * files over the size limit, an oversized tree, or Git LFS pointers/filters

Usage:  python3 scripts/prepush_check.py            (scan HEAD + index + working tree)
        python3 scripts/prepush_check.py --hook     (called by .git/hooks/pre-push; reads ref lines from stdin)
Exit status 1 on any finding. Secret values are never printed.
"""
import json, os, re, subprocess, sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or "."
SELF = "scripts/prepush_check.py"
ALLOWLIST = "scripts/prepush_allowlist.json"
MAX_FILE = 95 * 1024 * 1024
MAX_TOTAL = 900 * 1024 * 1024

FORBIDDEN_PATHS = [
    r"(^|/)\.env(\..*)?$", r"\.pem$", r"\.key$", r"(^|/)id_(rsa|ed25519|ecdsa)", r"(^|/)credentials", r"(^|/)secrets?\.",
    r"answer[_-]?key", r"instructor", r"modification[_-]?log", r"storyline", r"scenario[_-]?spec", r"prepare[_-]?evidence",
    r"qa[_-]?exercises", r"local[_-]?only", r"(^|/)sources/", r"(^|/)work/", r"evidence_private", r"\.part$",
]
MARKERS = [r"\banswers?\b", r"\bsolutions?\b", r"\bplanted\b", r"\binstructor\b", r"\bLOCAL-ONLY\b", r"\bground truth\b",
           r"\bmodification log\b", r"\bsynthetic\b"]
SECRETS = [
    ("GitHub token", r"\b(gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{40,})"),
    ("AWS access key", r"\b(AKIA|ASIA)[0-9A-Z]{16}\b"),
    ("private key block", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("Slack token", r"\bxox[abprs]-[A-Za-z0-9-]{10,}"),
    ("Google API key", r"\bAIza[0-9A-Za-z_-]{35}\b"),
    ("generic credential assignment", r"(?i)\b(api[_-]?key|secret|passwd|password|access[_-]?token)\s*[:=]\s*['\"][^'\"\s]{12,}['\"]"),
]
TEXT_EXT = {".html", ".htm", ".css", ".js", ".json", ".md", ".txt", ".csv", ".py", ".sh", ".svg", ".xml", ".yml", ".yaml",
            ".toml", ".cfg", ".gitignore", ".gitattributes", ".nojekyll", ""}
META_EXT = {".jpg", ".jpeg", ".heic", ".heif", ".dng", ".cr2", ".cr3", ".crw", ".nef", ".arw", ".raf", ".rw2", ".orf",
            ".pef", ".x3f", ".erf", ".dcr", ".mrw", ".gpr", ".png", ".tif", ".tiff"}

findings = []


def git(*args, text=True):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=text)


def add(kind, path, detail):
    findings.append((kind, path, detail))


def load_allowlist():
    p = os.path.join(ROOT, ALLOWLIST)
    return json.load(open(p)) if os.path.exists(p) else []


ALLOW = load_allowlist()


def allowed(path, tag, word, value):
    return any(a["path"] == path and a["tag"] == tag and a["marker"].lower() == word.lower() and a["contains"] in value
               for a in ALLOW)


def scan_text(path, data, label):
    if path in (SELF, ALLOWLIST):
        return
    for name, rx in SECRETS:
        if re.search(rx, data):
            add("secret", path, f"{name} pattern in {label} (value withheld)")
    for rx in MARKERS:
        for m in re.finditer(rx, data, flags=re.I):
            line = data.count("\n", 0, m.start()) + 1
            add("marker", path, f"'{m.group(0)}' at {label} line {line}")


def scan_metadata(path, abspath):
    r = subprocess.run(["exiftool", "-j", "-a", "-G1", "-q", "-q", "-b", "--ImageData", "-x", "PreviewImage", "-x", "JpgFromRaw",
                        "-x", "ThumbnailImage", "-x", "OtherImage", "-x", "MotionPhotoVideo", abspath], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)[0]
    except Exception:
        return
    for tag, v in d.items():
        if not isinstance(v, (str, int, float)) or str(v).startswith("base64:"):
            continue
        v = str(v)
        for name, rx in SECRETS:
            if re.search(rx, v):
                add("secret", path, f"{name} pattern in metadata tag {tag} (value withheld)")
        for rx in MARKERS:
            for m in re.finditer(rx, v, flags=re.I):
                if not allowed(path, tag, m.group(0), v):
                    add("marker", path, f"'{m.group(0)}' in metadata tag {tag}")


def main():
    hook = "--hook" in sys.argv
    tracked = [p for p in git("ls-files", "-z").stdout.split("\0") if p]
    staged = [p for p in git("diff", "--cached", "--name-only", "-z").stdout.split("\0") if p]
    paths = sorted(set(tracked) | set(staged))

    # paths ever committed on the branches being pushed (catches files added then deleted)
    history = set()
    revs = []
    if hook:
        for line in sys.stdin.read().splitlines():
            parts = line.split()
            if len(parts) == 4 and not set(parts[1]) == {"0"}:
                remote_sha = parts[3]
                revs.append(parts[1] if set(remote_sha) == {"0"} else f"{remote_sha}..{parts[1]}")
    for rev in (revs or ["HEAD"]):
        out = git("rev-list", "--objects", rev).stdout if git("rev-parse", "--verify", "-q", "HEAD").returncode == 0 else ""
        for line in out.splitlines():
            if " " in line:
                history.add(line.split(" ", 1)[1])

    for p in sorted(set(paths) | history):
        for rx in FORBIDDEN_PATHS:
            if re.search(rx, p, flags=re.I):
                add("forbidden-path", p, f"matches {rx}")

    attrs = open(os.path.join(ROOT, ".gitattributes")).read() if os.path.exists(os.path.join(ROOT, ".gitattributes")) else ""
    if "filter=lfs" in attrs:
        add("lfs", ".gitattributes", "Git LFS filter configured (GitHub Pages cannot serve LFS objects)")

    total = 0
    for p in paths:
        ap = os.path.join(ROOT, p)
        if not os.path.isfile(ap):
            continue
        size = os.path.getsize(ap)
        total += size
        if size > MAX_FILE:
            add("size", p, f"{size / 1e6:.1f} MB exceeds {MAX_FILE / 1e6:.0f} MB")
        ext = os.path.splitext(p)[1].lower()
        with open(ap, "rb") as f:
            head = f.read(200)
        if head.startswith(b"version https://git-lfs"):
            add("lfs", p, "Git LFS pointer file")
        if ext in TEXT_EXT or p.endswith((".nojekyll", "robots.txt")):
            scan_text(p, open(ap, encoding="utf-8", errors="replace").read(), "working tree")
            if p in staged:
                blob = git("show", f":{p}").stdout
                if blob:
                    scan_text(p, blob, "index")
        elif ext in META_EXT:
            scan_metadata(p, ap)
    if total > MAX_TOTAL:
        add("size", "(tree)", f"tracked content {total / 1e6:.0f} MB exceeds {MAX_TOTAL / 1e6:.0f} MB")

    if findings:
        print(f"prepush_check: {len(findings)} finding(s) - push blocked")
        for kind, p, d in findings[:200]:
            print(f"  [{kind}] {p}: {d}")
        sys.exit(1)
    print(f"prepush_check: OK ({len(paths)} files, {total / 1e6:.1f} MB tracked, {len(history)} history paths)")


if __name__ == "__main__":
    main()
