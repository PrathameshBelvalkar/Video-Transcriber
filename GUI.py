import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread
import whisper
import os
import torch
from moviepy.editor import VideoFileClip

class VideoTranscriber:
    def __init__(self, model_path, video_path, progress_callback):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        self.model = whisper.load_model(model_path).to(self.device)
        self.video_path = video_path
        self.audio_path = ''
        self.subtitles = []
        self.progress_callback = progress_callback

    def transcribe_video(self):
        print('Starting video transcription...')
        result = self.model.transcribe(self.audio_path, verbose=True)
        
        total_segments = len(result["segments"])
        subtitle_text = ""
        for idx, segment in enumerate(result["segments"]):
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]
            self.subtitles.append((start, end, text))
            subtitle_text += f"{self.format_timestamp(start)} --> {self.format_timestamp(end)}: {text}\n"
            self.progress_callback(subtitle_text, idx + 1 == total_segments)
        
        print('Video transcription complete')
        self.generate_srt()

    def format_timestamp(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    def generate_srt(self):
        base_name = os.path.splitext(os.path.basename(self.video_path))[0]
        srt_path = os.path.join(os.path.dirname(self.video_path), f"{base_name}.srt")
        with open(srt_path, "w", encoding="utf-8") as srt_file:
            for index, (start, end, text) in enumerate(self.subtitles, start=1):
                srt_file.write(f"{index}\n")
                srt_file.write(f"{self.format_timestamp(start)} --> {self.format_timestamp(end)}\n")
                srt_file.write(f"{text}\n\n")
        print(f'SRT file generated at {srt_path}')
       
        if os.path.exists(self.audio_path):
            os.remove(self.audio_path)
            print(f'Deleted audio file: {self.audio_path}')

    def extract_audio(self):
        print('Extracting audio from video...')
        self.audio_path = os.path.join(os.path.dirname(self.video_path), "audio.mp3")
        video = VideoFileClip(self.video_path)
        audio = video.audio
        audio.write_audiofile(self.audio_path)
        print(f'Audio extracted to {self.audio_path}')

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Transcriber")
        self.root.geometry("600x400")
        self.model_path = "base"
        self.video_path = None

        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.file_label = tk.Label(self.frame, text="Choose File")
        self.file_label.grid(row=0, column=0, pady=5, sticky="w")
        
        self.file_button = tk.Button(self.frame, text="Browse", command=self.select_file)
        self.file_button.grid(row=0, column=1, pady=5, sticky="e")

        self.text_area = tk.Text(self.frame, wrap="word", height=15, width=70, state="disabled")
        self.text_area.grid(row=1, column=0, columnspan=2, pady=10)

        self.process_button = tk.Button(self.frame, text="Process", command=self.process_video)
        self.process_button.grid(row=2, column=0, columnspan=2, pady=10)

    def select_file(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
        if self.video_path:
            pass

    def process_video(self):
        if not self.video_path:
            tk.messagebox.showwarning("No file selected", "Please select a video file first.")
            return

        self.process_button.config(state=tk.DISABLED)
        self.text_area.config(state="normal")
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, "Subtitles are processing. You will see them here shortly...\n")
        self.text_area.config(state="disabled")

        transcriber = VideoTranscriber(self.model_path, self.video_path, self.update_text_area)
        self.thread = Thread(target=self.run_transcription, args=(transcriber,))
        self.thread.start()

    def run_transcription(self, transcriber):
        transcriber.extract_audio()
        transcriber.transcribe_video()
        self.process_button.config(state=tk.NORMAL)
        tk.messagebox.showinfo("Process Complete", "Transcription and SRT generation completed successfully.")
        print(f'Subtitle file path: {os.path.join(os.path.dirname(self.video_path), f"{os.path.splitext(os.path.basename(self.video_path))[0]}.srt")}')

    def update_text_area(self, subtitle_text, done=False):
        if done:
            self.text_area.config(state="normal")
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert(tk.END, subtitle_text)
            self.text_area.config(state="disabled")
        else:
            self.text_area.config(state="normal")
            self.text_area.insert(tk.END, subtitle_text)
            self.text_area.yview(tk.END)  
            self.text_area.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
