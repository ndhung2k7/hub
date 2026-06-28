"""
Video Splitter - Ứng dụng chia nhỏ video tự động
Main entry point
"""

import sys
import os
from pathlib import Path

# Thêm thư mục gốc vào sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from gui.main_window import MainWindow
from utils.file_utils import ensure_ffmpeg


def main():
    """Hàm khởi chạy ứng dụng chính"""
    # Kiểm tra FFmpeg
    ffmpeg_path = ensure_ffmpeg()
    if not ffmpeg_path:
        print("LỖI: Không tìm thấy FFmpeg. Vui lòng cài đặt FFmpeg và thêm vào PATH")
        print("Tải FFmpeg tại: https://ffmpeg.org/download.html")
        input("Nhấn Enter để thoát...")
        return 1

    # Khởi tạo ứng dụng
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Tạo và hiển thị cửa sổ chính
    window = MainWindow()
    window.show()

    # Chạy ứng dụng
    return app.exec()


if __name__ == '__main__':
    sys.exit(main())
