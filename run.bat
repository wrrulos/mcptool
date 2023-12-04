@echo off

set "python_var=python"

IF EXIST .\env\Scripts\activate (
    call .\env\Scripts\activate
)

%python_var% main.py
