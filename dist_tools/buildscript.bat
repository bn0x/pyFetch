c:\python27\python.exe setup.py py2exe

cd dist
copy ..\dist_tools\pyFetch.bat .
copy c:\python27\lib\site-packages\Pythonwin\mfc90.dll .
"c:\Program Files (x86)\7-Zip\7z.exe" a -y ..\pyFetch.7z *
cd ..

copy /b "c:\Program Files (x86)\7-Zip\7zS.sfx" + dist_tools\sfxconfig.txt + pyFetch.7z pyFetch.exe
