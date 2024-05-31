# example from: https://github.com/ytdl-org/youtube-dl/blob/master/README.md#embedding-youtube-dl

from __future__ import unicode_literals
import youtube_dl

# Custom logging functionality
class MyLogger(object):
    def debug(self, msg):
         print('DEBUG:', msg)

    def warning(self, msg):
         print('WARNING:', msg)

    def error(self, msg):
        print('ERROR:', msg)

# required user input

# download dir
download_dir = 'output'
# youtube url
yt_url = 'https://www.youtube.com/watch?v=PjpyvYFSFPs'


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': f'{download_dir}/%(playlist)s/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([yt_url])