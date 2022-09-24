$ErrorActionPreference = "Stop"

$source = $args[0]
$target = $args[1]
$target_folder = Split-Path $target -Parent

Copy-Item $source $target

if (Test-Path "$target_folder/.git") {
    Remove-Item -Recurse -Force "$target_folder/.git"
}
Set-Location $target_folder

git init --initial-branch=main
git add -A
git commit -m 'Deploy to GH pages'
git push -f git@github.com:stanmart/ValueOfIntermediation.git main:gh-pages

Remove-Item -Recurse -Force .git
