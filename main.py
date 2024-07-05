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
        self.geometry("600x600")

        self.chapter_vars = []
        self.chapter_titles = []

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

        self.chapter_list_frame = tk.Frame(self)
        self.chapter_list_frame.pack(pady=5)

        self.list_chapters_button = tk.Button(
            self, text="Listar Capítulos", command=self.list_chapters
        )
        self.list_chapters_button.pack(pady=5)

        self.download_button = tk.Button(
            self, text="Baixar", command=self.start_download, state=tk.DISABLED
        )
        self.download_button.pack(pady=5)

        self.progress_label = tk.Label(self, text="Progresso")
        self.progress_label.pack(pady=5)

        self.progress_bar = Progressbar(
            self, orient=tk.HORIZONTAL, length=500, mode="determinate"
        )
        self.progress_bar.pack(pady=20)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.download_dir.set(directory)

    def list_chapters(self):
        url = self.url_entry.get()

        if not url:
            messagebox.showerror("Erro", "Por favor, insira uma URL válida.")
            return

        self.chapter_vars = []
        self.chapter_titles = []
        for widget in self.chapter_list_frame.winfo_children():
            widget.destroy()

        threading.Thread(target=self.fetch_chapters, args=(url,)).start()

    def fetch_chapters(self, url):
        ydl_opts = {"format": "best", "writeinfojson": True, "clean_infojson": True}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(url, download=False)
                if "chapters" in result:
                    self.chapter_titles = result["chapters"]
                    self.display_chapters()
                else:
                    messagebox.showinfo("Info", "Este vídeo não contém capítulos.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def display_chapters(self):
        for chapter in self.chapter_titles:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(
                self.chapter_list_frame, text=chapter["title"], variable=var
            )
            chk.pack(anchor="w")
            self.chapter_vars.append(var)

        self.download_button.config(state=tk.NORMAL)

    def start_download(self):
        url = self.url_entry.get()
        format = self.format_combobox.get()
        separate_chapters = self.chapter_var.get()
        download_dir = self.download_dir.get()
        selected_chapters = [var.get() for var in self.chapter_vars]

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
            args=(url, format, separate_chapters, download_dir, selected_chapters),
        ).start()

    def sanitize_filename(self, filename):
        directory, filename = os.path.split(filename)
        name, ext = os.path.splitext(filename)
        sanitized_name = re.sub(r"[^\w\s]", "", name)  # Remove caracteres especiais
        sanitized_name = re.sub(r"\s+", "_", sanitized_name)  # Substitui espaços por _
        return os.path.join(directory, sanitized_name + ext)

    def changeName(self, pathDir, oldFileName, newFileName):
        os.chdir(pathDir)

        for filename in os.listdir(pathDir):
            if filename.startswith(oldFileName):
                os.rename(
                    os.path.join(filename), os.path.join(filename[len(newFileName) :])
                )

    def download_video(
        self, url, format, separate_chapters, download_dir, selected_chapters
    ):
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
                original_title = result["title"]

                # Constrói o nome original do arquivo
                original_video_name = os.path.join(
                    download_dir,
                    (
                        f"{original_title}.mp4"
                        if format != "mp3"
                        else f"{original_title}.mp3"
                    ),
                )

                # Sanitize filenames
                sanitized_video_name = self.sanitize_filename(original_video_name)

                # Renomeando o arquivo, se existir
                self.changeName(
                    self.download_dir.get(), original_video_name, sanitized_video_name
                )
                lista_arqs = [arq for arq in os.listdir(self.download_dir.get())]
                print(f"Arquivos da pasta: {lista_arqs}")

                # if os.path.exists(original_video_name):
                #     try:
                #         os.rename(original_video_name, sanitized_video_name)
                #     except Exception as e:
                #         print(f"Erro ao renomear arquivo: {e}")

                print(f"sanitized_video_name: {sanitized_video_name}")

                if separate_chapters and "chapters" in result:
                    self.split_video_into_chapters(
                        result,
                        download_dir,
                        format,
                        selected_chapters,
                        sanitized_video_name,
                    )

            messagebox.showinfo("Sucesso", "Download concluído!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            self.download_button.config(state=tk.NORMAL)
            self.progress_bar["value"] = 0

    def split_video_into_chapters(
        self, video_info, download_dir, format, selected_chapters, video_file
    ):
        ffmpeg_path = self.get_ffmpeg_path()
        print(f"FFmpeg path: {ffmpeg_path}")
        print(f"Video file: {video_file}")
        print(f"Video chapters: {video_info['chapters']}")

        for index, chapter in enumerate(video_info["chapters"]):
            if not selected_chapters[index]:
                print(f"Chapter {chapter['title']} not selected.")
                continue
            start_time = chapter["start_time"]
            end_time = chapter["end_time"]
            chapter_title = chapter["title"].replace(" ", "_").replace("/", "-")
            output_file = os.path.join(download_dir, f"{chapter_title}.{format}")
            print(f"output_file chapter {output_file}")

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
            print(f"ffmpeg_command chapter {ffmpeg_command}")

            print(f"Running FFmpeg command: {' '.join(ffmpeg_command)}")

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
