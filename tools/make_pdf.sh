#!/bin/sh
# Prints the playbook page to downloads/mdm-saas-migration-playbook.pdf (FAQs expanded).
set -e
cd "$(dirname "$0")/.."
CH=$(ls -d ~/.cache/ms-playwright/chromium_headless_shell-*/*/ | tail -1)chrome-headless-shell
TMP=mdm-saas-migration-playbook/_print.html
sed -e 's#<details>#<details open>#g' \
    -e 's#<span class="kicker">#<p class="print-only" style="font-size:9pt;color:\#69717c">zclap.com/mdm-saas-migration-playbook · Informatica MDM consultants · info@zclap.com</p><span class="kicker">#' \
    mdm-saas-migration-playbook/index.html > "$TMP"
"$CH" --no-sandbox --disable-gpu --virtual-time-budget=8000 --no-pdf-header-footer \
  --print-to-pdf="$PWD/downloads/mdm-saas-migration-playbook.pdf" "file://$PWD/$TMP" 2>/dev/null
rm -f "$TMP"
ls -la downloads/
