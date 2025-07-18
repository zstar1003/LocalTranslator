"""
主题模块
包含亮色和暗色主题的样式设置
"""

from PyQt6.QtGui import QColor, QPalette


def apply_dark_theme(app):
    """应用深色主题样式"""
    app.setStyle("Fusion")

    # 创建深色调色板
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))

    # 应用调色板
    app.setPalette(dark_palette)

    # 设置样式表
    app.setStyleSheet("""
        QGroupBox {
            border: 1px solid #3A3A3A;
            border-radius: 8px;
            margin-top: 12px;
            font-weight: bold;
            font-size: 14px;
            background-color: #2D2D2D;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            color: #2A82DA;
        }
        QPushButton {
            background-color: #2A82DA;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #3A92EA;
        }
        QPushButton:pressed {
            background-color: #1A72CA;
        }
        QPushButton:disabled {
            background-color: #555555;
        }
        /* 主题切换按钮特殊样式 */
        QPushButton#themeButton {
            background-color: transparent;
            border: 1px solid #3A3A3A;
            border-radius: 15px;
            padding: 0px;
            font-size: 16px;
        }
        QPushButton#themeButton:hover {
            background-color: rgba(42, 130, 218, 0.2);
        }
        QPushButton#themeButton:pressed {
            background-color: rgba(42, 130, 218, 0.3);
        }
        /* 复制按钮特殊样式 */
        QToolButton#copyButton {
            background-color: transparent;
            border: 1px solid #3A3A3A;
            border-radius: 14px;
            padding: 0px;
            font-size: 16px;
            color: #DDDDDD;
        }
        QToolButton#copyButton:hover {
            background-color: rgba(42, 130, 218, 0.2);
        }
        QToolButton#copyButton:pressed {
            background-color: rgba(42, 130, 218, 0.3);
        }
        QTextEdit {
            border: 1px solid #3A3A3A;
            border-radius: 6px;
            padding: 8px;
            background-color: #2D2D2D;
            color: #FFFFFF;
            selection-background-color: #2A82DA;
        }
        QComboBox {
            border: 1px solid #3A3A3A;
            border-radius: 6px;
            padding: 6px;
            background-color: #2D2D2D;
            min-height: 24px;
            color: #FFFFFF;
        }
        QComboBox::drop-down {
            border: none;
            width: 24px;
        }
        QComboBox QAbstractItemView {
            background-color: #2D2D2D;
            color: #FFFFFF;
            selection-background-color: #2A82DA;
            selection-color: #FFFFFF;
            border: 1px solid #3A3A3A;
        }
        QComboBox QAbstractItemView::item:hover {
            background-color: #3A3A3A;
            color: #FFFFFF;
        }
        QLabel {
            color: #DDDDDD;
        }
        QProgressBar {
            border: 1px solid #3A3A3A;
            border-radius: 6px;
            text-align: center;
            height: 20px;
            background-color: #222222;
            color: white;
        }
        QProgressBar::chunk {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1A72CA, stop:1 #3A92EA);
            border-radius: 5px;
        }
        QStatusBar {
            background-color: #222222;
            color: #DDDDDD;
        }
    """)


def apply_light_theme(app):
    """应用明亮主题样式"""
    app.setStyle("Fusion")

    # 创建明亮调色板
    light_palette = QPalette()
    light_palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    light_palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    light_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(233, 233, 233))
    light_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    light_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    light_palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.Link, QColor(0, 102, 204))
    light_palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
    light_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

    # 应用调色板
    app.setPalette(light_palette)

    # 设置样式表
    app.setStyleSheet("""
        QGroupBox {
            border: 1px solid #CCCCCC;
            border-radius: 8px;
            margin-top: 12px;
            font-weight: bold;
            font-size: 14px;
            background-color: #F5F5F5;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            color: #0078D7;
        }
        QPushButton {
            background-color: #0078D7;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #1C84DC;
        }
        QPushButton:pressed {
            background-color: #0067C0;
        }
        QPushButton:disabled {
            background-color: #CCCCCC;
        }
        /* 主题切换按钮特殊样式 */
        QPushButton#themeButton {
            background-color: transparent;
            border: 1px solid #CCCCCC;
            border-radius: 15px;
            padding: 0px;
            font-size: 16px;
            color: #333333;
        }
        QPushButton#themeButton:hover {
            background-color: rgba(0, 120, 215, 0.1);
        }
        QPushButton#themeButton:pressed {
            background-color: rgba(0, 120, 215, 0.2);
        }
        /* 复制按钮特殊样式 */
        QToolButton#copyButton {
            background-color: transparent;
            border: 1px solid #CCCCCC;
            border-radius: 14px;
            padding: 0px;
            font-size: 16px;
            color: #333333;
        }
        QToolButton#copyButton:hover {
            background-color: rgba(0, 120, 215, 0.1);
        }
        QToolButton#copyButton:pressed {
            background-color: rgba(0, 120, 215, 0.2);
        }
        QTextEdit {
            border: 1px solid #CCCCCC;
            border-radius: 6px;
            padding: 8px;
            background-color: white;
            color: black;
            selection-background-color: #0078D7;
        }
        QComboBox {
            border: 1px solid #CCCCCC;
            border-radius: 6px;
            padding: 6px;
            background-color: white;
            min-height: 24px;
            color: #333333;
        }
        QComboBox::drop-down {
            border: none;
            width: 24px;
        }
        QComboBox QAbstractItemView {
            background-color: white;
            color: #333333;
            selection-background-color: #0078D7;
            selection-color: white;
            border: 1px solid #CCCCCC;
        }
        QComboBox QAbstractItemView::item:hover {
            background-color: #E5F1FB;
            color: #333333;
        }
        QLabel {
            color: #333333;
        }
        QProgressBar {
            border: 1px solid #CCCCCC;
            border-radius: 6px;
            text-align: center;
            height: 20px;
            background-color: #F0F0F0;
            color: black;
        }
        QProgressBar::chunk {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0067C0, stop:1 #1C84DC);
            border-radius: 5px;
        }
        QStatusBar {
            background-color: #F0F0F0;
            color: #333333;
        }
    """)
