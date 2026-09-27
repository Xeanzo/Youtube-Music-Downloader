import os
import sys
import glob
import threading
import subprocess
import customtkinter as ctk

# Set Appearance Base
ctk.set_appearance_mode("Dark")

# Palette Warna Gen-Z / Modern Dark Aesthetics
COLOR_BG_DARK = "#0D0F17"       # Dark Obsidian
COLOR_CARD_BG = "#161926"       # Deep Slate Card
COLOR_BORDER = "#2A2E43"        # Subtle Border
COLOR_PRIMARY = "#8B5CF6"       # Electric Violet
COLOR_PRIMARY_HOVER = "#7C3AED"
COLOR_ACCENT = "#06B6D4"        # Cyber Cyan
COLOR_AMBER = "#F59E0B"         # Hot Amber
COLOR_AMBER_HOVER = "#D97706"
COLOR_TEXT_MAIN = "#F3F4F6"     # Pure White/Light Gray
COLOR_TEXT_MUTED = "#9CA3AF"    # Slate Gray

# Fallback Font Stack ke Poppins
FONT_FAMILY = "Poppins"

class XeanzoGenZDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Config
        self.title("Xeanzo Music Downloader v2.5 • Gen-Z Edition")
        self.geometry("680x670")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_BG_DARK)

        # Path Setup
        self.download_folder = os.path.join(os.getcwd(), "Downloads")
        self.archive_file = os.path.join(self.download_folder, "downloaded_history.txt")
        self.success_count = 0

        # Building UI Components
        self._build_header()
        self._build_url_card()
        self._build_options_card()
        self._build_action_buttons()
        self._build_console_card()

    def _build_header(self):
        """Header Banner dengan Badge & Typo Poppins"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(22, 10))

        top_bar = ctk.CTkFrame(header_frame, fg_color="transparent")
        top_bar.pack(fill="x")

        title = ctk.CTkLabel(
            top_bar, 
            text="⚡ YOUTUBE MUSIC DOWNLOAD AUTOMATION", 
            font=ctk.CTkFont(family=FONT_FAMILY, size=21, weight="bold"),
            text_color=COLOR_TEXT_MAIN
        )
        title.pack(side="left")

        # Pill Badge Ornament
        badge = ctk.CTkLabel(
            top_bar,
            text="PRO v2.5",
            font=ctk.CTkFont(family=FONT_FAMILY, size=10, weight="bold"),
            fg_color=COLOR_PRIMARY,
            text_color="#FFFFFF",
            corner_radius=12,
            padx=10,
            pady=2
        )
        badge.pack(side="left", padx=10)

        subtitle = ctk.CTkLabel(
            header_frame, 
            text="Bulk Audio Extraction & MP3 320kbps High-Fidelity Converter", 
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=COLOR_TEXT_MUTED
        )
        subtitle.pack(anchor="w", pady=(3, 0))

    def _build_url_card(self):
        """Input Container Card"""
        url_card = ctk.CTkFrame(
            self, 
            fg_color=COLOR_CARD_BG, 
            border_color=COLOR_BORDER, 
            border_width=1, 
            corner_radius=14
        )
        url_card.pack(fill="x", padx=25, pady=8)

        lbl = ctk.CTkLabel(
            url_card, 
            text="🔗 YOUTUBE TARGET URL", 
            font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold"),
            text_color=COLOR_ACCENT
        )
        lbl.pack(anchor="w", padx=18, pady=(14, 6))

        self.entry_url = ctk.CTkEntry(
            url_card, 
            placeholder_text="Paste Channel, Playlist, or Video URL here...", 
            height=42,
            fg_color=COLOR_BG_DARK,
            border_color=COLOR_BORDER,
            border_width=1,
            text_color=COLOR_TEXT_MAIN,
            placeholder_text_color=COLOR_TEXT_MUTED,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            corner_radius=10
        )
        self.entry_url.pack(fill="x", padx=18, pady=(0, 16))

    def _build_options_card(self):
        """Options Grid Container"""
        options_card = ctk.CTkFrame(
            self, 
            fg_color=COLOR_CARD_BG, 
            border_color=COLOR_BORDER, 
            border_width=1, 
            corner_radius=14
        )
        options_card.pack(fill="x", padx=25, pady=8)

        inner = ctk.CTkFrame(options_card, fg_color="transparent")
        inner.pack(fill="x", padx=18, pady=14)

        # Row 1: Order Sequence
        lbl_order = ctk.CTkLabel(
            inner, 
            text="Urutan Unduh:", 
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
            text_color=COLOR_TEXT_MAIN
        )
        lbl_order.grid(row=0, column=0, sticky="w", padx=(0, 15))

        self.order_var = ctk.StringVar(value="terbaru")
        self.radio_new = ctk.CTkRadioButton(
            inner, 
            text="Terbaru Dulu", 
            variable=self.order_var, 
            value="terbaru",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER
        )
        self.radio_new.grid(row=0, column=1, padx=8)

        self.radio_old = ctk.CTkRadioButton(
            inner, 
            text="Terlama Dulu", 
            variable=self.order_var, 
            value="terlama",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER
        )
        self.radio_old.grid(row=0, column=2, padx=8)

        # Row 2: Audio Quality Selection
        lbl_quality = ctk.CTkLabel(
            inner, 
            text="Bitrate Audio:", 
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
            text_color=COLOR_TEXT_MAIN
        )
        lbl_quality.grid(row=1, column=0, sticky="w", pady=(14, 0), padx=(0, 15))

        self.combo_quality = ctk.CTkOptionMenu(
            inner, 
            values=["320 kbps (High Quality)", "192 kbps (Standard)", "128 kbps (Low)"], 
            width=180,
            height=32,
            fg_color=COLOR_BG_DARK,
            button_color=COLOR_PRIMARY,
            button_hover_color=COLOR_PRIMARY_HOVER,
            dropdown_fg_color=COLOR_CARD_BG,
            dropdown_hover_color=COLOR_BORDER,
            font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold"),
            corner_radius=8
        )
        self.combo_quality.grid(row=1, column=1, columnspan=2, pady=(14, 0), sticky="w")

    def _build_action_buttons(self):
        """Main Action Buttons Frame"""
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=25, pady=12)

        self.btn_download = ctk.CTkButton(
            btn_frame, 
            text="🚀  Mulai Download Bulk", 
            command=self.start_download_thread,
            height=46,
            corner_radius=12,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold")
        )
        self.btn_download.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.btn_convert = ctk.CTkButton(
            btn_frame, 
            text="🔄  Batch Convert WebM", 
            command=self.start_convert_thread,
            height=46,
            corner_radius=12,
            fg_color=COLOR_AMBER,
            hover_color=COLOR_AMBER_HOVER,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold")
        )
        self.btn_convert.pack(side="right", fill="x", expand=True, padx=(6, 0))

    def _build_console_card(self):
        """Status Bar & Output Console Container"""
        console_card = ctk.CTkFrame(
            self, 
            fg_color=COLOR_CARD_BG, 
            border_color=COLOR_BORDER, 
            border_width=1, 
            corner_radius=14
        )
        console_card.pack(fill="both", expand=True, padx=25, pady=(4, 22))

        # Glowing Progress Bar
        self.progress_bar = ctk.CTkProgressBar(
            console_card, 
            height=8, 
            corner_radius=4,
            progress_color=COLOR_ACCENT,
            fg_color=COLOR_BG_DARK
        )
        self.progress_bar.pack(fill="x", padx=18, pady=(16, 12))
        self.progress_bar.set(0)

        # Terminal Console Box
        self.textbox_status = ctk.CTkTextbox(
            console_card, 
            corner_radius=10,
            fg_color=COLOR_BG_DARK,
            text_color=COLOR_TEXT_MAIN,
            font=ctk.CTkFont(family="Consolas", size=11),
            border_color=COLOR_BORDER,
            border_width=1
        )
        self.textbox_status.pack(fill="both", expand=True, padx=18, pady=(0, 16))
        self.textbox_status.insert("0.0", "[System] Xeanzo Music Automation Initialized.\n[System] Ready to fetch YouTube tracks...\n")
        self.textbox_status.configure(state="disabled")

    def log(self, message):
        """Logger Writer"""
        self.textbox_status.configure(state="normal")
        self.textbox_status.insert("end", message + "\n")
        self.textbox_status.see("end")
        self.textbox_status.configure(state="disabled")

    def start_download_thread(self):
        raw_url = self.entry_url.get().strip()
        if not raw_url:
            self.log("[!] Error: Silakan masukkan URL YouTube terlebih dahulu!")
            return

        if "@" in raw_url and not any(sub in raw_url for sub in ["/videos", "/playlists", "/featured", "/shorts"]):
            url = raw_url.rstrip("/") + "/videos"
            self.log(f"[*] Auto-fix URL -> {url}")
        else:
            url = raw_url

        self.btn_download.configure(state="disabled")
        self.btn_convert.configure(state="disabled")
        self.progress_bar.set(0)
        self.success_count = 0
        
        is_reverse = (self.order_var.get() == "terlama")
        q_val = self.combo_quality.get().split()[0]
        
        threading.Thread(target=self.run_download, args=(url, is_reverse, q_val), daemon=True).start()

    def start_convert_thread(self):
        self.btn_download.configure(state="disabled")
        self.btn_convert.configure(state="disabled")
        self.progress_bar.set(0)
        threading.Thread(target=self.run_local_convert, daemon=True).start()

    def run_local_convert(self):
        self.log("\n[*] Memulai konversi batch file .webm lokal ke MP3...")
        webm_files = glob.glob(os.path.join(self.download_folder, "*.webm"))
        
        if not webm_files:
            self.log("[!] Tidak ditemukan file .webm di folder Downloads.")
            self.btn_download.configure(state="normal")
            self.btn_convert.configure(state="normal")
            return

        total = len(webm_files)
        self.log(f"[*] Ditemukan {total} file .webm yang akan dikonversi...\n")

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
                self.log(f"[!] Error: {e}")

            self.progress_bar.set(idx / total)

        self.log(f"\n[+] SELESAI! {converted} file dikonversi!")
        self.btn_download.configure(state="normal")
        self.btn_convert.configure(state="normal")

    def run_download(self, url, is_reverse, quality):
        self.log(f"\n[*] Target URL : {url}")
        self.log(f"[*] Bitrate    : {quality} kbps")
        
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

        try:
            import yt_dlp
        except ImportError:
            self.log("[*] Installing yt-dlp module...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
            import yt_dlp

        def my_hook(d):
            if d['status'] == 'downloading':
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 1)
                if total > 0:
                    self.progress_bar.set(downloaded / total)
            elif d['status'] == 'finished':
                self.success_count += 1
                filename = os.path.basename(d.get('filename', ''))
                self.log(f"[✓] Track Ready: {filename}")

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': quality},
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
        self.log(f"\n[+] SUCCESS! Total file MP3 baru terunduh: {self.success_count}")
        self.btn_download.configure(state="normal")
        self.btn_convert.configure(state="normal")

if __name__ == "__main__":
    app = XeanzoGenZDownloader()
    app.mainloop()