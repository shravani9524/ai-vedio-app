import streamlit as st
from gtts import gTTS
from moviepy.editor import AudioFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from PIL import Image
import os
import uuid

st.title("🎬 Script to Video (Voice Only)")

script = st.text_area("✍️ Enter your script here:")

if st.button("🎥 Generate Video"):
    if not script.strip():
        st.error("Please enter a script.")
    else:
        try:
            st.info("Generating voice from text...")
            # Save voice from script
            audio_path = f"audio_{uuid.uuid4().hex}.mp3"
            tts = gTTS(text=script, lang='en')
            tts.save(audio_path)

            st.info("Combining into video...")
            # Use a placeholder image to create a video with audio
            image_path = "placeholder.jpg"
            if not os.path.exists(image_path):
                Image.new('RGB', (1280, 720), color=(0, 0, 0)).save(image_path)

            video_output = f"output_{uuid.uuid4().hex}.mp4"
            os.system(f"ffmpeg -loop 1 -i {image_path} -i {audio_path} -shortest -c:v libx264 -c:a aac -strict experimental -b:a 192k -pix_fmt yuv420p -vf scale=1280:720 {video_output}")

            st.success("✅ Video created!")
            st.video(video_output)

            # Cleanup
            os.remove(audio_path)
            os.remove(video_output)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
