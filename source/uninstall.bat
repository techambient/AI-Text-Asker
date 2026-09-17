@echo off
setlocal

echo [1/3] Removing shortcuts from Start Menu and Startup...
if exist "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\AI Text Asker.lnk" (
    del /F /Q "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\AI Text Asker.lnk"
    echo Success: Start Menu Programs shortcut removed.
) else (
    echo Notice: Start Menu Programs shortcut not found.
)

if exist "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\AI Text Asker.lnk" (
    del /F /Q "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\AI Text Asker.lnk"
    echo Success: Startup shortcut removed.
) else (
    echo Notice: Startup shortcut not found.
)
echo.

echo [2/3] Removing application directory and files...
if exist "C:\Program Files\AI Text Asker" (
    rd /S /Q "C:\Program Files\AI Text Asker"
    echo Success: Installation folder removed.
) else (
    echo Notice: Installation folder not found.
)
echo.

echo [3/3] Uninstallation completed successfully!
echo ==========================================
pause

endlocal