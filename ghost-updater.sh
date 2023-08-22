#!/bin/bash
date=$(date)
git pull origin master
rm -r docs
mkdir docs
cd docs
echo "https://nick-mc.github.io" > CNAME
cd -
ECTO1_SOURCE=http://localhost:2368 ECTO1_TARGET=https://nick-mc.github.io python3 ecto1.py
cd docs
docker cp mywebsite-ghost-1:/var/lib/ghost/content/images/. content/images
cd -
grep -lR "srcset" docs/ | xargs sed -i 's/srcset/thisisbuggedatm/g'
git add .
git commit -m "$date"
git config --global credential.helper store
git push -u origin master
