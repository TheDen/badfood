#!/bin/bash
BADFOOD_DATA=$(cat badfood_data.json | jq -c '.')
export BADFOOD_DATA
envsubst < index.pre.html > index.html

rm -rf dist/
rsync --exclude=index.pre.html \
  --exclude=*.sh \
  -exclude=dist/ \
  --exclude=.git* \
  --exclude=LICENSE \
  --exclude=README.md \
  --exclude=spiders/ \
  --exclude=.prettierignore \
  --exclude=badfood_data.json \
  --exclude=requirements.txt \
  --exclude=images/*.xcf \
  --delete -av . dist/

prettier -w .

echo "Minifying everything we can"
find ./dist/ -type f \( \
  -name "*.html" \
  -o -name '*.js' \
  -o -name '*.css' \
  -o -name '*.svg' \
  -o -name "*.xml" \
  -o -name "*.json" \
  -o -name "*.html" \
  \) \
  -and ! -name "*.min*" -print0 |
  xargs -0 -n1 -P4 -I '{}' sh -c 'minify -o "{}" "{}"'
