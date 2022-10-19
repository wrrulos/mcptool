@echo off
color 0f
net session >nul 2>&1

if "%errorlevel%" == "0" (
    echo.
    echo [x] You must start the file without administrator permissions!
    echo.
    pause >nul 2>&1
    exit
)

:detect_python
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
        echo [-] If you think this is a bug, please contact me or start MCPTool manually.
        pause >nul 2>&1
        exit
    )
)

%python_command% MCPTool.py
