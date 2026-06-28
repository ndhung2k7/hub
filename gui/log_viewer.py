"""
Log viewer widget
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from datetime import datetime


class LogViewer(QWidget):
    """Widget for viewing logs"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        self.btn_clear = QPushButton("🗑️ Xóa log")
        self.btn_clear.clicked.connect(self.clear)
        toolbar.addWidget(self.btn_clear)
        
        self.btn_copy = QPushButton("📋 Copy")
        self.btn_copy.clicked.connect(self.copy)
        toolbar.addWidget(self.btn_copy)
        
        toolbar.addStretch()
        
        self.lbl_count = QLabel("0 dòng")
        toolbar.addWidget(self.lbl_count)
        
        layout.addLayout(toolbar)
        
        # Log text area
        self.text_area = QPlainTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("font-family: 'Consolas', monospace; font-size: 10px;")
        layout.addWidget(self.text_area)
    
    def log(self, message):
        """Thêm log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.text_area.appendPlainText(f"[{timestamp}] {message}")
        self.update_count()
        
        # Auto scroll to bottom
        scrollbar = self.text_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear(self):
        """Xóa log"""
        self.text_area.clear()
        self.update_count()
    
    def copy(self):
        """Copy log content"""
        content = self.text_area.toPlainText()
        clipboard = self.text_area.clipboard()
        if clipboard:
            clipboard.setText(content)
    
    def update_count(self):
        """Cập nhật số dòng"""
        lines = self.text_area.toPlainText().count('\n')
        self.lbl_count.setText(f"{lines} dòng")
