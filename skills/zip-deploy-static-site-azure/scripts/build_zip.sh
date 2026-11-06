#!/usr/bin/env bash
# Usage: build_zip.sh <site-repo-dir> <out.zip>
# Packages every git-tracked file of the site (minus repo-only clutter) plus server.js/package.json.
# Using `git ls-files` instead of hand-picking folders is deliberate: hand-picking once dropped
# pages/ and assets/, and every nav link 404'd.
set -euo pipefail
SITE=$(cd "$1" && pwd); mkdir -p "$(dirname "$2")"; OUT=$(cd "$(dirname "$2")" && pwd)/$(basename "$2"); HERE=$(cd "$(dirname "$0")" && pwd)
STAGE=$(mktemp -d); trap 'rm -rf "$STAGE"' EXIT
cd "$SITE"
# Exclude repo-only files; edit this list if the site genuinely needs one of them at runtime.
git ls-files -z | grep -zvE '^(docs/|skills/|tests?/|\.github/|\.gitignore$|Makefile$|AGENTS\.md$|CLAUDE\.md$|README\.md$|.*\.py$)' \
  | xargs -0 -I{} rsync -R "{}" "$STAGE/"
[ -f "$STAGE/server.js" ] || cp "$HERE/server.js" "$STAGE/server.js"
[ -f "$STAGE/package.json" ] || cat > "$STAGE/package.json" <<'JSON'
{ "name": "static-site", "version": "1.0.0", "private": true, "scripts": { "start": "node server.js" }, "engines": { "node": ">=22" } }
JSON
python3 "$HERE/check_links.py" "$STAGE"   # fail before deploying, not after
rm -f "$OUT"; (cd "$STAGE" && zip -qr "$OUT" .)
echo "built $OUT ($(unzip -l "$OUT" | tail -1 | awk '{print $2}') files)"
