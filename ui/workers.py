"""
Background workers to keep the UI responsive during heavy processing.
"""
import tempfile
from PySide6.QtCore import QThread, Signal

# Importando do nosso core isolado
from core.downloader import AudioDownloader
from core.transcriber import AudioTranscriber

class TranscribeWorker(QThread):
    finished = Signal(dict)
    status_update = Signal(str)
    progress_update = Signal(int)
    partial_text_update = Signal(str)
    error = Signal(str)

    def __init__(self, input_source: str, is_url: bool, model_type: str, language_code: str, compute_device: str):
        super().__init__()
        self.input_source = input_source
        self.is_url = is_url
        self.model_type = model_type
        self.language_code = language_code
        self.compute_device = compute_device
        self._is_cancelled = False

    def cancel(self) -> None:
        self._is_cancelled = True

    def run(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                target_path = self.input_source
                
                # Delega o download para a classe especialista
                if self.is_url:
                    self.status_update.emit("Downloading audio from link...")
                    target_path = AudioDownloader.download_from_youtube(self.input_source, temp_dir)

                self.status_update.emit(f"Initializing AI Engine...")
                
                # Instancia o motor de IA
                transcriber = AudioTranscriber(self.model_type, self.compute_device)
                
                self.status_update.emit(f"Transcribing ({self.language_code.upper()})...")
                
                full_text = ""
                segments_list = []
                
                # Consome o Generator yieldando resultados em tempo real
                for text, start, end, duration in transcriber.transcribe(target_path, self.language_code):
                    if self._is_cancelled:
                        self.status_update.emit("Process cancelled.")
                        self.error.emit("Transcription aborted by user.")
                        return

                    full_text += text
                    segments_list.append({
                        "start": start,
                        "end": end,
                        "text": text
                    })
                    
                    self.partial_text_update.emit(text)

                    if duration > 0:
                        percent = min(100, int((end / duration) * 100))
                        self.progress_update.emit(percent)

                result = {"text": full_text, "segments": segments_list}
                self.progress_update.emit(100)
                self.status_update.emit("Transcription finished successfully!")
                self.finished.emit(result)

            except Exception as e:
                self.error.emit(f"Critical Error: {str(e)}")