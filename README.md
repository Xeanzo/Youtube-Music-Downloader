# 🎵 YouTube Music Automation Downloader (GUI)

A modern, fast, and lightweight Python desktop application built with `CustomTkinter` and `yt-dlp` to bulk-download YouTube channels or playlists into high-quality **MP3 320kbps** with automated ID3 metadata and thumbnail embedding.

Developed by **Gigih Jean Fariellana** ([@xeanzo](https://github.com/xeanzo)).

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-blue?style=for-the-badge)
![yt-dlp](https://img.shields.io/badge/Engine-yt--dlp-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## ✨ Key Features

- **Modern Dark-Mode GUI:** Clean and responsive desktop user interface built using `CustomTkinter`.
- **High-Fidelity Audio Conversion:** Automatic extraction and conversion to **MP3 320kbps** complete with full ID3 metadata.
- **Smart URL Normalization:** Automatically handles channel URL variations (e.g., appends `/videos` tab) to prevent channel extraction failures.
- **Anti-Duplicate History Logging:** Smart tracker (`downloaded_history.txt`) prevents re-downloading previously fetched tracks during incremental updates.
- **Flexible Sorting:** Option to sequence downloads starting from the **Newest** or **Oldest** upload.
- **Emergency WebM -> MP3 Batch Converter:** Built-in multithreaded FFmpeg wrapper to convert offline `.webm` files directly into `.mp3` without extra bandwidth consumption.
- **Real-Time Progress & Console Logs:** Live visual progress bar paired with log console output.

---

## 🛠️ Prerequisites

1. **Python 3.10+**
2. **FFmpeg** (Required for audio post-processing & MP3 conversion)
   ```powershell
   winget install FFmpeg