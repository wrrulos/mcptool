@echo off

title MCP Tool Installer

:: Detecta si tiene conexion a internet

echo.
echo [#] Detecting internet connection..
timeout 2 >nul
echo.

ping www.google.com -n 2 >nul

if %errorlevel% == 0 goto pip

cls
echo.
echo [X] You need an internet connection to install the dependencies.
echo.
pause>nul
exit

:pip
echo [#] Detecting if pip is installed...
timeout 2 >nul
pip >nul
if %errorlevel% == 0 goto dependencias

echo.
echo [X] You need to have pip installed.
echo.
pause>nul
exit

:dependencias
pip install pyfiglet && pip install mcstatus && pip install requests && pip install future && pip install colorama && pip install cryptography
echo.
echo [#] Correctly installed dependencies
pause >nul
exit
