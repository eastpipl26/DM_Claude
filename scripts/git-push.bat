@echo off
pushd "%~dp0"
git add .
git commit -m "업데이트"
git push
popd
pause
