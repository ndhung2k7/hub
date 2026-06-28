"""
Video processing using FFmpeg
"""

import subprocess
import os
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from utils.file_utils import ensure_ffmpeg
from video.video_info import VideoInfo


class VideoProcessor:
    """Class xử lý video với FFmpeg"""
    
    def __init__(self):
        self.ffmpeg_path = ensure_ffmpeg()
        if not self.ffmpeg_path:
            raise RuntimeError("FFmpeg not found")
    
    def cut_video(
        self,
        input_path: str,
        output_path: str,
        start_time: float,
        duration: float,
        copy_mode: bool = True,
        quality: int = 18
    ) -> Tuple[bool, str]:
        """
        Cắt video từ start_time với duration giây
        
        Args:
            input_path: Đường dẫn file đầu vào
            output_path: Đường dẫn file đầu ra
            start_time: Thời điểm bắt đầu (giây)
            duration: Thời lượng cần cắt (giây)
            copy_mode: Sử dụng copy mode (không re-encode)
            quality: CRF quality (1-51, thấp hơn = chất lượng tốt hơn)
            
        Returns:
            (success, message)
        """
        try:
            # Tạo thư mục đầu ra
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            cmd = [self.ffmpeg_path, '-y']
            
            # Input
            cmd.extend(['-ss', str(start_time)])
            cmd.extend(['-i', input_path])
            
            # Duration
            if duration > 0:
                cmd.extend(['-t', str(duration)])
            
            if copy_mode:
                # Copy mode - không re-encode
                cmd.extend(['-c', 'copy'])
            else:
                # Re-encode với chất lượng cao
                cmd.extend([
                    '-c:v', 'libx264',
                    '-preset', 'fast',
                    '-crf', str(quality),
                    '-c:a', 'aac',
                    '-b:a', '192k'
                ])
            
            # Output
            cmd.append(output_path)
            
            # Chạy FFmpeg
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0 and os.path.exists(output_path):
                return True, "Thành công"
            else:
                error_msg = result.stderr if result.stderr else "Lỗi không xác định"
                return False, error_msg
                
        except Exception as e:
            return False, str(e)
    
    def split_video(
        self,
        input_path: str,
        output_dir: str,
        segment_duration: float,
        copy_mode: bool = True,
        quality: int = 18
    ) -> List[Dict]:
        """
        Chia video thành nhiều đoạn
        
        Args:
            input_path: Đường dẫn file đầu vào
            output_dir: Thư mục đầu ra
            segment_duration: Thời lượng mỗi đoạn (giây)
            copy_mode: Sử dụng copy mode
            quality: CRF quality
            
        Returns:
            Danh sách thông tin các clip đã tạo
        """
        # Lấy thông tin video
        video_info = VideoInfo(input_path)
        if not video_info.load_info():
            raise RuntimeError("Không thể đọc thông tin video")
        
        total_duration = video_info.duration
        if total_duration <= 0:
            raise RuntimeError("Thời lượng video không hợp lệ")
        
        # Tạo thư mục đầu ra
        os.makedirs(output_dir, exist_ok=True)
        
        # Lấy tên file không có extension
        base_name = Path(input_path).stem
        
        # Tạo các clip
        clips_info = []
        start_time = 0.0
        clip_number = 1
        
        while start_time < total_duration:
            # Tính thời lượng cho clip cuối
            remaining = total_duration - start_time
            current_duration = min(segment_duration, remaining)
            
            # Tạo tên file
            output_path = os.path.join(
                output_dir,
                f"Clip_{clip_number:03d}.mp4"
            )
            
            # Đảm bảo tên file duy nhất
            counter = 1
            while os.path.exists(output_path):
                output_path = os.path.join(
                    output_dir,
                    f"Clip_{clip_number:03d}_{counter}.mp4"
                )
                counter += 1
            
            # Cắt video
            success, message = self.cut_video(
                input_path,
                output_path,
                start_time,
                current_duration,
                copy_mode,
                quality
            )
            
            if success:
                # Lấy thông tin clip
                clip_info = VideoInfo(output_path)
                clip_info.load_info()
                
                clips_info.append({
                    'path': output_path,
                    'name': Path(output_path).name,
                    'start_time': start_time,
                    'duration': current_duration,
                    'duration_str': clip_info.get_duration_str(),
                    'size': clip_info.size,
                    'index': clip_number
                })
            
            start_time += current_duration
            clip_number += 1
        
        return clips_info
    
    def get_video_info(self, file_path: str) -> Optional[Dict]:
        """Lấy thông tin video dưới dạng dict"""
        video_info = VideoInfo(file_path)
        if video_info.load_info():
            return video_info.to_dict()
        return None
