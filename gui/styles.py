"""
Stylesheet cho ứng dụng - Dark Mode hiện đại
"""

DARK_STYLE = """
QMainWindow {
    background-color: #1a1a1a;
}

QWidget {
    background-color: #1e1e1e;
    color: #ffffff;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 12px;
}

QLabel {
    color: #e0e0e0;
    background-color: transparent;
}

QGroupBox {
    background-color: #242424;
    border: 1px solid #3a3a3a;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 8px;
    font-weight: bold;
    color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 8px;
    background-color: #242424;
}

QPushButton {
    background-color: #2d2d2d;
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    padding: 8px 16px;
    color: #ffffff;
    font-weight: 500;
    min-height: 20px;
}

QPushButton:hover {
    background-color: #3a3a3a;
    border-color: #4a4a4a;
}

QPushButton:pressed {
    background-color: #252525;
}

QPushButton:disabled {
    background-color: #1a1a1a;
    color: #666666;
}

QPushButton#primaryButton {
    background-color: #0078d4;
    border-color: #0078d4;
}

QPushButton#primaryButton:hover {
    background-color: #1084d8;
}

QPushButton#primaryButton:pressed {
    background-color: #006cbc;
}

QPushButton#successButton {
    background-color: #107c10;
    border-color: #107c10;
}

QPushButton#successButton:hover {
    background-color: #189018;
}

QPushButton#dangerButton {
    background-color: #c42b1c;
    border-color: #c42b1c;
}

QPushButton#dangerButton:hover {
    background-color: #d63a2a;
}

QLineEdit, QSpinBox, QComboBox {
    background-color: #2d2d2d;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    padding: 6px 8px;
    color: #ffffff;
}

QLineEdit:focus, QSpinBox:focus, QComboBox:focus {
    border-color: #0078d4;
}

QComboBox::drop-down {
    border: none;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #888888;
    margin-right: 8px;
}

QComboBox QAbstractItemView {
    background-color: #2d2d2d;
    border: 1px solid #3a3a3a;
    selection-background-color: #0078d4;
}

QProgressBar {
    background-color: #2d2d2d;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    height: 20px;
    text-align: center;
    color: #ffffff;
}

QProgressBar::chunk {
    background-color: #0078d4;
    border-radius: 3px;
}

QTableWidget {
    background-color: #1e1e1e;
    alternate-background-color: #252525;
    gridline-color: #2d2d2d;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
}

QTableWidget::item {
    padding: 6px;
}

QHeaderView::section {
    background-color: #2d2d2d;
    padding: 8px;
    border: none;
    border-right: 1px solid #3a3a3a;
    border-bottom: 1px solid #3a3a3a;
    font-weight: bold;
    color: #e0e0e0;
}

QScrollBar:vertical {
    background-color: #1e1e1e;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #3a3a3a;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #4a4a4a;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}

QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    background-color: #2d2d2d;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
}

QCheckBox::indicator:checked {
    background-color: #0078d4;
    border-color: #0078d4;
}

QTabWidget::pane {
    background-color: #1e1e1e;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #2d2d2d;
    padding: 8px 16px;
    border: 1px solid #3a3a3a;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #3a3a3a;
    border-bottom: 2px solid #0078d4;
}

QTabBar::tab:hover {
    background-color: #3a3a3a;
}

QPlainTextEdit {
    background-color: #1a1a1a;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    color: #e0e0e0;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 11px;
}

QToolTip {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #3a3a3a;
    padding: 4px 8px;
    border-radius: 4px;
}
"""

PLAYER_STYLE = """
QSlider::groove:horizontal {
    background-color: #3a3a3a;
    height: 4px;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background-color: #0078d4;
    width: 14px;
    height: 14px;
    border-radius: 7px;
    margin: -5px 0;
}

QSlider::handle:horizontal:hover {
    background-color: #1084d8;
}

QSlider::sub-page:horizontal {
    background-color: #0078d4;
    border-radius: 2px;
}
"""
