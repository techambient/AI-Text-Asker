@echo off
setlocal

:: Get the directory where setup.bat is currently running from
set "SCRIPT_DIR=%~dp0"
:: Remove trailing backslash for clean path handling
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

echo [1/5] Creating installation directory...
if not exist "C:\Program Files\AI Text Asker" (
    mkdir "C:\Program Files\AI Text Asker"
)
echo Success: Directory ready.
echo.

echo [2/5] Copying application executable...
if exist "%SCRIPT_DIR%\ai-text-asker-v1.exe" (
    copy /Y "%SCRIPT_DIR%\ai-text-asker-v1.exe" "C:\Program Files\AI Text Asker\ai-text-asker-v1.exe"
) else (
    echo [ERROR] ai-text-asker-v1.exe not found in the same folder as setup.bat!
    goto error
)
echo Success: Executable copied.
echo.

echo [3/5] Creating startup shortcut...
powershell -ExecutionPolicy Bypass -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\AI Text Asker.lnk'); $s.TargetPath = 'C:\Program Files\AI Text Asker\ai-text-asker-v1.exe'; $s.WorkingDirectory = 'C:\Program Files\AI Text Asker'; $s.Save()"
echo Success: Startup shortcut created.
echo.

echo [4/5] Copying shortcut to Start Menu Programs...
if exist "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\AI Text Asker.lnk" (
    copy /Y "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\AI Text Asker.lnk" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\AI Text Asker.lnk"
) else (
    echo [ERROR] Startup shortcut could not be found to copy.
    goto error
)
echo Success: Shortcut copied to Start Menu Programs.
echo.

echo [5/5] Setup completed, please close this cmd...
if exist "%SCRIPT_DIR%\done.ps1" (
    powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%\done.ps1"
) else (
    echo [WARNING] done.ps1 was not found in the same folder, skipping step.
)
echo.

echo ==========================================
echo Setup completed successfully!
echo ==========================================
goto end

:error
echo.
echo Setup failed due to missing files or permissions. Please ensure you ran setup.bat as Administrator.
pause

:end
endlocal