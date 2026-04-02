@echo off
echo ================================
echo   Compilation Bignon AquaStock
echo ================================
echo.

call venv\Scripts\activate

echo Nettoyage ancien build...
rmdir /s /q build
rmdir /s /q dist

echo.
echo Compilation en cours...
pyinstaller bignon.spec --clean

echo.
echo ================================
echo   COMPILATION TERMINEE !
echo   Dossier : dist\BignonAquaStock
echo ================================
pause