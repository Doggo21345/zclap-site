#!/bin/sh
# Makes dist/ and zclap-site-production.zip for zclap.com: drops the preview-only
# noindex tag and points estimator links back at the site's own /estimator/.
set -e
cd "$(dirname "$0")"
rm -rf dist zclap-site-production.zip
mkdir -p dist
cp -R index.html healthcare styles.css site.js assets dist/
find dist -name '*.html' -exec sed -i.bak \
  -e '/<meta name="robots" content="noindex">/d' \
  -e 's#https://zclap.com/estimator/#/estimator/#g' {} \;
find dist -name '*.bak' -delete
(cd dist && zip -qr ../zclap-site-production.zip .)
echo "dist/ and zclap-site-production.zip ready"
