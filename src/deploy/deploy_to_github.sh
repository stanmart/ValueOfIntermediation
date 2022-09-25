set -e
set -u

source=$1
target=$2
target_folder=$(dirname "$target")

cp $source $target

rm -rf "$target_folder/.git"
cd $target_folder

git init --initial-branch=main
git add -A
git commit -m 'Deploy to GH pages'
git push -f git@github.com:stanmart/ValueOfIntermediation.git main:gh-pages

rm -rf .git
