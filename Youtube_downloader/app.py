import os
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import threading
from downloader import download_video

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")

class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Modern YouTube Downloader")
        self.geometry("550x420")  
        self.resizable(False, False)

        # Download states
        self.is_downloading = False
        self.is_cancelled = False

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="YouTube Video Downloader", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.pack(padx=20, fill="x", pady=(25, 15))

        # URL Input Field
        self.url_entry = ctk.CTkEntry(self, placeholder_text="Paste your YouTube link here...", width=450, height=35)
        self.url_entry.pack(padx=20, pady=10)

        # Output Folder Selection UI
        self.folder_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.folder_frame.pack(padx=20, pady=10, fill="x")

        # Windows-friendly path layout
        default_download_path = os.path.normpath(os.path.expanduser("~/Downloads"))
        self.folder_path = tk.StringVar(value=default_download_path)
        
        self.folder_label = ctk.CTkLabel(self.folder_frame, text=f"Save to: {default_download_path}", text_color="gray", wraplength=320, anchor="w")
        self.folder_label.pack(side="left", padx=(40, 10))

        self.browse_button = ctk.CTkButton(self.folder_frame, text="Browse", width=80, command=self.browse_folder)
        self.browse_button.pack(side="right", padx=(10, 40))

        # Audio-Only Toggle Switch
        self.audio_switch_var = tk.StringVar(value="off")
        self.audio_switch = ctk.CTkSwitch(
            self, 
            text="Audio Only (Convert to MP3)", 
            variable=self.audio_switch_var, 
            onvalue="on", 
            offvalue="off",
            command=self.update_action_button_ui
        )
        self.audio_switch.pack(padx=20, pady=15)

        # Live Progress Metrics Label
        self.progress_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=13, weight="bold"), text_color="cyan")
        self.progress_label.pack(padx=20, pady=(15, 5))

        # Visual Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self, width=450, height=8)
        self.progress_bar.set(0)  
        self.progress_bar.pack(padx=20, pady=(0, 15))

        # General Status Message Label
        self.status_label = ctk.CTkLabel(self, text="", text_color="yellow", wraplength=450)
        self.status_label.pack(padx=20, pady=5)

        # Main Action Button (Serves as both Download and Cancel dynamically!)
        self.action_button = ctk.CTkButton(
            self, 
            text="Download Highest Quality Video", 
            font=ctk.CTkFont(size=14, weight="bold"), 
            height=40,
            width=250,
            command=self.handle_action_click
        )
        self.action_button.pack(padx=20, pady=20)

    def browse_folder(self):
        if self.is_downloading:
            return  # Lock browsing folder during active download
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            normalized_dir = os.path.normpath(selected_dir)
            self.folder_path.set(normalized_dir)
            self.folder_label.configure(text=f"Save to: {normalized_dir}")

    def update_action_button_ui(self):
        """Updates the button theme dynamically based on app state."""
        if self.is_downloading:
            # Change to red Cancel button state
            self.action_button.configure(text="Cancel Download", fg_color="#C0392B", hover_color="#A93226")
            self.audio_switch.configure(state="disabled")
            self.browse_button.configure(state="disabled")
        else:
            # Change back to standard blue download configuration state
            self.audio_switch.configure(state="normal")
            self.browse_button.configure(state="normal")
            if self.audio_switch_var.get() == "on":
                self.action_button.configure(text="Download MP3 Audio", fg_color=("#3B8ED0", "#1F6AA5"), hover_color=("#367E96", "#144870"))
            else:
                self.action_button.configure(text="Download Highest Quality Video", fg_color=("#3B8ED0", "#1F6AA5"), hover_color=("#367E96", "#144870"))

    def handle_action_click(self):
        """Routing check: Decides whether to start downloading or cancel an active run."""
        if self.is_downloading:
            self.trigger_cancel()
        else:
            self.start_download()

    def update_progress_ui(self, percentage, text_status):
        self.progress_bar.set(percentage)
        self.progress_label.configure(text=text_status, text_color="cyan")

    def check_is_cancelled(self):
        return self.is_cancelled

    def trigger_cancel(self):
        self.is_cancelled = True
        self.status_label.configure(text="Cancelling download request...", text_color="orange")
        self.action_button.configure(state="disabled")

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            self.status_label.configure(text="Error: Please enter a valid URL link.", text_color="red")
            return

        # Initialize background processing states
        self.is_downloading = True
        self.is_cancelled = False
        
        self.status_label.configure(text="")
        self.progress_label.configure(text="Fetching video components...", text_color="cyan")
        self.progress_bar.set(0)
        
        # Transform button look immediately
        self.update_action_button_ui()

        is_audio = self.audio_switch_var.get() == "on"

        download_thread = threading.Thread(target=self.run_download, args=(url, is_audio))
        download_thread.daemon = True 
        download_thread.start()

    def run_download(self, url, is_audio):
        result = download_video(
            url, 
            self.folder_path.get(), 
            audio_only=is_audio, 
            progress_callback=self.update_progress_ui,
            is_cancelled_callback=self.check_is_cancelled
        )

        # UI updates after processing finishes
        if result["success"]:
            self.status_label.configure(text=result["message"], text_color="green")
            self.progress_label.configure(text="Done!", text_color="green")
            self.progress_bar.set(1.0)
            self.url_entry.delete(0, tk.END)
        else:
            self.status_label.configure(text=result["message"], text_color="red")
            if self.is_cancelled:
                self.progress_label.configure(text="Cancelled", text_color="orange")
            else:
                self.progress_label.configure(text="Failed", text_color="red")
            self.progress_bar.set(0)

        # Return UI layout states back to normal entry defaults
        self.is_downloading = False
        self.action_button.configure(state="normal")
        self.update_action_button_ui()

if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()
