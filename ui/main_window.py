"""
Main application window and UI orchestrator.
"""
import os
import time
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, 
                             QComboBox, QGroupBox, QFileDialog, QLineEdit,
                             QTextEdit, QProgressBar, QMessageBox)
from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QGuiApplication, QIcon

# Importing our modularized components
from ui.styles import MAIN_STYLESHEET
from ui.workers import TranscribeWorker
from utils.constants import (SUPPORTED_LANGUAGES, WHISPER_MODELS, 
                             COMPUTE_DEVICES, EXPORT_FORMATS, ICON_PATH)
from utils.export import Exporter

class TranscriberApp(QMainWindow):
    """Main GUI class handling user interactions and visual state."""
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(550, 850)
        
        # Ensures the icon is loaded correctly dynamically
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))
            
        self._old_pos = None
        self.selected_file = None
        self.last_result = None
        self.worker = None
        
        self.setAcceptDrops(True)
        
        # Setup UI framework
        self.main_container = QWidget()
        self.main_container.setObjectName("MainContainer")
        self.setCentralWidget(self.main_container)
        
        self.base_layout = QVBoxLayout(self.main_container)
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.base_layout.setSpacing(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer_display)
        self.elapsed_seconds = 0

        self.setup_title_bar()
        self.setup_content()
        
        # Apply extracted QSS
        self.setStyleSheet(MAIN_STYLESHEET)

    def setup_title_bar(self):
        self.title_bar = QWidget()
        self.title_bar.setObjectName("TitleBar")
        t_layout = QHBoxLayout(self.title_bar)
        t_layout.setContentsMargins(0, 0, 10, 0)
        self.title_label = QLabel("Professional Transcriber | Lucas de Almeida")
        self.title_label.setObjectName("TitleLabel")
        self.btn_min = QPushButton("\uE921"); self.btn_min.setObjectName("MinBtn"); self.btn_min.setFixedSize(35, 30); self.btn_min.clicked.connect(self.showMinimized)
        self.btn_close = QPushButton("\uE8BB"); self.btn_close.setObjectName("CloseBtn"); self.btn_close.setFixedSize(35, 30); self.btn_close.clicked.connect(self.close)
        t_layout.addWidget(self.title_label); t_layout.addStretch(); t_layout.addWidget(self.btn_min); t_layout.addWidget(self.btn_close)
        self.base_layout.addWidget(self.title_bar)

    def setup_content(self):
        content = QVBoxLayout()
        content.setContentsMargins(20, 10, 20, 20)
        content.setSpacing(10)

        # File Input Group
        file_grp = QGroupBox("Input Media (Drag & Drop a file or paste a link)")
        fg_layout = QVBoxLayout(file_grp)
        self.btn_select = QPushButton("Select Local File")
        self.btn_select.setObjectName("Secondary")
        self.btn_select.clicked.connect(self.select_file)
        self.lbl_file = QLabel("No file selected (Drag and drop here)")
        self.lbl_file.setStyleSheet("color: #707070;")
        fg_layout.addWidget(self.btn_select)
        fg_layout.addWidget(self.lbl_file)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Or paste a video URL (YouTube, etc.)")
        fg_layout.addWidget(self.url_input)
        content.addWidget(file_grp)

        # Settings Group using dynamically imported Constants
        set_grp = QGroupBox("Settings")
        sg_layout = QVBoxLayout(set_grp)
        row1 = QHBoxLayout()
        self.combo_model = QComboBox(); self.combo_model.addItems(WHISPER_MODELS)
        self.combo_lang = QComboBox(); self.combo_lang.addItems(list(SUPPORTED_LANGUAGES.keys()))
        row1.addWidget(QLabel("Model:")); row1.addWidget(self.combo_model)
        row1.addWidget(QLabel("Language:")); row1.addWidget(self.combo_lang)
        sg_layout.addLayout(row1)
        
        row2 = QHBoxLayout()
        self.combo_device = QComboBox(); self.combo_device.addItems(COMPUTE_DEVICES)
        self.combo_format = QComboBox(); self.combo_format.addItems(EXPORT_FORMATS)
        row2.addWidget(QLabel("Hardware:")); row2.addWidget(self.combo_device)
        row2.addWidget(QLabel("Export Format:")); row2.addWidget(self.combo_format)
        sg_layout.addLayout(row2)
        content.addWidget(set_grp)

        # Control Buttons
        ctrl_layout = QHBoxLayout()
        self.btn_start = QPushButton("Start Transcription")
        self.btn_start.clicked.connect(self.start_process)
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setObjectName("BtnCancel")
        self.btn_cancel.clicked.connect(self.cancel_process)
        self.btn_cancel.hide()
        ctrl_layout.addWidget(self.btn_start)
        ctrl_layout.addWidget(self.btn_cancel)
        content.addLayout(ctrl_layout)

        # Progress and Timer
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        content.addWidget(self.progress_bar)

        self.lbl_timer = QLabel("Elapsed Time: 00:00:00")
        self.lbl_timer.setAlignment(Qt.AlignCenter)
        self.lbl_timer.setStyleSheet("font-weight: bold; color: #348DC5;")
        content.addWidget(self.lbl_timer)

        self.lbl_status = QLabel("Status: Waiting...")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        content.addWidget(self.lbl_status)

        # Live Text Area
        self.live_text = QTextEdit()
        self.live_text.setReadOnly(True)
        self.live_text.setPlaceholderText("Transcription will appear here in real-time...")
        content.addWidget(self.live_text)

        # Final Actions
        self.actions_widget = QWidget()
        actions_layout = QHBoxLayout(self.actions_widget)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        self.btn_copy = QPushButton("Copy Text")
        self.btn_copy.clicked.connect(self.copy_to_clipboard)
        self.btn_save = QPushButton("Save File")
        self.btn_save.clicked.connect(self.save_file)
        actions_layout.addWidget(self.btn_copy)
        actions_layout.addWidget(self.btn_save)
        self.actions_widget.hide()
        content.addWidget(self.actions_widget)

        self.base_layout.addLayout(content)

    # --- DRAG AND DROP ---
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls and urls[0].isLocalFile():
            path = urls[0].toLocalFile()
            self.selected_file = path
            self.lbl_file.setText(os.path.basename(path))
            self.url_input.clear()

    # --- WINDOW MOVEMENT ---
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton: self._old_pos = e.globalPos()
    def mouseMoveEvent(self, e):
        if self._old_pos:
            delta = QPoint(e.globalPos() - self._old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._old_pos = e.globalPos()
    def mouseReleaseEvent(self, e): self._old_pos = None

    # --- CORE UI LOGIC ---
    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Media", "", "Media Files (*.mp4 *.mp3 *.m4a *.wav *.mkv *.ogg)")
        if path:
            self.selected_file = path
            self.lbl_file.setText(os.path.basename(path))
            self.url_input.clear()

    def toggle_ui(self, is_processing):
        self.btn_select.setEnabled(not is_processing)
        self.url_input.setEnabled(not is_processing)
        self.combo_model.setEnabled(not is_processing)
        self.combo_lang.setEnabled(not is_processing)
        self.combo_device.setEnabled(not is_processing)
        
        if is_processing:
            self.btn_start.hide()
            self.btn_cancel.show()
            self.actions_widget.hide()
            self.progress_bar.setValue(0)
            self.live_text.clear()
        else:
            self.btn_start.show()
            self.btn_cancel.hide()

    def update_timer_display(self):
        self.elapsed_seconds += 1
        td = time.gmtime(self.elapsed_seconds)
        time_str = time.strftime('%H:%M:%S', td)
        self.lbl_timer.setText(f"Elapsed Time: {time_str}")

    def start_process(self):
        url = self.url_input.text().strip()
        is_url = bool(url)
        input_source = url if is_url else self.selected_file

        if not input_source:
            QMessageBox.warning(self, "Warning", "Please select a file or paste a URL.")
            return
        
        self.toggle_ui(is_processing=True)
        
        self.elapsed_seconds = 0
        self.lbl_timer.setText("Elapsed Time: 00:00:00")
        self.timer.start(1000)
        
        lang_code = SUPPORTED_LANGUAGES.get(self.combo_lang.currentText(), "en")
        device_code = self.combo_device.currentText().lower().split()[0]
        
        self.worker = TranscribeWorker(input_source, is_url, self.combo_model.currentText(), lang_code, device_code)
        
        self.worker.status_update.connect(self.update_status)
        self.worker.progress_update.connect(self.progress_bar.setValue)
        self.worker.partial_text_update.connect(self.append_live_text)
        self.worker.finished.connect(self.process_finished)
        self.worker.error.connect(self.process_error)
        
        self.worker.start()

    def cancel_process(self):
        if self.worker and self.worker.isRunning():
            self.update_status("Cancelling process... Please wait.")
            self.btn_cancel.setEnabled(False)
            self.worker.cancel()
            self.timer.stop()

    def update_status(self, msg):
        self.lbl_status.setText(f"Status: {msg}")

    def append_live_text(self, text):
        self.live_text.insertPlainText(text + " ")
        self.live_text.verticalScrollBar().setValue(self.live_text.verticalScrollBar().maximum())

    def process_finished(self, result):
        self.timer.stop()
        self.last_result = result
        self.update_status("Completed! What do you want to do with the text?")
        self.toggle_ui(is_processing=False)
        self.btn_cancel.setEnabled(True)
        self.actions_widget.show()

    def process_error(self, err):
        self.timer.stop()
        self.update_status(f"Error: {err}")
        self.toggle_ui(is_processing=False)
        self.btn_cancel.setEnabled(True)

    # --- DELEGATED ACTIONS ---
    def copy_to_clipboard(self):
        if self.last_result:
            clipboard = QGuiApplication.clipboard()
            clipboard.setText(self.last_result["text"].strip())
            self.update_status("Text copied to clipboard!")

    def save_file(self):
        if not self.last_result: return
        
        ext = self.combo_format.currentText()
        default_name = "transcription" + ext
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Transcription", default_name, f"Files (*{ext})")
        
        if save_path:
            try:
                # Delega a lógica de salvar para a classe utilitária Exporter
                Exporter.save(self.last_result, save_path, ext)
                self.update_status(f"Successfully saved: {os.path.basename(save_path)}")
            except Exception as e:
                QMessageBox.critical(self, "Save Error", str(e))