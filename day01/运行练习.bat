@echo off
chcp 65001 >nul
cd /d "%~dp0"
setlocal
cls
echo.
echo   ==========================================
echo      Day 1 练习题
echo   ==========================================
echo.
echo      [1] 题目版 - 自己填答案
echo      [2] 答案版 - 全部填好
echo      [3] 题2 专项讲解 - dict.get 是什么
echo.
set /p CHOICE=   输入 1 / 2 / 3 然后回车:
echo.

if "%CHOICE%"=="2" goto answer
if "%CHOICE%"=="3" goto explain
goto question

:answer
set FILE=drills_答案.py
goto run

:explain
set FILE=题2讲解.py
goto run

:question
set FILE=drills.py
goto run

:run
where py >nul 2>nul
if %errorlevel%==0 (
    py %FILE%
    goto done
)

where python >nul 2>nul
if %errorlevel%==0 (
    python %FILE%
    goto done
)

echo   [错误] 没找到 Python
echo   请先安装: https://www.python.org/downloads/
echo   安装时务必勾选 Add Python to PATH

:done
echo.
echo   ==========================================
echo     运行结束 - 按任意键关闭
echo   ==========================================
pause >nul
endlocal
