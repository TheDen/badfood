#!/bin/bash
export BADFOOD_DATA=$(cat badfood_data.json | jq -c '')
cat index.pre.html | envsubst > index.html

rsync --exclude=index.pre.html --exclude=sync.sh --exclude=dist/ --exclude=.git/ --exclude=.gitignore --exclude=node_modules --delete -av . dist/

echo "Minifying everything we can"
find ./dist/ -type f \( \
  -name "*.html" \
  -o -name '*.js' \
  -o -name '*.css' \
  -o -name '*.svg' \
  -o -name "*.xml" \
  -o -name "*.json" \
  -o -name "*.htm" \
  \) \
  -and ! -name "*.min*" -print0 |
  xargs -0 -n1 -P4 -I '{}' sh -c 'minify -o "{}" "{}"'
