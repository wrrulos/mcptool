:: Delete .\dist and .\build directories
DEL /Q /S .\dist > NUL

:: Start the build
python dist.py build
python dist.py bdist_msi
