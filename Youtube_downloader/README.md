@'
# Asynchronous YouTube Video and Audio Downloader

A lightweight, production-grade desktop application built with Python that allows users to securely extract highest-quality video streams or high-fidelity MP3 audio directly from YouTube URLs. 

Designed natively with custom dark/light UI support, the project implements concurrent networking pipelines to insulate the application interface layer against thread starvation and freezing.

---

## Features

- **Asynchronous Architecture:** Leverages Python threading systems to offload network resolution, extraction, and post-processing computations away from the primary event loop, keeping the UI fully interactive and context-responsive.
- **Real-time Stream Analytics:** Integrates native yt-dlp hook interceptions to parse telemetry data on the fly, rendering live progress percentage meters alongside streaming connection speed metrics (e.g., 4.7 MB/s).
- **Mid-Stream Cancellation:** Employs explicit condition flags combined with yt_dlp.utils.DownloadCancelled triggers to gracefully terminate active socket connections mid-download and clear runtime stream fragments safely.
- **Clean Link Handling:** Implements automatic string and parameter routing filters ('noplaylist': True) to bypass background mixing queues and isolate solo video targets from playlist links.
- **Modern Dark Mode GUI:** Designed using CustomTkinter widgets featuring automatic OS accent themes, dynamic operational button layouts, and system folder interaction dialogues.

---

## Technology Stack

- **Core Language:** Python 3.11+
- **Graphical Interface Engine:** CustomTkinter (Declarative Tkinter Layer)
- **Extraction Core Wrapper:** yt-dlp
- **Stream Concurrency Provider:** threading (Native Python Execution Block)
- **Multimedia Processing Pipeline:** FFmpeg (Required for audio track conversion and high-definition multi-stream merging)

---

## Repository Structure

```text
youtube-downloader/
│
├── __pycache__/             # Compiled bytecode cache blocks (Ignored by Git)
├── venv/                    # Isolated runtime environment packages (Ignored by Git)
├── .gitignore               # Explicit tracking exclusion matrices
├── app.py                   # Main GUI Application Thread and State Manager
├── downloader.py            # Deep-level yt-dlp and FFmpeg interface backend
└── requirements.txt         # Explicitly locked dependency manifest
```

---

## Getting Started

### 1. Prerequisites (Stitching Engine Installation)
Because YouTube splits high-definition video and audio tracks, FFmpeg must be installed and globally registered to your system path to perform post-download merging.

Open an Administrator PowerShell window and install it automatically via the Windows Package Manager:
```powershell
winget install Gyan.FFmpeg
```
*Restart your terminal and run ffmpeg -version to verify successful path mapping.*

### 2. Installation and Setup Pipeline

1. **Clone the repository space:**
   ```bash
   git clone https://github.com
   cd youtube-downloader
   ```

2. **Activate your isolated project virtual environment:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   venv\Scripts\activate
   ```

3. **Install application dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Desktop Application:**
   ```bash
   python app.py
   ```

---

## License and Project Disclaimer
This project is open-source and intended strictly for educational research purposes and portfolio evaluation. Downloading copyrighted content or deploying unauthorized stream parsers violates YouTube's global Terms of Service. The developer assumes no liability for external usage patterns.
'@ | Out-File -FilePath README.md -Encoding utf8
