if exist ".git/refs/heads/master" ( set /p GITCOMMIT=<".git/refs/heads/master" ) else ( set GITCOMMIT=unknown )

c:\python27\python.exe setup.py py2exe

cd dist

echo Commit: %GITCOMMIT% > buildinfo
echo Build: %BUILD_TAG% >> buildinfo
echo Build URL: %BUILD_URL% >> buildinfo

copy ..\dist_tools\pyFetch.bat .
copy c:\python27\lib\site-packages\Pythonwin\mfc90.dll Microsoft.VC90.MFC.dll

xcopy /F /Y /E ..\pyFetch pyFetch

"c:\Program Files (x86)\7-Zip\7z.exe" a -y ..\pyFetch.7z *

cd ..

copy /b "c:\Program Files (x86)\7-Zip\7zS.sfx" + dist_tools\sfxconfig.txt + pyFetch.7z pyFetch.exe
