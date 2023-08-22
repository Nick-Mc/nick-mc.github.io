#!/bin/bash
date=$(date)
git pull origin master
rm -r docs
mkdir docs
cd docs
echo "https://nick-mc.github.io" > CNAME
cd -
<<<<<<< HEAD
ECTO1_SOURCE=http://localhost:2368 ECTO1_TARGET=https://nick-mc.github.io python3 ecto1.py
cd docs
docker cp nickmc_ghost_1:/var/lib/ghost/content/images/. content/images
=======
ECTO1_SOURCE=http://SERVERIP:2368 ECTO1_TARGET=https://nick-mc.github.io python3 ecto1.py
cd docs
docker cp ghost:/var/lib/ghost/content/images/. content/images
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
cd -
grep -lR "srcset" docs/ | xargs sed -i 's/srcset/thisisbuggedatm/g'
git add .
git commit -m "$date"
git config --global credential.helper store
<<<<<<< HEAD
git push -u origin master
=======
git push -u origin master
>>>>>>> 72864d1 (Tue 22 Aug 2023 02:44:06 PM CDT)
