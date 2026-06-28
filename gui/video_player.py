"""
Video player widget using QMediaPlayer
"""

import os
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QSlider, QLabel, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QUrl, QTimer, Signal, Slot


class VideoPlayer(QWidget):
    """Custom video player widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Khởi tạo media player
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        
        # Setup UI
        self.setup_ui()
        
        # Kết nối signals
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)
        self.player.mediaStatusChanged.connect(self.handle_media_status)
        self.player.playbackStateChanged.connect(self.handle_playback_state)
        self.player.errorOccurred.connect(self.handle_player_error)
        
        # Timer để cập nhật UI
        self.update_timer = QTimer()
        self.update_timer.setInterval(100)
        self.update_timer.timeout.connect(self.update_ui)
        
        # Set volume
        self.audio_output.setVolume(0.8)
    
    def setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Video widget
        self.video_widget = QVideoWidget()
        self.video_widget.setStyleSheet("background-color: #000000;")
        self.player.setVideoOutput(self.video_widget)
        layout.addWidget(self.video_widget)
        
        # Controls
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(5)
        
        # Timeline
        timeline_layout = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 1000)
        self.slider.sliderMoved.connect(self.seek)
        timeline_layout.addWidget(self.slider)
        controls_layout.addLayout(timeline_layout)
        
        # Playback controls
        buttons_layout = QHBoxLayout()
        
        self.btn_play = QPushButton("▶")
        self.btn_play.setFixedSize(40, 40)
        self.btn_play.clicked.connect(self.toggle_play)
        buttons_layout.addWidget(self.btn_play)
        
        self.btn_stop = QPushButton("⏹")
        self.btn_stop.setFixedSize(40, 40)
        self.btn_stop.clicked.connect(self.stop)
        buttons_layout.addWidget(self.btn_stop)
        
        # Time labels
        self.lbl_current_time = QLabel("00:00")
        buttons_layout.addWidget(self.lbl_current_time)
        
        self.lbl_separator = QLabel("/")
        buttons_layout.addWidget(self.lbl_separator)
        
        self.lbl_total_time = QLabel("00:00")
        buttons_layout.addWidget(self.lbl_total_time)
        
        buttons_layout.addStretch()
        
        # Volume
        btn_volume = QPushButton("🔊")
        btn_volume.setFixedSize(30, 30)
        btn_volume.clicked.connect(self.toggle_mute)
        buttons_layout.addWidget(btn_volume)
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        self.volume_slider.setFixedWidth(80)
        self.volume_slider.valueChanged.connect(self.set_volume)
        buttons_layout.addWidget(self.volume_slider)
        
        controls_layout.addLayout(buttons_layout)
        layout.addLayout(controls_layout)
    
    def load_video(self, file_path):
        """Load video từ file"""
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy file video")
            return
        
        # Dừng phát hiện tại
        self.player.stop()
        
        # Load video mới
        url = QUrl.fromLocalFile(file_path)
        self.player.setSource(url)
        
        # Reset UI
        self.slider.setValue(0)
        self.lbl_current_time.setText("00:00")
        self.btn_play.setText("▶")
        
        # Bắt đầu cập nhật timer
        self.update_timer.start()
    
    def play(self):
        """Phát video"""
        if self.player.playbackState() != QMediaPlayer.PlayingState:
            self.player.play()
    
    def pause(self):
        """Tạm dừng video"""
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
    
    def stop(self):
        """Dừng video"""
        self.player.stop()
        self.slider.setValue(0)
        self.lbl_current_time.setText("00:00")
        self.btn_play.setText("▶")
    
    def toggle_play(self):
        """Chuyển đổi play/pause"""
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.pause()
        else:
            self.play()
    
    def seek(self, position):
        """Tua đến vị trí"""
        duration = self.player.duration()
        if duration > 0:
            seek_pos = int(position / 1000.0 * duration)
            self.player.setPosition(seek_pos)
    
    def set_volume(self, value):
        """Điều chỉnh âm lượng"""
        self.audio_output.setVolume(value / 100.0)
    
    def toggle_mute(self):
        """Bật/tắt tiếng"""
        self.audio_output.setMuted(not self.audio_output.isMuted())
    
    def update_position(self, position):
        """Cập nhật vị trí hiện tại"""
        duration = self.player.duration()
        if duration > 0:
            # Cập nhật slider
            progress = int(position / duration * 1000)
            self.slider.setValue(progress)
            
            # Cập nhật thời gian
            current_time = self.format_time(position)
            self.lbl_current_time.setText(current_time)
    
    def update_duration(self, duration):
        """Cập nhật thời lượng"""
        if duration > 0:
            total_time = self.format_time(duration)
            self.lbl_total_time.setText(total_time)
    
    def format_time(self, milliseconds):
        """Định dạng thời gian từ milliseconds"""
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        
        return f"{minutes:02d}:{seconds:02d}"
    
    def update_ui(self):
        """Cập nhật UI định kỳ"""
        # Cập nhật trạng thái play/pause
        state = self.player.playbackState()
        if state == QMediaPlayer.PlayingState:
            self.btn_play.setText("⏸")
        elif state == QMediaPlayer.PausedState:
            self.btn_play.setText("▶")
        
        # Tự động dừng timer khi video kết thúc
        if state == QMediaPlayer.StoppedState:
            if self.player.position() >= self.player.duration() and self.player.duration() > 0:
                self.btn_play.setText("▶")
    
    def handle_media_status(self, status):
        """Xử lý thay đổi trạng thái media"""
        if status == QMediaPlayer.LoadedMedia:
            # Video đã load xong
            pass
        elif status == QMediaPlayer.EndOfMedia:
            # Video kết thúc
            self.btn_play.setText("▶")
            self.slider.setValue(0)
            self.lbl_current_time.setText("00:00")
    
    def handle_playback_state(self, state):
        """Xử lý thay đổi playback state"""
        if state == QMediaPlayer.PlayingState:
            self.btn_play.setText("⏸")
        else:
            self.btn_play.setText("▶")
    
    def handle_player_error(self, error):
        """Xử lý lỗi player"""
        if error != QMediaPlayer.NoError:
            error_msg = self.player.errorString()
            QMessageBox.warning(self, "Lỗi video", f"Lỗi khi phát video:\n{error_msg}")
