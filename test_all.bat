@echo off
chcp 65001 > nul
echo Running all configuration tests...
echo.

echo === Test 1: Config file ===
python main.py --config-file config.toml
echo.

echo === Test 2: Command line parameters ===
python main.py --vfs-path ./custom_vfs --startup-script ./custom_script.txt
echo.

echo === Test 3: Mixed mode ===
python main.py --config-file config.toml --vfs-path ./override_vfs
echo.

echo All tests completed!
pause