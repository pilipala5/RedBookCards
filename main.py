# main.py
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from src.ui.main_window import MainWindow

def main():
    # 启用高DPI支持
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 使用 Fusion 风格
    
    # 设置应用程序样式
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f7;
        }
    """)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()