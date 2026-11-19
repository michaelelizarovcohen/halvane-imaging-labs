#!/bin/sh
# Install the pre-push content gate into this clone.
set -e
top=$(git rev-parse --show-toplevel)
cat > "$top/.git/hooks/pre-push" <<'HOOK'
#!/bin/sh
top=$(git rev-parse --show-toplevel)
exec python3 "$top/scripts/prepush_check.py" --hook
HOOK
chmod +x "$top/.git/hooks/pre-push"
echo "pre-push hook installed"
