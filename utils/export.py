"""
Handles formatting and exporting of transcription results.
"""
import json
import time
from typing import Dict, Any

try:
    from docx import Document
except ImportError:
    Document = None

class Exporter:
    """Utility class for exporting transcription data to various formats."""
    
    @staticmethod
    def format_timestamp(seconds: float) -> str:
        """Converts seconds into SRT timestamp format."""
        td = time.gmtime(seconds)
        ms = int((seconds % 1) * 1000)
        return f"{time.strftime('%H:%M:%S', td)},{ms:03d}"

    @classmethod
    def save(cls, result: Dict[str, Any], file_path: str, ext: str) -> None:
        """
        Saves the transcription result to the specified file format.
        """
        if ext == ".txt":
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(result["text"])
                
        elif ext == ".json":
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4)
                
        elif ext == ".docx" and Document:
            doc = Document()
            doc.add_heading('Transcription | Lucas de Almeida', 0)
            doc.add_paragraph(result["text"])
            doc.save(file_path)
            
        elif ext == ".srt":
            with open(file_path, "w", encoding="utf-8") as f:
                for i, seg in enumerate(result["segments"]):
                    start = cls.format_timestamp(seg["start"])
                    end = cls.format_timestamp(seg["end"])
                    f.write(f"{i+1}\n{start} --> {end}\n{seg['text'].strip()}\n\n")
        else:
            raise ValueError(f"Unsupported format or missing dependencies for {ext}")