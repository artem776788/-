MAIN_WINDOW_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}

QPushButton {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 12px;
}

QPushButton:hover {
    background-color: #45a049;
}

QPushButton:pressed {
    background-color: #3d8b40;
}

QTableWidget {
    background-color: white;
    alternate-background-color: #f9f9f9;
    gridline-color: #ddd;
}

QTableWidget::item {
    padding: 5px;
}

QHeaderView::section {
    background-color: #4CAF50;
    color: white;
    padding: 5px;
    border: none;
}

QLineEdit, QTextEdit, QComboBox {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 5px;
}

QLineEdit:focus, QTextEdit:focus {
    border-color: #4CAF50;
}

QTabWidget::pane {
    border: 1px solid #ddd;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #e0e0e0;
    padding: 8px 16px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #4CAF50;
    color: white;
}

QMessageBox {
    background-color: #f5f5f5;
}
"""

LOGIN_STYLE = """
QDialog {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                      stop:0 #667eea, stop:1 #764ba2);
}

QLineEdit {
    border: 2px solid #ddd;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
    background-color: white;
}

QPushButton {
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #45a049;
}

QLabel {
    color: white;
}
"""