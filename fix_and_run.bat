@echo off
title Fix Video Splitter
color 0E

echo ========================================
echo   SUA LOI VA CHAY VIDEO SPLITTER
echo ========================================
echo.

REM Xóa file main.py cũ nếu có
if exist main.py (
    echo Dang xoa main.py cu...
    del main.py
)

REM Tạo main.py mới
echo Dang tao main.py moi...
(
echo import sys
echo import os
echo from pathlib import Path
echo.
echo sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
echo.
echo from PySide6.QtWidgets import QApplication
echo from gui.main_window import MainWindow
echo from utils.file_utils import ensure_ffmpeg
echo.
echo def main():
echo     ffmpeg_path = ensure_ffmpeg()
echo     if not ffmpeg_path:
echo         print("LOI: Khong tim thay FFmpeg")
echo         input("Nhan Enter de thoat...")
echo         return 1
echo.
echo     app = QApplication(sys.argv)
echo     app.setStyle('Fusion')
echo     window = MainWindow()
echo     window.show()
echo     return app.exec()
echo.
echo if __name__ == '__main__':
echo     sys.exit(main())
) > main.py

echo [OK] Da tao main.py moi
echo.

REM Kiểm tra thư mục utils
if not exist "utils\file_utils.py" (
    echo [WARNING] Khong tim thay utils\file_utils.py
    echo Ban can copy toan bo source code vao day!
)

echo.
echo Dang chay Video Splitter...
echo ========================================
echo.
python main.py

pause
