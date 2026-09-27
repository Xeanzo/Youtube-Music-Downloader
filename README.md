# 🎵 YouTube Music Automation Downloader (GUI)

A modern, fast, and lightweight Python desktop application built with `CustomTkinter` and `yt-dlp` to bulk download YouTube channels or playlists into high-quality **MP3 320kbps** with automated metadata & thumbnail embedding.

Developed by **Gigih Jean Fariellana** ([@xeanzo](https://github.com/xeanzo)).

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-blue?style=for-the-badge)
![yt-dlp](https://img.shields.io/badge/Engine-yt--dlp-red?style=for-the-badge)

---

## ✨ Features

- **Modern Dark Mode GUI:** Clean and intuitive user interface built using `CustomTkinter`.
- **High-Quality Audio:** Automatic extraction and conversion to **MP3 320kbps** with full ID3 metadata.
- **Auto URL Corrector:** Automatically appends `/videos` tab for YouTube channel URLs to prevent extraction errors.
- **Anti-Duplicate Archive:** Smart history tracker (`downloaded_history.txt`) prevents re-downloading previously fetched tracks.
- **Flexible Sorting:** Option to download tracks starting from the **Newest** or **Oldest** upload.
- **Emergency WebM -> MP3 Converter:** Built-in tool to instantly convert offline `.webm` files to `.mp3` using FFmpeg without re-downloading.
- **Real-time Progress & Logging:** Live progress bar and log console for full visibility.

---

## 🛠️ Prerequisites

1. **Python 3.10+**
2. **FFmpeg** (Required for audio conversion to MP3)
   ```powershell
   winget install FFmpeg