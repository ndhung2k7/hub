"""
Video information extraction using FFprobe
"""

import json
import subprocess
from typing import Optional, Dict, Any
from utils.file_utils import ensure_ffprobe


class VideoInfo:
    """Class lấy và lưu trữ thông tin video"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.duration: float = 0.0
        self.width: int = 0
        self.height: int = 0
        self.fps: float = 0.0
        self.bitrate: int = 0
        self.codec: str = ""
        self.audio_codec: str = ""
        self.format: str = ""
        self.size: str = ""
        self._loaded = False
    
    def load_info(self) -> bool:
        """
        Lấy thông tin video bằng FFprobe
        
        Returns:
            True nếu thành công, False nếu thất bại
        """
        ffprobe = ensure_ffprobe()
        if not ffprobe:
            return False
        
        try:
            cmd = [
                ffprobe,
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                self.file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            
            # Lấy thông tin format
            if 'format' in data:
                format_info = data['format']
                self.duration = float(format_info.get('duration', 0))
                self.bitrate = int(format_info.get('bit_rate', 0))
                self.format = format_info.get('format_name', '')
                self.size = format_info.get('size', '0')
            
            # Lấy thông tin streams
            if 'streams' in data:
                for stream in data['streams']:
                    if stream.get('codec_type') == 'video':
                        self.width = int(stream.get('width', 0))
                        self.height = int(stream.get('height', 0))
                        self.codec = stream.get('codec_name', '')
                        
                        # Lấy FPS
                        fps_str = stream.get('r_frame_rate', '0/0')
                        if '/' in fps_str:
                            num, den = fps_str.split('/')
                            if float(den) > 0:
                                self.fps = float(num) / float(den)
                        
                        # Nếu không có r_frame_rate, thử avg_frame_rate
                        if self.fps == 0:
                            fps_str = stream.get('avg_frame_rate', '0/0')
                            if '/' in fps_str:
                                num, den = fps_str.split('/')
                                if float(den) > 0:
                                    self.fps = float(num) / float(den)
                    
                    elif stream.get('codec_type') == 'audio':
                        self.audio_codec = stream.get('codec_name', '')
            
            self._loaded = True
            return True
            
        except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError):
            return False
    
    def is_loaded(self) -> bool:
        """Kiểm tra đã load thông tin chưa"""
        return self._loaded
    
    def get_duration_str(self) -> str:
        """Lấy thời lượng dạng HH:MM:SS"""
        from utils.time_utils import seconds_to_time
        return seconds_to_time(self.duration)
    
    def get_resolution(self) -> str:
        """Lấy độ phân giải dạng WxH"""
        return f"{self.width}x{self.height}"
    
    def get_fps_str(self) -> str:
        """Lấy FPS dạng string"""
        return f"{self.fps:.2f}"
    
    def get_bitrate_str(self) -> str:
        """Lấy bitrate dạng readable"""
        if self.bitrate > 0:
            if self.bitrate > 1000000:
                return f"{self.bitrate / 1000000:.2f} Mbps"
            elif self.bitrate > 1000:
                return f"{self.bitrate / 1000:.2f} Kbps"
            else:
                return f"{self.bitrate} bps"
        return "N/A"
    
    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi thông tin thành dictionary"""
        return {
            'file_path': self.file_path,
            'duration': self.duration,
            'duration_str': self.get_duration_str(),
            'width': self.width,
            'height': self.height,
            'resolution': self.get_resolution(),
            'fps': self.fps,
            'fps_str': self.get_fps_str(),
            'bitrate': self.bitrate,
            'bitrate_str': self.get_bitrate_str(),
            'codec': self.codec,
            'audio_codec': self.audio_codec,
            'format': self.format,
            'size': self.size
        }
