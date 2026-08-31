@echo off
cd /d "%~dp0"
echo ============================================
echo   Running drills.py
echo ============================================
echo.

where python >nul 2>nul
if %errorlevel%==0 (
    python drills.py
) else (
    py drills.py
)

echo.
echo ============================================
echo   Done. Press any key to close.
echo ============================================
pause >nul
