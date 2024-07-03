import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.ttk import Progressbar, Combobox, Checkbutton
import threading
import yt_dlp
import re
import os
import subprocess
import sys


class YouTubeDownloader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader")
        self.geometry("600x400")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="URL do vídeo:").pack(pady=5)
        self.url_entry = tk.Entry(self, width=60)
        self.url_entry.pack(pady=5)

        tk.Label(self, text="Formato:").pack(pady=5)
        self.format_combobox = Combobox(self, values=["mp4", "mp3"], state="readonly")
        self.format_combobox.current(0)
        self.format_combobox.pack(pady=5)

        self.chapter_var = tk.BooleanVar()
        self.chapter_checkbox = Checkbutton(
            self, text="Separar por capítulos", variable=self.chapter_var
        )
        self.chapter_checkbox.pack(pady=5)

        self.download_dir = tk.StringVar()
        self.download_dir.set("Escolha o diretório de salvamento")

        self.select_dir_button = tk.Button(
            self, text="Selecionar Diretório", command=self.select_directory
        )
        self.select_dir_button.pack(pady=5)

        self.download_dir_label = tk.Label(self, textvariable=self.download_dir)
        self.download_dir_label.pack(pady=5)

        self.progress_label = tk.Label(self, text="Progresso")
        self.progress_label.pack(pady=5)

        self.progress_bar = Progressbar(
            self, orient=tk.HORIZONTAL, length=500, mode="determinate"
        )
        self.progress_bar.pack(pady=20)

        self.download_button = tk.Button(
            self, text="Baixar", command=self.start_download
        )
        self.download_button.pack(pady=5)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.download_dir.set(directory)

    def start_download(self):
        url = self.url_entry.get()
        format = self.format_combobox.get()
        separate_chapters = self.chapter_var.get()
        download_dir = self.download_dir.get()

        if not url:
            messagebox.showerror("Erro", "Por favor, insira uma URL válida.")
            return

        if download_dir == "Escolha o diretório de salvamento":
            messagebox.showerror(
                "Erro", "Por favor, selecione um diretório de salvamento."
            )
            return

        threading.Thread(
            target=self.download_video,
            args=(url, format, separate_chapters, download_dir),
        ).start()

    def download_video(self, url, format, separate_chapters, download_dir):
        self.download_button.config(state=tk.DISABLED)
        output_template = os.path.join(download_dir, "%(title)s.%(ext)s")

        ydl_opts = {
            "format": "bestaudio/best" if format == "mp3" else "best",
            "postprocessors": (
                [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}]
                if format == "mp3"
                else []
            ),
            "progress_hooks": [self.progress_hook],
            "outtmpl": output_template,
            "writeinfojson": True,
            "clean_infojson": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(url, download=True)
                if separate_chapters and "chapters" in result:
                    self.split_video_into_chapters(result, download_dir, format)
            messagebox.showinfo("Sucesso", "Download concluído!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            self.download_button.config(state=tk.NORMAL)
            self.progress_bar["value"] = 0

    def split_video_into_chapters(self, video_info, download_dir, format):
        video_file = os.path.join(download_dir, f"{video_info['title']}.{format}")
        if not os.path.exists(video_file):
            return

        ffmpeg_path = self.get_ffmpeg_path()

        for chapter in video_info["chapters"]:
            start_time = chapter["start_time"]
            end_time = chapter["end_time"]
            chapter_title = chapter["title"].replace(" ", "_").replace("/", "-")
            output_file = os.path.join(download_dir, f"{chapter_title}.{format}")

            ffmpeg_command = [
                ffmpeg_path,
                "-i",
                video_file,
                "-ss",
                str(start_time),
                "-to",
                str(end_time),
                "-c",
                "copy",
                output_file,
            ]

            self.update_progress_label(f"Baixando capítulo: {chapter['title']}")
            subprocess.run(ffmpeg_command)

    def get_ffmpeg_path(self):
        if sys.platform == "win32":
            return os.path.join(
                os.path.dirname(__file__), "ffmpeg", "windows", "ffmpeg.exe"
            )
        elif sys.platform == "darwin":
            return os.path.join(os.path.dirname(__file__), "ffmpeg", "macos", "ffmpeg")
        elif sys.platform == "linux":
            return os.path.join(os.path.dirname(__file__), "ffmpeg", "linux", "ffmpeg")
        else:
            raise ValueError("Sistema operacional não suportado")

    def update_progress_label(self, text):
        self.progress_label.config(text=text)

    def progress_hook(self, d):
        if d["status"] == "downloading":
            percent_str = re.search(r"(\d+\.\d+)%", d["_percent_str"])
            if percent_str:
                percent = float(percent_str.group(1))
                self.progress_bar["value"] = percent
                self.update_progress_label(f"{d['filename']}: {percent}%")


if __name__ == "__main__":
    app = YouTubeDownloader()
    app.mainloop()
