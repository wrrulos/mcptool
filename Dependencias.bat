@echo off

title Instalador de dependencias

echo.
echo [#] Verificando conexion...
timeout 2 >nul
echo.

ping www.google.com -n 2 >nul


if %errorlevel% == 0 goto pip

echo [X] Necesitas estar conectado a internet para instalar las dependencias!
echo.
pause>nul
exit

:pip
echo [#] Detectando si pip esta instalado...
echo.
timeout 2 >nul

pip >nul

if %errorlevel% == 0 goto dependencias

echo.
echo [X] Necesitas tener pip instalado!
echo.
pause>nul
exit

:dependencias
echo [#] Instalando dependencias...
echo.
pip install requests & pip install colorama
echo. 
echo [#] Dependencias instaladas correctamente.
pause >nul
exit