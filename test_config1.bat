@echo off
chcp 65001 > nul
echo Test 1: Run with config file
python main.py --config-file config.toml
echo Test 1 completed
pause