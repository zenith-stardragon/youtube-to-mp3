import streamlit as st
from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
import base64

def convert_and_download(url, on_progress):
    video = YouTube(url, on_progress_callback=on_progress)
    stream = video.streams.get_highest_resolution()
    video_path = stream.download(filename=video.title)
    audio = AudioFileClip(video_path)
    audio_path = video.title + '.mp3'
    audio.write_audiofile(audio_path)
    return audio_path

def update_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = bytes_downloaded / total_size  # this is now a fraction from 0.0 to 1.0
    progress_bar.progress(percentage)

def create_download_link(audio_path, filename = "download.mp3"):  
    with open(audio_path, 'rb') as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/mp3;base64,{b64}" download="{filename}">Click Here to Download</a>'
        return href

st.title('YouTube to MP3 Converter')
url = st.text_input('Enter YouTube Video URL')
convert_button = st.button('Convert')
progress_bar = st.progress(0)

if convert_button:
    audio_path = convert_and_download(url, update_progress)
    st.markdown(create_download_link(audio_path), unsafe_allow_html=True)