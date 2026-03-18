@echo off
rem Start the BAC Study Organizer application (Python backend + browser UI)

rem Activate the virtual environment if it exists
if exist "%~dp0.venv\Scripts\activate.bat" (
  call "%~dp0.venv\Scripts\activate.bat"
)

rem Run the desktop launcher (starts the server and opens the browser)
python "%~dp0run.py"

pause