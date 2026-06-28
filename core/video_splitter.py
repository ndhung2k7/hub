"""
Video splitter core logic
"""

import os
import logging
from typing import Optional, List, Dict, Callable
from pathlib import Path
from video.video_processor import VideoProcessor
from video.video_info import VideoInfo


class VideoSplitter:
    """Core class for splitting videos"""
    
    def __init__(self):
        self.processor = VideoProcessor()
        self.current_video = None
        self.is_running = False
        self.clips = []
        
    def split_video(
        self,
        input_path: str,
        output_dir: str,
        mode: str = 'duration',  # 'duration' hoặc 'count'
        segment_duration: float = 30.0,
        segment_count: int = 10,
        copy_mode: bool = True,
        quality: int = 18,
        progress_callback: Optional[Callable] = None,
        log_callback: Optional[Callable] = None
    ) -> List[Dict]:
        """
        Chia video
        
        Args:
            input_path: Đường dẫn video đầu vào
            output_dir: Thư mục đầu ra
            mode: 'duration' hoặc 'count'
            segment_duration: Thời lượng mỗi clip (giây) - cho mode 'duration'
            segment_count: Số lượng clip - cho mode 'count'
            copy_mode: Sử dụng copy mode
            quality: CRF quality
            progress_callback: Callback cho tiến trình
            log_callback: Callback cho log
            
        Returns:
            Danh sách thông tin clip
        """
        self.is_running = True
        self.clips = []
        
        try:
            # Kiểm tra file đầu vào
            if not os.path.exists(input_path):
                raise FileNotFoundError(f"Không tìm thấy file: {input_path}")
            
            # Tạo thư mục đầu ra
            os.makedirs(output_dir, exist_ok=True)
            
            # Lấy thông tin video
            if log_callback:
                log_callback("Đang đọc thông tin video...")
            
            video_info = VideoInfo(input_path)
            if not video_info.load_info():
                raise RuntimeError("Không thể đọc thông tin video")
            
            total_duration = video_info.duration
            if total_duration <= 0:
                raise RuntimeError("Thời lượng video không hợp lệ")
            
            if log_callback:
                log_callback(f"Thời lượng video: {video_info.get_duration_str()}")
                log_callback(f"Độ phân giải: {video_info.get_resolution()}")
                log_callback(f"FPS: {video_info.get_fps_str()}")
            
            # Tính toán thời lượng mỗi clip
            if mode == 'count':
                if segment_count <= 0:
                    raise ValueError("Số lượng clip phải lớn hơn 0")
                segment_duration = total_duration / segment_count
                if log_callback:
                    log_callback(f"Chia thành {segment_count} clip, mỗi clip {segment_duration:.1f} giây")
            else:
                if segment_duration <= 0:
                    raise ValueError("Thời lượng clip phải lớn hơn 0")
                if log_callback:
                    segment_count = int(total_duration / segment_duration) + 1
                    log_callback(f"Chia theo thời lượng {segment_duration:.1f} giây, dự kiến {segment_count} clip")
            
            # Thực hiện chia
            if log_callback:
                log_callback("Bắt đầu chia video...")
            
            self.clips = self.processor.split_video(
                input_path,
                output_dir,
                segment_duration,
                copy_mode,
                quality
            )
            
            if log_callback:
                log_callback(f"Đã chia thành {len(self.clips)} clip")
            
            # Gọi progress callback
            if progress_callback:
                progress_callback(100, len(self.clips))
            
            self.is_running = False
            return self.clips
            
        except Exception as e:
            self.is_running = False
            if log_callback:
                log_callback(f"LỖI: {str(e)}")
            raise
        
        finally:
            self.is_running = False
    
    def get_clips(self) -> List[Dict]:
        """Lấy danh sách clip đã tạo"""
        return self.clips
    
    def cancel(self):
        """Hủy quá trình chia video"""
        self.is_running = False
