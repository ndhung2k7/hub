"""
Clip list widget for displaying and managing clips
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView, QLabel,
    QMenu, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from pathlib import Path
import os


class ClipListWidget(QWidget):
    """Widget for displaying list of clips"""
    
    clip_selected = Signal(str)  # Emitted when clip is selected
    clip_removed = Signal(str)   # Emitted when clip is removed
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clips = []
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        self.btn_add = QPushButton("➕ Thêm clip")
        self.btn_add.clicked.connect(self.add_clip)
        toolbar.addWidget(self.btn_add)
        
        self.btn_remove = QPushButton("🗑️ Xóa")
        self.btn_remove.clicked.connect(self.remove_selected)
        toolbar.addWidget(self.btn_remove)
        
        self.btn_remove_all = QPushButton("🗑️ Xóa tất cả")
        self.btn_remove_all.clicked.connect(self.remove_all)
        toolbar.addWidget(self.btn_remove_all)
        
        toolbar.addStretch()
        
        self.lbl_count = QLabel("0 clip")
        toolbar.addWidget(self.lbl_count)
        
        layout.addLayout(toolbar)
        
        # Clips table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["STT", "Tên clip", "Thời lượng", "Dung lượng"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.itemDoubleClicked.connect(self.on_item_double_clicked)
        
        # Context menu
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        
        layout.addWidget(self.table)
    
    def add_clip(self, clip_path=None):
        """Thêm clip vào danh sách"""
        if not clip_path:
            # Mở dialog chọn file
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Chọn clip",
                "",
                "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm);;All Files (*.*)"
            )
            if not file_path:
                return
            clip_path = file_path
        
        # Kiểm tra trùng lặp
        for clip in self.clips:
            if clip['path'] == clip_path:
                QMessageBox.warning(self, "Cảnh báo", "Clip đã tồn tại trong danh sách")
                return
        
        # Lấy thông tin clip
        from video.video_info import VideoInfo
        from utils.file_utils import get_file_size
        
        video_info = VideoInfo(clip_path)
        if not video_info.load_info():
            QMessageBox.warning(self, "Lỗi", "Không thể đọc thông tin clip")
            return
        
        # Thêm vào danh sách
        clip_data = {
            'path': clip_path,
            'name': Path(clip_path).name,
            'duration': video_info.duration,
            'duration_str': video_info.get_duration_str(),
            'size': get_file_size(clip_path)
        }
        
        self.clips.append(clip_data)
        self.refresh_table()
    
    def refresh_table(self):
        """Làm mới bảng hiển thị"""
        self.table.setRowCount(len(self.clips))
        
        for i, clip in enumerate(self.clips):
            # STT
            stt_item = QTableWidgetItem(str(i + 1))
            stt_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 0, stt_item)
            
            # Tên
            name_item = QTableWidgetItem(clip['name'])
            self.table.setItem(i, 1, name_item)
            
            # Thời lượng
            duration_item = QTableWidgetItem(clip['duration_str'])
            duration_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 2, duration_item)
            
            # Dung lượng
            size_item = QTableWidgetItem(clip['size'])
            size_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 3, size_item)
        
        # Cập nhật số lượng
        self.lbl_count.setText(f"{len(self.clips)} clip")
    
    def remove_selected(self):
        """Xóa clip được chọn"""
        selected_rows = set()
        for item in self.table.selectedItems():
            selected_rows.add(item.row())
        
        if not selected_rows:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn clip cần xóa")
            return
        
        # Xóa từ cuối lên để không ảnh hưởng index
        for row in sorted(selected_rows, reverse=True):
            if row < len(self.clips):
                clip_path = self.clips[row]['path']
                self.clips.pop(row)
                self.clip_removed.emit(clip_path)
        
        self.refresh_table()
    
    def remove_all(self):
        """Xóa tất cả clip"""
        if not self.clips:
            return
        
        reply = QMessageBox.question(
            self,
            "Xác nhận",
            "Bạn có chắc muốn xóa tất cả clip?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.clips.clear()
            self.refresh_table()
    
    def on_item_double_clicked(self, item):
        """Xử lý double click vào clip"""
        row = item.row()
        if row < len(self.clips):
            clip_path = self.clips[row]['path']
            if os.path.exists(clip_path):
                self.clip_selected.emit(clip_path)
            else:
                QMessageBox.warning(self, "Lỗi", "Không tìm thấy file clip")
    
    def show_context_menu(self, position):
        """Hiển thị context menu"""
        menu = QMenu()
        
        action_play = menu.addAction("▶ Phát")
        action_remove = menu.addAction("🗑️ Xóa")
        menu.addSeparator()
        action_remove_all = menu.addAction("🗑️ Xóa tất cả")
        
        action = menu.exec(self.table.viewport().mapToGlobal(position))
        
        if action == action_play:
            self.on_item_double_clicked(self.table.currentItem())
        elif action == action_remove:
            self.remove_selected()
        elif action == action_remove_all:
            self.remove_all()
    
    def get_clips(self):
        """Lấy danh sách clip"""
        return self.clips
    
    def clear(self):
        """Xóa tất cả clip"""
        self.clips.clear()
        self.refresh_table()
