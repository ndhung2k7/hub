@echo off
echo Building Video Splitter...

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build executable
pyinstaller --onefile --windowed --name "VideoSplitter" --icon resources/icon.ico main.py

echo Build complete!
pause
