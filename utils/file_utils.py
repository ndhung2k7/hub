"""
Utility functions for file operations
"""

import os
import subprocess
import shutil
from pathlib import Path
from typing import Optional


def ensure_ffmpeg() -> Optional[str]:
    """
    Kiểm tra và tìm đường dẫn FFmpeg
    
    Returns:
        Đường dẫn đến ffmpeg hoặc None nếu không tìm thấy
    """
    # Kiểm tra trong PATH
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path:
        return ffmpeg_path
    
    # Kiểm tra trong thư mục hiện tại
    local_ffmpeg = Path('ffmpeg.exe')
    if local_ffmpeg.exists():
        return str(local_ffmpeg)
    
    # Kiểm tra trong thư mục resources
    resources_ffmpeg = Path('resources/ffmpeg.exe')
    if resources_ffmpeg.exists():
        return str(resources_ffmpeg)
    
    return None


def ensure_ffprobe() -> Optional[str]:
    """
    Kiểm tra và tìm đường dẫn FFprobe
    
    Returns:
        Đường dẫn đến ffprobe hoặc None nếu không tìm thấy
    """
    ffprobe_path = shutil.which('ffprobe')
    if ffprobe_path:
        return ffprobe_path
    
    local_ffprobe = Path('ffprobe.exe')
    if local_ffprobe.exists():
        return str(local_ffprobe)
    
    resources_ffprobe = Path('resources/ffprobe.exe')
    if resources_ffprobe.exists():
        return str(resources_ffprobe)
    
    return None


def get_file_size(file_path: str) -> str:
    """
    Lấy dung lượng file dạng readable
    
    Args:
        file_path: Đường dẫn file
        
    Returns:
        String dung lượng (VD: 125.6 MB)
    """
    try:
        size = os.path.getsize(file_path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    except:
        return "0 B"


def get_file_extension(file_path: str) -> str:
    """Lấy phần mở rộng của file"""
    return Path(file_path).suffix.lower()


def is_video_file(file_path: str) -> bool:
    """Kiểm tra xem file có phải là video không"""
    video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', 
                       '.webm', '.m4v', '.mpg', '.mpeg', '.3gp'}
    return get_file_extension(file_path) in video_extensions


def create_directory(path: str) -> bool:
    """Tạo thư mục nếu chưa tồn tại"""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except:
        return False


def get_unique_filename(directory: str, base_name: str, extension: str) -> str:
    """
    Tạo tên file duy nhất trong thư mục
    
    Args:
        directory: Thư mục chứa file
        base_name: Tên cơ bản
        extension: Phần mở rộng (bao gồm dấu chấm)
        
    Returns:
        Đường dẫn file duy nhất
    """
    counter = 1
    while True:
        if counter == 1:
            filename = f"{base_name}{extension}"
        else:
            filename = f"{base_name}_{counter}{extension}"
        
        filepath = Path(directory) / filename
        if not filepath.exists():
            return str(filepath)
        counter += 1
