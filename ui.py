import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import sv_ttk
import threading
import time

# Mock download function (to be replaced with actual download logic)
def download_youtube_video(youtube_url, destination_folder, status_label):
    # Simulate a download process
    status_label.config(text="Downloading...")
    time.sleep(5)  # Simulating download delay
    downloaded_file_path = f"{destination_folder}/downloaded_video.mp4"
    status_label.config(text=f"Download completed: {downloaded_file_path}")

def init_download(youtube_url_entry, destination_folder_entry, status_label):
    youtube_url = youtube_url_entry.get()
    destination_folder = destination_folder_entry.get()
    
    # Input validation
    if not youtube_url:
        messagebox.showwarning("Input Error", "Please paste a YouTube URL.")
        return
    if not destination_folder:
        messagebox.showwarning("Input Error", "Please select a destination folder.")
        return

    # Start the download in a separate thread to avoid blocking the UI
    threading.Thread(target=download_youtube_video, args=(youtube_url, destination_folder, status_label)).start()

def browse_destination_folder(destination_folder_entry):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        destination_folder_entry.delete(0, tk.END)
        destination_folder_entry.insert(0, folder_selected)

def create_gui():
    root = tk.Tk()
    root.title("YouTube Video Downloader")

    
    # YouTube URL input
    ttk.Label(root, text="Paste YouTube URL here:").grid(row=0, column=0, padx=10, pady=20, sticky=tk.W)
    youtube_url_entry = ttk.Entry(root, width=50)
    youtube_url_entry.grid(row=0, column=1, padx=10, pady=20)

    # Destination folder input
    ttk.Label(root, text="Select destination folder:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    destination_folder_entry = ttk.Entry(root, width=50)
    destination_folder_entry.grid(row=1, column=1, padx=10, pady=5)
    browse_button = ttk.Button(root, text="Browse", command=lambda: browse_destination_folder(destination_folder_entry))
    browse_button.grid(row=1, column=2, padx=10, pady=5)

    # Download button
    download_button = ttk.Button(root, text="Download", command=lambda: init_download(youtube_url_entry, destination_folder_entry, status_label))
    download_button.grid(row=2, column=0, columnspan=3, padx=10, pady=20)

    # Status area
    status_frame = tk.LabelFrame(root, text="Status", padx=10, pady=10)
    status_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
    status_label = ttk.Label(status_frame, text="", anchor="w")
    status_label.pack(fill="both")

    # Set custom theme: https://github.com/rdbende/Sun-Valley-ttk-theme
    sv_ttk.set_theme("dark")

    root.mainloop()

if __name__ == "__main__":
    create_gui()
