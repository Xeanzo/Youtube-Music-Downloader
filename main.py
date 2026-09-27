import os
import sys
import subprocess

def check_and_install_ytdlp():
    try:
        import yt_dlp
    except ImportError:
        print("[*] 'yt-dlp' belum terinstall. Menginstall otomatis...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])

def main():
    check_and_install_ytdlp()
    import yt_dlp

    print("==================================================")
    print("        YOUTUBE MUSIC DOWNLOADER AUTOMATION       ")
    print("==================================================")
    
    url = input("\nMasukkan Link YouTube (Channel/Playlist/Video): ").strip()
    
    if not url:
        print("[!] Link tidak boleh kosong!")
        return

    output_folder = "Downloads"
    archive_file = os.path.join(output_folder, "downloaded_history.txt")

    # Counter statistik
    stats = {'success': 0}

    def my_hook(d):
        if d['status'] == 'downloading':
            # Menampilkan progress ringkas saat download berjalan
            p = d.get('_percent_str', '0%').strip()
            speed = d.get('_speed_str', 'N/A').strip()
            print(f"\r  [Downloading] {p} | Kecepatan: {speed}", end='', flush=True)
        elif d['status'] == 'finished':
            stats['success'] += 1
            print(f"\n  [✓] Selesai & Dikonversi ke MP3: {os.path.basename(d.get('filename', ''))}\n")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'},
            {'key': 'FFmpegMetadata'},
        ],
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'download_archive': archive_file,
        'ignoreerrors': True,
        'progress_hooks': [my_hook],
        'quiet': True,
        'no_warnings': True,
        
        # TRIK CEPAT: Mengunduh langsung tanpa scanning panjang di awal
        'extract_flat': 'in_playlist',
    }

    print("\n[*] Langsung memulai proses download...\n")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("==================================================")
    print("                RINGKASAN STATISTIK               ")
    print("==================================================")
    print(f" [+] File baru berhasil diunduh : {stats['success']}")
    print(f" [+] Lokasi penyimpanan         : {os.path.abspath(output_folder)}")
    print("==================================================")

if __name__ == "__main__":
    main()