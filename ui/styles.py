"""
Centralized UI styling configurations (QSS).
"""

MAIN_STYLESHEET = """
    QWidget#MainContainer { background-color: #121421; border: 1px solid #348DC5; border-radius: 10px; }
    QWidget#TitleBar { background-color: #1b1e2e; border-top-left-radius: 10px; border-top-right-radius: 10px; min-height: 45px; }
    QLabel#TitleLabel { color: #F5F5F5; font-weight: bold; font-size: 12px; margin-left: 15px; }
    
    QPushButton#MinBtn, QPushButton#CloseBtn { font-family: 'Segoe MDL2 Assets'; font-size: 10px; border-radius: 4px; border: none; color: #F5F5F5; }
    QPushButton#MinBtn { background-color: transparent; }
    QPushButton#MinBtn:hover { background-color: #2c313c; }
    QPushButton#CloseBtn { background-color: #348DC5; }
    QPushButton#CloseBtn:hover { background-color: #FF6347; }
    
    QLabel { color: #F5F5F5; font-family: 'Segoe UI'; }
    
    QPushButton { background-color: #348DC5; color: #F5F5F5; border-radius: 6px; padding: 10px; font-weight: 600; border: none; }
    QPushButton:hover { background-color: #6A5ACD; }
    QPushButton#BtnCancel { background-color: #FF6347; }
    QPushButton#BtnCancel:hover { background-color: #D2042D; }
    QPushButton#Secondary { background-color: #2c313c; }
    QPushButton#Secondary:hover { background-color: #348DC5; }
    QPushButton:disabled { background-color: #2c313c; color: #707070; }

    QComboBox, QLineEdit { background-color: #1b1e2e; color: #F5F5F5; border: 1px solid #348DC5; border-radius: 5px; padding: 6px; }
    QComboBox QAbstractItemView { background-color: #1b1e2e; color: #F5F5F5; selection-background-color: #348DC5; }
    
    QTextEdit { background-color: #1b1e2e; border: 1px solid #348DC5; border-radius: 8px; color: #F5F5F5; padding: 10px; font-size: 13px; font-family: 'Segoe UI';}
    
    QProgressBar { border: 1px solid #348DC5; border-radius: 4px; text-align: center; background: #1b1e2e; color: white; height: 20px; font-weight: bold; }
    QProgressBar::chunk { background-color: #348DC5; border-radius: 3px; }

    QGroupBox { border: 1px solid #348DC5; border-radius: 8px; margin-top: 12px; color: #348DC5; font-weight: bold; padding-top: 15px; }
    QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; left: 10px; top: 0px; padding: 0 5px; background-color: #121421; }
"""