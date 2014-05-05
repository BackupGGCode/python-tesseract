python setup.py clean
del *wrap*
python setup.py bdist_wininst
dist\python-tesseract.win32-py2.7.exe
cd test-slim
python test.py
cd ..

