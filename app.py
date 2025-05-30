import streamlit as st
from gtts import gTTS
from moviepy.editor import *
import tempfile
import os

st.title("🎬 AI Script to Video Generator")

script = st.text_area("✍️ Enter your script here:")

if st.button("🎥 Generate Video"):
    if not script.strip():
        st.error("Please enter a script.")
    else:
        with st.spinner("Generating audio..."):
            tts = gTTS(text=script, lang='en')
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp_audio.name)

        with st.spinner("Creating video..."):
            audioclip = AudioFileClip(temp_audio.name)
            txtclip = TextClip(script, fontsize=24, color='white', size=(720, 480), method='caption')
            txtclip = txtclip.set_duration(audioclip.duration).set_audio(audioclip)

            temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            txtclip.write_videofile(temp_video.name, fps=24)

        st.success("✅ Video created!")
        st.video(temp_video.name)

        os.remove(temp_audio.name)
        os.remove(temp_video.name)
