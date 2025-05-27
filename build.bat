@echo off
setlocal

echo [*] Suppression des anciens builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist GestionBudgetUFR.exe del GestionBudgetUFR.exe

echo [*] Compilation avec le fichier .spec...
:: Activation de l'environnement virtuel si nécessaire
if exist env_pyqt\Scripts\activate (
    call env_pyqt\Scripts\activate
)

:: Vérifier si PyInstaller est bien installé
where pyinstaller >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [!] PyInstaller n'est pas installé. Installation en cours...
    pip install pyinstaller
)

:: Compilation
pyinstaller GestionBudgetUFR.spec

if %ERRORLEVEL% neq 0 (
    echo [X] Erreur lors de la compilation.
) else (
    echo [✓] Compilation terminée avec succès.
    echo [→] Exécutable disponible dans le dossier dist\GestionBudgetUFR\
)

pause
endlocal
