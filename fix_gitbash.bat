@echo off
echo Corrigindo Git Bash definitivamente...

REM Remove entradas duplicadas e adiciona os caminhos corretos
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "USERPATH=%%b"

REM Remove caminhos duplicados do Git se existirem
set "USERPATH=%USERPATH:;C:\Program Files\Git\bin=%"
set "USERPATH=%USERPATH:;C:\Program Files\Git\usr\bin=%"
set "USERPATH=%USERPATH:C:\Program Files\Git\bin;=%"
set "USERPATH=%USERPATH:C:\Program Files\Git\usr\bin;=%"

REM Adiciona os caminhos corretos
set "NEWPATH=%USERPATH%;C:\Program Files\Git\bin;C:\Program Files\Git\usr\bin"

REM Atualiza o registro
reg add "HKCU\Environment" /v PATH /t REG_EXPAND_SZ /d "%NEWPATH%" /f >nul 2>&1

echo PATH atualizado com sucesso!
echo.
echo Testando comandos diretamente...
echo.

REM Testa comandos diretamente dos diretórios
echo Testando git:
"C:\Program Files\Git\bin\git.exe" --version
echo.

echo Testando uname:
"C:\Program Files\Git\usr\bin\uname.exe" -a
echo.

echo Testando sed:
echo teste | "C:\Program Files\Git\usr\bin\sed.exe" "s/teste/funcionou/"
echo.

echo ========================================
echo IMPORTANTE: 
echo 1. Feche COMPLETAMENTE o Git Bash atual
echo 2. Abra um NOVO Git Bash
echo 3. Os comandos devem funcionar agora
echo ========================================
echo.
pause