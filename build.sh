#!/usr/bin/env bash
echo "Fetching extensions..."
python build.py
echo "Clean up..."
cd public
find -type f \
    \( -name README.md \
       -o -name .babelrc \
       -o -name Gruntfile.js \
       -o -name package.json \
       -o -name "*.map" \) | xargs rm
find -maxdepth 2 -type d -name src | xargs rm -rf
find -maxdepth 2 -type d -name vendor | xargs rm -rf
echo "Clean up finished."
echo "Post building..."
cp _headers public/
echo "Build finished."
