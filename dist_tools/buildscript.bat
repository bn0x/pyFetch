if exist ".git/refs/heads/master" ( set /p GITCOMMIT=<".git/refs/heads/master" ) else ( set GITCOMMIT=unknown )
echo Commit: %GITCOMMIT% > buildinfo
echo Build: %BUILD_TAG% >> buildinfo
echo Build URL: %BUILD_URL% >> buildinfo

c:\python27\python.exe C:\Python27\Lib\site-packages\pyinstaller\pyinstaller.py -F pyFetch.py