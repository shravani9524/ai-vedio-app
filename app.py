import streamlit as st
from gtts import gTTS
from moviepy.editor import *
import os
import uuid

st.title("🎬 Script to Video Generator")

# User script input
script = st.text_area("✍️ Enter your script below:", height=200)

# Generate video
if st.button("🎥 Generate Video"):
    if script.strip() == "":
        st.warning("Please enter a script.")
    else:
        # Generate audio from script
        tts = gTTS(script)
        audio_filename = f"audio_{uuid.uuid4().hex}.mp3"
        tts.save(audio_filename)

        # Create blank video (black background, 720p)
        video = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=AudioFileClip(audio_filename).duration)
        video = video.set_audio(AudioFileClip(audio_filename))

        # Output filename
        output_filename = f"video_{uuid.uuid4().hex}.mp4"
        video.write_videofile(output_filename, fps=24)

        # Show video
        st.video(output_filename)

        # Cleanup
        os.remove(audio_filename)
