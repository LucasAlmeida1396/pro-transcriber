<h1 align="center">
  ProTranscriber
</h1>

<p align="center">
  <b>A high-performance, AI-powered desktop transcription tool built with Python and Faster-Whisper.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Framework-PySide6-brightgreen.svg" alt="PySide6">
  <img src="https://img.shields.io/badge/AI_Engine-Faster_Whisper-orange.svg" alt="Faster Whisper">
</p>

## 📌 Overview

ProTranscriber is a robust, modular desktop application designed to transcribe audio and video files locally using state-of-the-art AI models. Built with a strong emphasis on Software Engineering principles, it features a fully decoupled architecture, asynchronous processing, and a highly responsive GUI.

Whether you are dropping a local `.mp4` file or pasting a YouTube link, the application dynamically manages hardware resources to deliver real-time transcription text streams and precise subtitle exports.

## ✨ Key Features

* **Multi-Source Input:** Seamlessly transcribe local media files (Drag & Drop supported) or download and transcribe directly from YouTube URLs via `yt-dlp`.
* **Intelligent Hardware Fallback:** Automatically detects CUDA-enabled GPUs for accelerated processing. If a GPU is unavailable or out of memory, it gracefully falls back to CPU (int8 quantization) without crashing.
* **Real-Time UI Updates:** Utilizes Python Generators (`yield`) and `QThread` to stream transcription text and progress updates to the interface in real-time, preventing UI freezing.
* **Multiple Export Formats:** Export processed transcripts to `.txt`, `.docx`, `.json`, or precisely timestamped `.srt` files.
* **Process Management:** Built-in state machine allowing users to safely abort transcription threads mid-process without leaving orphaned temporary files.

## 🏗️ Architecture & Design Decisions

Coming from a heavy backend background, I structured this desktop application following the **Single Responsibility Principle (SRP)** and clear Separation of Concerns, mimicking a robust MVC/MVT architecture:

* **Decoupled UI & Core:** The user interface (`ui/`) has absolutely zero knowledge of the AI models or download logic. It strictly acts as a View, interacting with the backend (`core/`) exclusively through PyQt Signals and background Workers.
* **Memory-Efficient Data Streaming:** Instead of waiting for a 2-hour audio file to finish transcribing to return a massive data block, the `AudioTranscriber` core yields data segment by segment using Python Generators.
* **Scoped Temporary Environments:** All media downloads and intermediate processing happen within Python's `tempfile` contexts. If the application crashes or the user aborts, the OS automatically cleans up the storage.
* **Centralized Configurations:** UI stylesheets (QSS) and application constants (supported languages, models) are isolated in `utils/`, ensuring high maintainability.

## 🚀 Getting Started

### Prerequisites
* Python 3.10 or higher.
* **FFmpeg:** This application requires `ffmpeg.exe` to extract audio streams. 
  1. Download the essential build from [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/).
  2. Extract the `.zip` and place `ffmpeg.exe` (found in the `bin` folder) directly into the root directory of this project.

### Installation

1. Clone the repository:
```bash
git clone [https://github.com/LucasAlmeida1396/pro-transcriber.git](https://github.com/LucasAlmeida1396/pro-transcriber.git)
cd pro-transcriber
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows use:
venv\Scripts\activate
# On Linux/Mac use:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

## 📦 Building the Executable (.exe)

To package the application into a standalone Windows executable, run:

```bash
pyinstaller --noconsole --name "ProTranscriber" --icon="assets/logo.ico" main.py
```

*Note: After the build is complete, ensure you copy `ffmpeg.exe` into the generated `dist/ProTranscriber` folder before distributing.*

## 👨‍💻 Author

**Lucas Pacheco de Almeida**
* LinkedIn: https://www.linkedin.com/in/lucas-de-almeida-a099053ba/
* GitHub: https://github.com/LucasAlmeida1396

---
*If you find this project interesting or helpful, feel free to reach out or leave a ⭐!*