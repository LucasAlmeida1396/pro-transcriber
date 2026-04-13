"""
Core AI module utilizing Faster-Whisper for audio transcription.
"""
import os
from typing import Generator, Tuple, Dict, Any
from faster_whisper import WhisperModel

class TranscriptionInitializationError(Exception):
    """Raised when the AI model fails to load into memory."""
    pass

class AudioTranscriber:
    """Encapsulates the Faster-Whisper model loading and processing logic."""
    
    def __init__(self, model_type: str, compute_device: str):
        self.model_type = model_type
        
        # Hardware Setup & Fallback Logic
        self.device = "cuda" if compute_device in ["auto", "cuda"] else "cpu"
        self.compute_type = "float16" if self.device == "cuda" else "int8"
        
        try:
            self.model = WhisperModel(
                self.model_type, 
                device=self.device, 
                compute_type=self.compute_type
            )
        except Exception as e:
            # Automatic fallback to CPU if CUDA initialization fails under "Auto" mode
            if compute_device == "auto" and self.device == "cuda":
                self.device, self.compute_type = "cpu", "int8"
                self.model = WhisperModel(
                    self.model_type, 
                    device=self.device, 
                    compute_type=self.compute_type
                )
            else:
                raise TranscriptionInitializationError(f"Failed to initialize Whisper model: {e}")

    def transcribe(self, file_path: str, language: str) -> Generator[Tuple[str, float, float, float], None, None]:
        """
        Transcribes audio and yields segments in real-time.
        
        Args:
            file_path (str): Absolute path to the audio file.
            language (str): Language code (e.g., 'en', 'pt').
            
        Yields:
            Tuple containing (segment_text, segment_start, segment_end, total_duration)
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Media file not found at: {file_path}")

        segments, info = self.model.transcribe(file_path, language=language, beam_size=5)
        total_duration = info.duration

        # Generator pattern to stream results back to the caller (Worker/UI)
        for segment in segments:
            yield (segment.text, segment.start, segment.end, total_duration)