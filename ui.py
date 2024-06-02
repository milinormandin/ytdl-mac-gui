import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import sv_ttk
import threading
import time
from ytdl_lib import download_yt_to_audio



# # Mock download function (to be replaced with actual download logic)
# def download_youtube_video(youtube_url, destination_folder, status_label):
#     # Simulate a download process
#     status_label.config(text="Downloading...")
#     time.sleep(5)  # Simulating download delay
#     downloaded_file_path = f"{destination_folder}/downloaded_video.mp4"
#     status_label.config(text=f"Download completed: {downloaded_file_path}")

def init_download(youtube_url_entry, destination_folder_entry, loggerInstance, hookFn):
    youtube_url = youtube_url_entry.get()
    destination_folder = destination_folder_entry.get()
    
    # Input validation
    if not youtube_url:
        messagebox.showwarning("Input Error", "Please paste a YouTube URL.")
        return
    if not destination_folder:
        messagebox.showwarning("Input Error", "Please select a destination folder.")
        return
    
    # Pause fn to not look like a bot to youtube
    time.sleep(.5)
    # Start the download in a separate thread to avoid blocking the UI
    threading.Thread(target=download_yt_to_audio, args=(destination_folder, youtube_url, loggerInstance, hookFn)).start()

def browse_destination_folder(destination_folder_entry):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        destination_folder_entry.delete(0, tk.END)
        destination_folder_entry.insert(0, folder_selected)

def create_gui():
    root = tk.Tk()
    root.title("YouTube Video Downloader")

    
    # Custom logging functionality for ytdl progress
    class MyLogger(object):
        def debug(self, msg):
            status_label.config(text=f'DEBUG: {msg}')
            #  print('DEBUG:', msg)

        def warning(self, msg):
            # print('WARNING:', msg)
            status_label.config(text=f'WARNING: {msg}')

        def error(self, msg):
            # print('ERROR:', msg)
            status_label.config(text=f'ERROR: {msg}')
    
    def my_hook(d):
        if d['status'] == 'downloading':
            status_label.config(text=f'downloading...')
            filename = d['filename']
            total_bytes = int(d['total_bytes'])
            print(total_bytes)
            downloaded_bytes = int(d['downloaded_bytes'])
            if total_bytes:
                # Set the maximum value for the progress bar.
                progressbar.configure(maximum=total_bytes)
            else:
                # Increase the progress.
                progressbar.step(downloaded_bytes)
            
            progressbar.config()
        if d['status'] == 'finished':
            status_label.config(text=f'Download finished ✅')
    
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
    download_button = ttk.Button(root, text="Download", command=lambda: init_download(youtube_url_entry, destination_folder_entry, MyLogger(), my_hook))
    download_button.grid(row=2, column=0, columnspan=3, padx=10, pady=20)

    # TODO: add cancel button to kill thread: https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/#

    # Add progress bar
    progressbar = ttk.Progressbar()
    progressbar.grid(row=3, column=0, columnspan=3, padx=10, pady=20)
    
    # Status area
    status_frame = tk.LabelFrame(root, text="Status", padx=10, pady=10)
    status_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
    status_label = ttk.Label(status_frame, text="", anchor="w")
    status_label.pack(fill="both")

    # Set custom theme: https://github.com/rdbende/Sun-Valley-ttk-theme
    sv_ttk.set_theme("dark")

    root.mainloop()

if __name__ == "__main__":
    create_gui()
