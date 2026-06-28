"""
Time utility functions
"""

from typing import Tuple


def seconds_to_time(seconds: float) -> str:
    """
    Chuyển đổi số giây sang định dạng thời gian HH:MM:SS
    
    Args:
        seconds: Số giây
        
    Returns:
        Chuỗi thời gian định dạng
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def time_to_seconds(time_str: str) -> float:
    """
    Chuyển đổi chuỗi thời gian sang số giây
    
    Args:
        time_str: Chuỗi thời gian (HH:MM:SS hoặc MM:SS)
        
    Returns:
        Số giây
    """
    parts = time_str.split(':')
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    elif len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    else:
        return float(time_str)


def format_duration(duration: float) -> str:
    """
    Định dạng thời lượng
    
    Args:
        duration: Thời lượng (giây)
        
    Returns:
        Chuỗi định dạng (VD: 1h 23m 45s)
    """
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = int(duration % 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    
    return " ".join(parts)