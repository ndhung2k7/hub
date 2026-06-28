"""
Main window of the application
"""

import os
import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QSpinBox,
    QComboBox, QCheckBox, QProgressBar, QGroupBox,
    QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QFileDialog, QMessageBox, QSplitter,
    QPlainTextEdit, QApplication, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QIcon, QFont

from gui.styles import DARK_STYLE, PLAYER_STYLE
from gui.video_player import VideoPlayer
from core.video_splitter import VideoSplitter
from video.video_info import VideoInfo
from utils.file_utils import get_file_size


class SplitWorker(QThread):
    """Worker thread for splitting videos"""
    
    progress = Signal(int, int)  # current, total
    log = Signal(str)
    finished = Signal(list)
    error = Signal(str)
    
    def __init__(self, splitter, input_path, output_dir, mode, duration, count, copy_mode, quality):
        super().__init__()
        self.splitter = splitter
        self.input_path = input_path
        self.output_dir = output_dir
        self.mode = mode
        self.duration = duration
        self.count = count
        self.copy_mode = copy_mode
        self.quality = quality
    
    def run(self):
        try:
            # Định nghĩa callback cho progress
            def progress_callback(current, total):
                self.progress.emit(current, total)
            
            def log_callback(message):
                self.log.emit(message)
            
            # Chia video
            clips = self.splitter.split_video(
                self.input_path,
                self.output_dir,
                self.mode,
                self.duration,
                self.count,
                self.copy_mode,
                self.quality,
                progress_callback,
                log_callback
            )
            
            self.finished.emit(clips)
            
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main window class"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Splitter - Chia nhỏ video tự động")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(DARK_STYLE)
        
        # Khởi tạo
        self.current_video = None
        self.clips = []
        self.splitter = VideoSplitter()
        self.worker = None
        
        # Setup UI
        self.setup_ui()
        
        # Apply player style
        self.setStyleSheet(DARK_STYLE + PLAYER_STYLE)
    
    def setup_ui(self):
        """Setup user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Main splitter
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Controls
        left_panel = self.create_control_panel()
        main_splitter.addWidget(left_panel)
        
        # Right panel - Video player and clips
        right_panel = self.create_preview_panel()
        main_splitter.addWidget(right_panel)
        
        # Set splitter ratio
        main_splitter.setSizes([400, 800])
        
        main_layout.addWidget(main_splitter)
    
    def create_control_panel(self):
        """Create control panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        
        # 1. Video selection
        video_group = QGroupBox("📁 Chọn Video")
        video_layout = QVBoxLayout(video_group)
        
        # Select button
        btn_select = QPushButton("📂 Chọn Video")
        btn_select.clicked.connect(self.select_video)
        video_layout.addWidget(btn_select)
        
        # Video info
        self.lbl_video_info = QLabel("Chưa chọn video")
        self.lbl_video_info.setWordWrap(True)
        self.lbl_video_info.setStyleSheet("padding: 8px; background-color: #2d2d2d; border-radius: 4px;")
        video_layout.addWidget(self.lbl_video_info)
        
        layout.addWidget(video_group)
        
        # 2. Output directory
        output_group = QGroupBox("💾 Thư mục lưu")
        output_layout = QVBoxLayout(output_group)
        
        output_row = QHBoxLayout()
        self.lbl_output_dir = QLineEdit()
        self.lbl_output_dir.setReadOnly(True)
        self.lbl_output_dir.setPlaceholderText("Chọn thư mục xuất...")
        output_row.addWidget(self.lbl_output_dir)
        
        btn_output = QPushButton("📁")
        btn_output.setFixedWidth(40)
        btn_output.clicked.connect(self.select_output_dir)
        output_row.addWidget(btn_output)
        
        output_layout.addLayout(output_row)
        layout.addWidget(output_group)
        
        # 3. Split mode
        mode_group = QGroupBox("⚙️ Chế độ chia")
        mode_layout = QVBoxLayout(mode_group)
        
        # Mode selection
        mode_row = QHBoxLayout()
        mode_row.addWidget(QLabel("Chế độ:"))
        self.combo_mode = QComboBox()
        self.combo_mode.addItems(["Theo thời lượng", "Theo số clip"])
        self.combo_mode.currentIndexChanged.connect(self.on_mode_changed)
        mode_row.addWidget(self.combo_mode)
        mode_row.addStretch()
        mode_layout.addLayout(mode_row)
        
        # Duration
        duration_row = QHBoxLayout()
        duration_row.addWidget(QLabel("Thời lượng mỗi clip:"))
        self.spin_duration = QSpinBox()
        self.spin_duration.setRange(1, 3600)
        self.spin_duration.setValue(30)
        duration_row.addWidget(self.spin_duration)
        duration_row.addWidget(QLabel("giây"))
        duration_row.addStretch()
        mode_layout.addLayout(duration_row)
        
        # Count
        count_row = QHBoxLayout()
        count_row.addWidget(QLabel("Số clip:"))
        self.spin_count = QSpinBox()
        self.spin_count.setRange(1, 1000)
        self.spin_count.setValue(10)
        count_row.addWidget(self.spin_count)
        count_row.addStretch()
        mode_layout.addLayout(count_row)
        
        # Set initial visibility
        self.spin_duration.setVisible(True)
        self.spin_count.setVisible(False)
        
        layout.addWidget(mode_group)
        
        # 4. Options
        options_group = QGroupBox("🔧 Tùy chọn")
        options_layout = QVBoxLayout(options_group)
        
        self.chk_copy_mode = QCheckBox("Không re-encode (nhanh hơn)")
        self.chk_copy_mode.setChecked(True)
        options_layout.addWidget(self.chk_copy_mode)
        
        self.chk_quality = QCheckBox("Chất lượng cao (CRF 18)")
        self.chk_quality.setChecked(True)
        options_layout.addWidget(self.chk_quality)
        
        self.chk_log = QCheckBox("Ghi log")
        self.chk_log.setChecked(True)
        options_layout.addWidget(self.chk_log)
        
        self.chk_open_folder = QCheckBox("Tự mở thư mục sau khi hoàn thành")
        self.chk_open_folder.setChecked(True)
        options_layout.addWidget(self.chk_open_folder)
        
        layout.addWidget(options_group)
        
        # 5. Start button
        btn_start = QPushButton("▶ Bắt đầu chia")
        btn_start.setObjectName("primaryButton")
        btn_start.setMinimumHeight(50)
        btn_start.clicked.connect(self.start_splitting)
        layout.addWidget(btn_start)
        
        # 6. Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.lbl_progress = QLabel("")
        self.lbl_progress.setVisible(False)
        layout.addWidget(self.lbl_progress)
        
        # 7. Log
        log_group = QGroupBox("📋 Nhật ký")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QPlainTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        self.log_text.setStyleSheet("font-family: 'Consolas', monospace; font-size: 10px;")
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_group)
        
        # Add stretch at the end
        layout.addStretch()
        
        return panel
    
    def create_preview_panel(self):
        """Create preview panel with video player and clips list"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        
        # Video player
        player_group = QGroupBox("🎬 Xem trước")
        player_layout = QVBoxLayout(player_group)
        
        self.video_player = VideoPlayer()
        player_layout.addWidget(self.video_player)
        
        layout.addWidget(player_group)
        
        # Clips list
        clips_group = QGroupBox("📋 Danh sách clip")
        clips_layout = QVBoxLayout(clips_group)
        
        # Toolbar
        toolbar = QHBoxLayout()
        btn_refresh = QPushButton("🔄 Làm mới")
        btn_refresh.clicked.connect(self.refresh_clips)
        toolbar.addWidget(btn_refresh)
        
        btn_clear = QPushButton("🗑️ Xóa tất cả")
        btn_clear.clicked.connect(self.clear_clips)
        toolbar.addWidget(btn_clear)
        toolbar.addStretch()
        clips_layout.addLayout(toolbar)
        
        # Clips table
        self.clips_table = QTableWidget()
        self.clips_table.setColumnCount(4)
        self.clips_table.setHorizontalHeaderLabels(["Tên clip", "Thời lượng", "Dung lượng", "Ngày tạo"])
        self.clips_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.clips_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.clips_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.clips_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.clips_table.setAlternatingRowColors(True)
        self.clips_table.itemDoubleClicked.connect(self.on_clip_double_click)
        clips_layout.addWidget(self.clips_table)
        
        layout.addWidget(clips_group)
        
        return panel
    
    def select_video(self):
        """Mở dialog chọn video"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn video",
            "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm);;All Files (*.*)"
        )
        
        if file_path:
            self.load_video(file_path)
    
    def load_video(self, file_path):
        """Load video và hiển thị thông tin"""
        self.current_video = file_path
        
        # Lấy thông tin video
        video_info = VideoInfo(file_path)
        if video_info.load_info():
            # Hiển thị thông tin
            info = video_info.to_dict()
            info_text = f"""
            📹 {Path(file_path).name}
            ⏱️ Thời lượng: {info['duration_str']}
            📐 Độ phân giải: {info['resolution']}
            🎞️ FPS: {info['fps_str']}
            💾 Dung lượng: {get_file_size(file_path)}
            """
            self.lbl_video_info.setText(info_text.strip())
            
            # Load vào player
            self.video_player.load_video(file_path)
            
            # Tự động đặt thư mục xuất
            output_dir = os.path.join(
                os.path.dirname(file_path),
                "split_output"
            )
            self.lbl_output_dir.setText(output_dir)
            
            self.add_log(f"Đã tải video: {Path(file_path).name}")
        else:
            QMessageBox.warning(self, "Lỗi", "Không thể đọc thông tin video")
    
    def select_output_dir(self):
        """Chọn thư mục xuất"""
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Chọn thư mục lưu"
        )
        
        if dir_path:
            self.lbl_output_dir.setText(dir_path)
    
    def on_mode_changed(self, index):
        """Xử lý thay đổi chế độ chia"""
        if index == 0:  # Theo thời lượng
            self.spin_duration.setVisible(True)
            self.spin_count.setVisible(False)
        else:  # Theo số clip
            self.spin_duration.setVisible(False)
            self.spin_count.setVisible(True)
    
    def start_splitting(self):
        """Bắt đầu quá trình chia video"""
        # Kiểm tra đầu vào
        if not self.current_video:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn video")
            return
        
        output_dir = self.lbl_output_dir.text()
        if not output_dir:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn thư mục lưu")
            return
        
        # Lấy thông số
        mode = 'duration' if self.combo_mode.currentIndex() == 0 else 'count'
        duration = self.spin_duration.value() if mode == 'duration' else 30
        count = self.spin_count.value() if mode == 'count' else 10
        copy_mode = self.chk_copy_mode.isChecked()
        quality = 18 if self.chk_quality.isChecked() else 23
        
        # Disable controls
        self.set_controls_enabled(False)
        
        # Reset progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.lbl_progress.setVisible(True)
        self.lbl_progress.setText("Đang chuẩn bị...")
        
        # Clear log
        if not self.chk_log.isChecked():
            self.log_text.clear()
        
        self.add_log("=" * 50)
        self.add_log("Bắt đầu chia video")
        self.add_log(f"Video: {Path(self.current_video).name}")
        self.add_log(f"Thư mục xuất: {output_dir}")
        self.add_log(f"Chế độ: {'Theo thời lượng' if mode == 'duration' else 'Theo số clip'}")
        
        # Tạo worker thread
        self.worker = SplitWorker(
            self.splitter,
            self.current_video,
            output_dir,
            mode,
            duration,
            count,
            copy_mode,
            quality
        )
        
        # Connect signals
        self.worker.progress.connect(self.update_progress)
        self.worker.log.connect(self.add_log)
        self.worker.finished.connect(self.on_split_finished)
        self.worker.error.connect(self.on_split_error)
        
        # Start
        self.worker.start()
    
    def update_progress(self, current, total):
        """Cập nhật tiến trình"""
        self.progress_bar.setValue(current)
        self.lbl_progress.setText(f"Đang xử lý clip: {current} / {total}")
    
    def add_log(self, message):
        """Thêm log vào text area"""
        if not self.chk_log.isChecked():
            return
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.appendPlainText(f"[{timestamp}] {message}")
        
        # Auto scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def on_split_finished(self, clips):
        """Xử lý khi chia video hoàn thành"""
        self.clips = clips
        
        self.add_log(f"Hoàn thành! Đã tạo {len(clips)} clip")
        self.add_log("=" * 50)
        
        # Refresh clips list
        self.refresh_clips()
        
        # Enable controls
        self.set_controls_enabled(True)
        
        # Hide progress
        self.progress_bar.setVisible(False)
        self.lbl_progress.setVisible(False)
        
        # Show completion message
        QMessageBox.information(
            self,
            "Hoàn thành",
            f"Đã chia video thành {len(clips)} clip thành công!"
        )
        
        # Mở thư mục
        if self.chk_open_folder.isChecked() and self.lbl_output_dir.text():
            output_dir = self.lbl_output_dir.text()
            if os.path.exists(output_dir):
                os.startfile(output_dir)
    
    def on_split_error(self, error_msg):
        """Xử lý lỗi khi chia video"""
        self.add_log(f"LỖI: {error_msg}")
        self.add_log("=" * 50)
        
        # Enable controls
        self.set_controls_enabled(True)
        
        # Hide progress
        self.progress_bar.setVisible(False)
        self.lbl_progress.setVisible(False)
        
        # Show error
        QMessageBox.critical(
            self,
            "Lỗi",
            f"Đã xảy ra lỗi khi chia video:\n\n{error_msg}"
        )
    
    def set_controls_enabled(self, enabled):
        """Bật/tắt các control"""
        # Tìm tất cả các widget và set enabled
        for widget in self.findChildren(QWidget):
            if widget not in [self.progress_bar, self.lbl_progress, self.log_text]:
                widget.setEnabled(enabled)
    
    def refresh_clips(self):
        """Làm mới danh sách clip"""
        self.clips_table.setRowCount(len(self.clips))
        
        for i, clip in enumerate(self.clips):
            # Tên
            name_item = QTableWidgetItem(Path(clip['path']).name)
            self.clips_table.setItem(i, 0, name_item)
            
            # Thời lượng
            duration_item = QTableWidgetItem(clip.get('duration_str', 'N/A'))
            self.clips_table.setItem(i, 1, duration_item)
            
            # Dung lượng
            size = clip.get('size', '0')
            size_str = get_file_size(clip['path']) if clip.get('path') else 'N/A'
            size_item = QTableWidgetItem(size_str)
            self.clips_table.setItem(i, 2, size_item)
            
            # Ngày tạo
            if os.path.exists(clip['path']):
                import datetime
                mtime = os.path.getmtime(clip['path'])
                date_str = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
                date_item = QTableWidgetItem(date_str)
                self.clips_table.setItem(i, 3, date_item)
            else:
                date_item = QTableWidgetItem('N/A')
                self.clips_table.setItem(i, 3, date_item)
    
    def clear_clips(self):
        """Xóa tất cả clip khỏi danh sách"""
        self.clips = []
        self.refresh_clips()
        self.add_log("Đã xóa danh sách clip")
    
    def on_clip_double_click(self, item):
        """Xử lý double click vào clip để phát"""
        row = item.row()
        if row < len(self.clips):
            clip_path = self.clips[row]['path']
            if os.path.exists(clip_path):
                self.video_player.load_video(clip_path)
                self.video_player.play()
            else:
                QMessageBox.warning(self, "Lỗi", "Không tìm thấy file clip")
