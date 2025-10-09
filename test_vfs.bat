@echo off
chcp 65001 >nul
echo ========================================
echo    File System Emulator - VFS Tests
echo ========================================
echo.

echo Step 1: Creating test CSV files...
call :create_csv_files

echo.
echo Step 2: Running tests with different VFS configurations...
echo.

echo === Test 1: Simple VFS ===
python main.py --vfs-csv vfs_simple.csv --startup-script test_simple_commands.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Simple VFS test failed!
    pause
    exit /b 1
)

echo.
echo === Test 2: Medium VFS ===
python main.py --vfs-csv vfs_medium.csv --startup-script test_medium_commands.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Medium VFS test failed!
    pause
    exit /b 1
)

echo.
echo === Test 3: Complex VFS ===
python main.py --vfs-csv vfs_complex.csv --startup-script test_complex_commands.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Complex VFS test failed!
    pause
    exit /b 1
)

echo.
echo === Test 4: All Commands ===
python main.py --vfs-csv vfs_complex.csv --startup-script test_all_commands.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: All commands test failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo    All tests completed successfully!
echo ========================================
pause
exit /b 0