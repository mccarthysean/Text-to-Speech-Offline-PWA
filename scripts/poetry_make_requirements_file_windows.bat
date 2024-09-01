@echo off
REM Enable exit on error
setlocal enabledelayedexpansion
cd /d "%~dp0"
cd ..
echo Current working directory: %cd%

echo.
echo Making requirements.prod.txt and requirements.dev.txt...

poetry export --no-interaction --no-ansi --without-hashes --format requirements.txt --only main --output .\requirements.prod.txt
poetry export --no-interaction --no-ansi --without-hashes --format requirements.txt --only dev --output .\requirements.dev.txt

echo.
echo Process complete!

exit /b 0
