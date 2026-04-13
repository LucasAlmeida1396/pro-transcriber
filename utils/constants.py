"""
Constants and Configuration mappings for the ProTranscriber application.
"""
import os
import sys

# Base Directories Configuration
# Dynamically resolves the project root depending on if it's running as a script or a compiled .exe
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
ICON_PATH = os.path.join(ASSETS_DIR, "logo.ico")

# Application Constants
SUPPORTED_LANGUAGES = {
    "Portuguese": "pt", 
    "English": "en", 
    "Spanish": "es",
    "German": "de", 
    "Italian": "it", 
    "French": "fr"
}

WHISPER_MODELS = ["tiny", "base", "small", "medium", "large"]
COMPUTE_DEVICES = ["Auto", "CUDA", "CPU"]
EXPORT_FORMATS = [".txt", ".docx", ".srt", ".json"]
