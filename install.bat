@ECHO off &setlocal

python --version 2>&1 | findstr "3.7 3.8 3.9"
IF NOT ERRORLEVEL 0 (
	ECHO Error: Please make sure you have Python 3.7, 3.8 or 3.9 in PATH
) ELSE (
	IF NOT EXIST ".\venv\" (
		ECHO Creating virtual environment...
		python -m venv venv
		ECHO Creation OK
	)
	ECHO Installing packages
	CALL venv\Scripts\activate.bat
	python -m pip install --upgrade pip setuptools wheel
	python -m pip install -r requirements.txt
	ECHO Installation OK
)
PAUSE
GOTO :eof