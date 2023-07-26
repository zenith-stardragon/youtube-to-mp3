import streamlit as st
from pytube import YouTube
from moviepy.editor import AudioFileClip
import os
import base64
import re

def convert_and_download(url):
    video = YouTube(url)
    stream = video.streams.get_highest_resolution()
    video_path = stream.download(filename=video.title)
    audio = AudioFileClip(video_path)
    audio_path = video.title + '.mp3'
    audio.write_audiofile(audio_path)
    return audio_path, video.title

def convert_video_and_download(url, resolution):
    video = YouTube(url)
    stream = video.streams.filter(res=resolution, progressive=True).first()
    if not stream:
        raise Exception(f"No stream available with resolution {resolution}")
    video_path = stream.download(filename=video.title)
    return video_path, video.title

def create_download_link(path, filename, extension):  
    with open(path, 'rb') as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/{extension};base64,{b64}" download="{filename}.{extension}">Click Here to Download</a>'
        return href

def is_youtube_url(url):
    youtube_regex = r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
    youtube_regex_match = re.match(youtube_regex, url)
    return bool(youtube_regex_match)

st.title('YouTube Downloader')
url = st.text_input('Enter YouTube Video URL')
resolution = st.selectbox('Select Resolution', ('720p', '480p', '360p', '240p', '144p'))
convert_audio_button = st.button('Convert to MP3')
convert_video_button = st.button('Convert to MP4')

if convert_audio_button or convert_video_button:
    if is_youtube_url(url):
        if convert_audio_button:
            audio_path, title = convert_and_download(url)
            st.markdown(create_download_link(audio_path, title, "mp3"), unsafe_allow_html=True)
        elif convert_video_button:
            video_path, title = convert_video_and_download(url, resolution)
            st.markdown(create_download_link(video_path, title, "mp4"), unsafe_allow_html=True)
    else:
        st.error("Invalid YouTube URL")
