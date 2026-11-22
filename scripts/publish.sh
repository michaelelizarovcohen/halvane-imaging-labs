#!/usr/bin/env bash
# Create the public repository (if needed), push, enable GitHub Pages from main:/docs with HTTPS,
# wait for the build, then verify every published evidence file against the local copies.
#
# Requires GitHub CLI auth whose token can: create repositories / administer this repo (Administration: write),
# push (Contents: write) and configure Pages (Pages: write). A classic token needs the `repo` scope instead.
# CUSTOM_DOMAIN defaults to none; if set, docs/CNAME is committed before pushing and DNS is NOT changed.
# Usage: [OWNER=<user-or-org>] scripts/publish.sh [REPORT_PATH]   (OWNER defaults to the authenticated gh user)
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
REPO="${REPO:-halvane-imaging-labs}"
OWNER="${OWNER:-$(gh api user --jq .login)}"
CUSTOM_DOMAIN="${CUSTOM_DOMAIN:-}"
REPORT="${1:-}"

python3 scripts/prepush_check.py

if ! gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
  gh repo create "$OWNER/$REPO" --public --disable-wiki \
    --description "Fictional company - OSINT and EXIF/XMP metadata training environment (GitHub Pages)" \
    --homepage "https://$OWNER.github.io/$REPO/"
fi
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "https://github.com/$OWNER/$REPO.git"
else
  git remote add origin "https://github.com/$OWNER/$REPO.git"
fi
if [ -n "$CUSTOM_DOMAIN" ]; then
  printf '%s\n' "$CUSTOM_DOMAIN" > docs/CNAME
  git add docs/CNAME && git commit -m "Set custom domain $CUSTOM_DOMAIN" >/dev/null
  echo "DNS to create yourself: CNAME $CUSTOM_DOMAIN -> $OWNER.github.io (apex: A records 185.199.108-111.153)"
fi
git config http.postBuffer 1048576000
git push -u origin --all           # pre-push hook re-runs the content gate
git push origin --tags

if gh api "repos/$OWNER/$REPO/pages" >/dev/null 2>&1; then
  gh api -X PUT "repos/$OWNER/$REPO/pages" -f "source[branch]=main" -f "source[path]=/docs" >/dev/null
else
  gh api -X POST "repos/$OWNER/$REPO/pages" -f "source[branch]=main" -f "source[path]=/docs" >/dev/null
fi

echo "waiting for Pages build..."
for _ in $(seq 1 80); do
  st="$(gh api "repos/$OWNER/$REPO/pages" --jq .status 2>/dev/null || echo pending)"
  [ "$st" = "built" ] && break
  [ "$st" = "errored" ] && { echo "Pages build errored"; exit 1; }
  sleep 15
done
gh api -X PUT "repos/$OWNER/$REPO/pages" -F https_enforced=true >/dev/null || echo "note: HTTPS enforcement will be retried once the certificate is issued"
URL="$(gh api "repos/$OWNER/$REPO/pages" --jq .html_url)"
echo "live at $URL"
python3 scripts/verify_deploy.py "$URL" ${REPORT:+"$REPORT"}
