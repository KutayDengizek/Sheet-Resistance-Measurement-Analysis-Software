@echo off
rem Double-click to start the Sheet Resistance Analysis app (see README.md).
cd /d "%~dp0"
uv sync --quiet || (echo. & echo Could not set up the Python environment. Is uv installed? & pause & exit /b 1)
start "" ".venv\Scripts\sheetres-gui.exe" %*
