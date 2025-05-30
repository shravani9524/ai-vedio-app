import streamlit as st
from gtts import gTTS
import os
import uuid
import shutil

st.title("🎬 AI Script-to-Video Generator with Background and Subtitles")

# Choose background by keyword
def select_background_video(script):
    script = script.lower()
    if "nature" in script:
        return "videos/nature.mp4"
    elif "finance" in script or "money" in script:
        return "videos/finance.mp4"
    elif "education" in script or "study" in script:
        return "videos/education.mp4"
    else:
        return "videos/default.mp4"

# User input
script = st.text_area("✍️ Enter your script:", height=200)

if st.button("🎥 Generate Video"):
    if not script.strip():
        st.warning("Please enter a script.")
    else:
        try:
            st.info("🔊 Converting script to voice...")
            audio_path = f"audio_{uuid.uuid4().hex}.mp3"
            tts = gTTS(text=script, lang='en')
            tts.save(audio_path)

            st.info("🎞️ Selecting background video...")
            bg_video = select_background_video(script)

            output_path = f"video_{uuid.uuid4().hex}.mp4"
            subtitle_path = f"subtitle_{uuid.uuid4().hex}.srt"

            # Generate subtitle file
            with open(subtitle_path, "w") as srt:
                srt.write("1\n00:00:00,000 --> 00:00:10,000\n")
                srt.write(script)

            st.info("🎬 Creating final video...")
            ffmpeg_cmd = f"""
            ffmpeg -y -i "{bg_video}" -i "{audio_path}" -vf "subtitles={subtitle_path}" \
            -shortest -c:v libx264 -c:a aac -strict experimental "{output_path}"
            """
            os.system(ffmpeg_cmd)

            st.success("✅ Video created!")
            st.video(output_path)

            with open(output_path, "rb") as video_file:
                st.download_button("📥 Download Video", data=video_file, file_name="my_video.mp4")

            # Cleanup
            os.remove(audio_path)
            os.remove(output_path)
            os.remove(subtitle_path)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
