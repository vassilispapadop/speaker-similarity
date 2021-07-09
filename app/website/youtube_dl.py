from __future__ import unicode_literals
import youtube_dl

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'app/website/downloads/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192'
    }],
    'postprocessor_args': [
        '-ar', '16000'
    ],
    'prefer_ffmpeg': True,
    'keepvideo': True
}

def download_audio(file='http://www.youtube.com/watch?v=BaW_jenozKc'):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([file])
