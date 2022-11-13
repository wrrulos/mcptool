@echo off
color 0f
title MCPTool Installer
mode con cols=80 lines=18
net session >nul 2>&1

if "%errorlevel%" == "0" (
    echo.
    echo [x] You must start the installer without administrator permissions!
    echo.
    pause >nul 2>&1
    exit
)

:question
cls
echo.
set /p question="Do you want to set the ngrok authtoken? y/n "

if "%question%" == "y" (
    set /p authtoken="Enter the authtoken of ngrok: "
    goto save_variables
)

if "%question%" == "Y" (
    set /p authtoken="Enter the authtoken of ngrok: "
    goto save_variables
)

if "%question%" == "n" (
    set authtoken=none
    goto save_variables
)

if "%question%" == "N" (
    set authtoken=none
    goto save_variables
)

goto question

:save_variables
:: Reset errorlevel
call (exit /b 0)

:: Save the python variable
python3 --version >nul 2>&1

if "%errorlevel%" == "0" (
    set python_command=python3
)

call (exit /b 0)
python --version >nul 2>&1

if "%python_command%" == "" (
    if "%errorlevel%" == "0" (
        set python_command=python

    ) else (
        :: Python is not installed.
        echo [#] Python is not installed. Install it and run the script again.
        echo. 
        echo [-] If you think this is a bug, contact me or install dependencies manually.
        pause >nul 2>&1
        exit
    )
)

call (exit /b 0)
call npm --version >nul 2>&1

if "%errorlevel%" == "0" (
    echo.
) else (
    :: Python is not installed.
    echo [#] NodeJS is not installed. Install it and run the script again.
    echo. 
    echo [-] If you think this is a bug, contact me or install dependencies manually.
    pause >nul 2>&1
    exit
)

call (exit /b 0)
ngrok -v >nul 2>&1

if "%errorlevel%" == "0" (
    echo.
) else (
    :: Python is not installed.
    echo [#] Ngrok is not installed. Install it and run the script again.
    echo. 
    echo [-] If you think this is a bug, contact me or install dependencies manually.
    pause >nul 2>&1
    exit
)

:install_dependencies
echo.
echo [#] Installing dependencies..
echo.

%python_command% -m pip install -r requirements.txt 
call npm install mineflayer 
call npm install process 
call npm install socks
call npm install proxy-agent 
call npm install readline

if not "%authtoken%" == "none" (
    ngrok config add-authtoken %authtoken%
)
    
cls
title MCPTool Installer
color a
echo.
echo Dependencies installed.
echo.
echo You can now start MCPTool.
echo You can start it by opening the MCPTool.bat file or 
echo by opening a terminal and typing python main.py
echo.
echo https://github.com/wrrulos/
echo.
pause >nul 2>&1