@echo off
echo Tao toan bo project Video Splitter...

REM Xóa project cũ nếu có
if exist VideoSplitter_new (
    rmdir /s /q VideoSplitter_new
)

mkdir VideoSplitter_new
cd VideoSplitter_new

REM Tạo cấu trúc thư mục
mkdir gui core video player utils log config resources

REM Tạo các file __init__.py
echo # GUI package > gui\__init__.py
echo # Core package > core\__init__.py
echo # Video package > video\__init__.py
echo # Player package > player\__init__.py
echo # Utils package > utils\__init__.py
echo # Log package > log\__init__.py
echo # Config package > config\__init__.py

REM Tạo file utils\file_utils.py
(
echo import os
echo import subprocess
echo import shutil
echo from pathlib import Path
echo from typing import Optional
echo.
echo def ensure_ffmpeg() -> Optional[str]:
echo     ffmpeg_path = shutil.which('ffmpeg')
echo     if ffmpeg_path:
echo         return ffmpeg_path
echo     local_ffmpeg = Path('ffmpeg.exe')
echo     if local_ffmpeg.exists():
echo         return str(local_ffmpeg)
echo     resources_ffmpeg = Path('resources/ffmpeg.exe')
echo     if resources_ffmpeg.exists():
echo         return str(resources_ffmpeg)
echo     return None
echo.
echo def get_file_size(file_path: str) -> str:
echo     try:
echo         size = os.path.getsize(file_path)
echo         for unit in ['B', 'KB', 'MB', 'GB']:
echo             if size < 1024.0:
echo                 return f"{size:.1f} {unit}"
echo             size /= 1024.0
echo         return f"{size:.1f} TB"
echo     except:
echo         return "0 B"
) > utils\file_utils.py

REM Tạo requirements.txt
echo PySide6==6.6.0 > requirements.txt
echo pyinstaller==6.3.0 >> requirements.txt

REM Tạo main.py
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

echo.
echo [OK] Project da duoc tao tai: %cd%
echo.
echo Tiep theo:
echo 1. Copy cac file khac (gui, core, video, player) vao day
echo 2. Chay: pip install -r requirements.txt
echo 3. Chay: python main.py
pause
