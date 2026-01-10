@echo off
SETLOCAL

:: --- CONFIGURATION ---
SET DB_SERVER=Q556\SQLPASS
SET DB_NAME=PassepartoutRetail
SET SQL_FILE=temp_create_func.sql

:: --- 1. CREATE THE SQL FILE ---
echo Creating SQL script...
(
echo USE [%DB_NAME%];
echo GO
echo CREATE OR ALTER FUNCTION dbo.clnstr (@str NVARCHAR(MAX^)^)
echo RETURNS NVARCHAR(MAX^)
echo AS
echo BEGIN
echo     IF @str IS NULL RETURN NULL;
echo     SET @str = REPLACE(REPLACE(REPLACE(REPLACE(@str, CHAR(13^), ''^), CHAR(10^), ''^), '^|', ' '^), '\', ' '^);
echo     RETURN @str;
echo END;
echo GO
) > %SQL_FILE%

:: --- 2. RUN SQLCMD ---
echo Deploying to SQL Server...
:: Using Windows Authentication (-E). Change to -U user -P pass if needed.
sqlcmd -S %DB_SERVER% -d %DB_NAME% -i %SQL_FILE% -E

:: --- 3. CLEAN UP ---
if %ERRORLEVEL% EQU 0 (
    echo Deployment Successful!
    del %SQL_FILE%
) else (
    echo Error occurred during deployment.
)

pause
