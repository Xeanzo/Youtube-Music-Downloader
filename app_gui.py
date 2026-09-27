import os
import sys
import glob
import threading
import subprocess
import customtkinter as ctk

# Set Tema Tampilan (Dark Mode)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class XeanzoMusicDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Config
        self.title("Xeanzo YouTube Music Downloader v1.1")
        self.geometry("620x570")
        self.resizable(False, False)

        # Path Setup
        self.download_folder = os.path.join(os.getcwd(), "Downloads")
        self.archive_file = os.path.join(self.download_folder, "downloaded_history.txt")
        self.success_count = 0

        # Header Title
        self.label_title = ctk.CTkLabel(
            self, 
            text="YouTube Music Automation Downloader", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label_title.pack(pady=(20, 2))

        self.label_subtitle = ctk.CTkLabel(
            self, 
            text="Bulk Downloader & Auto-Converter MP3 320kbps (by Xeanzo)", 
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.label_subtitle.pack(pady=(0, 10))

        # Input URL
        self.entry_url = ctk.CTkEntry(
            self, 
            placeholder_text="Masukkan link Channel / Playlist / Video...", 
            width=540,
            height=38
        )
        self.entry_url.pack(pady=5)

        # Frame Opsi Urutan Download
        self.frame_options = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_options.pack(pady=5)

        self.label_order = ctk.CTkLabel(self.frame_options, text="Urutan Download:")
        self.label_order.pack(side="left", padx=(0, 10))

        self.order_var = ctk.StringVar(value="terbaru")
        self.radio_newest = ctk.CTkRadioButton(
            self.frame_options, text="Video Terbaru Dulu", variable=self.order_var, value="terbaru"
        )
        self.radio_newest.pack(side="left", padx=10)

        self.radio_oldest = ctk.CTkRadioButton(
            self.frame_options, text="Video Terlama Dulu", variable=self.order_var, value="terlama"
        )
        self.radio_oldest.pack(side="left", padx=10)

        # Frame Tombol Action
        self.frame_btn = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_btn.pack(pady=10)

        # Tombol Download
        self.btn_download = ctk.CTkButton(
            self.frame_btn, 
            text="Mulai Download MP3", 
            command=self.start_download_thread,
            height=42,
            width=260,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_download.pack(side="left", padx=5)

        # Tombol Convert WebM ke MP3
        self.btn_convert = ctk.CTkButton(
            self.frame_btn, 
            text="Convert Local WebM -> MP3", 
            command=self.start_convert_thread,
            height=42,
            width=260,
            fg_color="#D97706",
            hover_color="#B45309",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.btn_convert.pack(side="left", padx=5)

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self, width=540)
        self.progress_bar.pack(pady=5)
        self.progress_bar.set(0)

        # Log Status Output Box
        self.textbox_status = ctk.CTkTextbox(self, width=540, height=160)
        self.textbox_status.pack(pady=10)
        self.textbox_status.insert("0.0", "[System] Aplikasi siap digunakan.\n[!] Jika hasil berbentuk .webm, klik 'Convert Local WebM -> MP3' untuk mengubahnya cepat tanpa download ulang.\n\n")
        self.textbox_status.configure(state="disabled")

    def log(self, message):
        """Menampilkan teks log ke dalam box status"""
        self.textbox_status.configure(state="normal")
        self.textbox_status.insert("end", message + "\n")
        self.textbox_status.see("end")
        self.textbox_status.configure(state="disabled")

    def start_download_thread(self):
        raw_url = self.entry_url.get().strip()
        if not raw_url:
            self.log("[!] URL tidak boleh kosong!")
            return

        if "@" in raw_url and not any(sub in raw_url for sub in ["/videos", "/playlists", "/featured", "/shorts"]):
            url = raw_url.rstrip("/") + "/videos"
            self.log(f"[*] URL disesuaikan otomatis ke tab videos: {url}")
        else:
            url = raw_url

        self.btn_download.configure(state="disabled")
        self.btn_convert.configure(state="disabled")
        self.progress_bar.set(0)
        self.success_count = 0
        
        is_reverse = (self.order_var.get() == "terlama")
        threading.Thread(target=self.run_download, args=(url, is_reverse), daemon=True).start()

    def start_convert_thread(self):
        self.btn_download.configure(state="disabled")
        self.btn_convert.configure(state="disabled")
        self.progress_bar.set(0)
        threading.Thread(target=self.run_local_convert, daemon=True).start()

    def run_local_convert(self):
        self.log("\n[*] Memulai konversi file lokal WebM ke MP3...")
        webm_files = glob.glob(os.path.join(self.download_folder, "*.webm"))
        
        if not webm_files:
            self.log("[!] Tidak ditemukan file .webm di folder Downloads.")
            self.btn_download.configure(state="normal")
            self.btn_convert.configure(state="normal")
            return

        total = len(webm_files)
        self.log(f"[*] Ditemukan {total} file .webm yang akan dikonversi.\n")

        converted = 0
        for idx, file_path in enumerate(webm_files, start=1):
            mp3_path = os.path.splitext(file_path)[0] + ".mp3"
            cmd = f'ffmpeg -y -i "{file_path}" -vn -ab 320k -ar 44100 "{mp3_path}"'
            try:
                subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if os.path.exists(mp3_path):
                    os.remove(file_path)
                    converted += 1
                    self.log(f"[{idx}/{total}] [✓] Converted: {os.path.basename(mp3_path)}")
            except Exception as e:
                self.log(f"[!] Error convert {os.path.basename(file_path)}: {e}")

            self.progress_bar.set(idx / total)

        self.log(f"\n[+] SELESAI! {converted} file berhasil diubah jadi MP3 320kbps!")
        self.btn_download.configure(state="normal")
        self.btn_convert.configure(state="normal")

    def run_download(self, url, is_reverse):
        self.log(f"\n[*] Memproses link: {url}")
        
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

        try:
            import yt_dlp
        except ImportError:
            self.log("[*] Menginstall modul yt-dlp...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
            import yt_dlp

        def my_hook(d):
            if d['status'] == 'downloading':
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 1)
                if total > 0:
                    percentage = downloaded / total
                    self.progress_bar.set(percentage)
            elif d['status'] == 'finished':
                self.success_count += 1
                filename = os.path.basename(d.get('filename', ''))
                self.log(f"[✓] File Selesai: {filename}")

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'},
                {'key': 'FFmpegMetadata'},
            ],
            'outtmpl': os.path.join(self.download_folder, '%(title)s.%(ext)s'),
            'download_archive': self.archive_file,
            'ignoreerrors': True,
            'progress_hooks': [my_hook],
            'quiet': True,
            'no_warnings': True,
            'playlistreverse': is_reverse,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        self.progress_bar.set(1)
        self.log(f"\n[+] SELESAI! Total file terunduh: {self.success_count}")
        self.log(f"[+] Lokasi Penyimpanan: {self.download_folder}")
        self.btn_download.configure(state="normal")
        self.btn_convert.configure(state="normal")

if __name__ == "__main__":
    app = XeanzoMusicDownloader()
    app.mainloop()