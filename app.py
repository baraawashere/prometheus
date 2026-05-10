import streamlit as st
import json
from pipeline.script_generator import generate_script
from pipeline.image_generator import generate_all_images
from pipeline.voice_generator import generate_all_audio
from pipeline.video_generator import generate_video

st.set_page_config(page_title="PROMETHEUS", page_icon="🔥", layout="wide")

st.title("🔥 PROMETHEUS")
st.caption("Text → Image → Voice → Video")

# --- Sidebar ---
with st.sidebar:
    st.header("Settings")
    num_sections = st.slider("Number of sections", min_value=3, max_value=6, value=4)
    length_mode = st.radio("Script length by", ["Words", "A4 Pages"])
    if length_mode == "Words":
        target_length = st.slider("Target words per section", min_value=50, max_value=200, value=80)
        length_instruction = f"Each section MUST be Exactly {target_length} words."
    else:
        pages = st.slider("Total A4 pages", min_value=1, max_value=5, value=1)
        words_total = pages * 250
        words_per_section = words_total // num_sections
        length_instruction = (
            f"Each section MUST be between {words_per_section - 25} and {words_per_section + 25} words. "
            f"Total script target is {words_total} words."
        )

# --- Main Input ---
topic = st.text_input("Enter a topic", placeholder="e.g. How black holes are formed")

if st.button("Generate Script", type="primary"):
    if not topic:
        st.warning("Please enter a topic first.")
    else:
        # Step 1: Generate script
        with st.spinner("Writing script..."):
            try:
                sections = generate_script(topic, num_sections, length_instruction)
                st.session_state["sections"] = sections
                st.success("Script ready!")
            except Exception as e:
                st.error(f"Something went wrong: {e}")

        # Step 2: Only continue if script exists
        if "sections" in st.session_state:
            with st.spinner("Generating images... this may take a minute ⏳"):
                try:
                    image_paths = generate_all_images(st.session_state["sections"])
                    st.session_state["image_paths"] = image_paths
                    st.success("Images ready!")
                except Exception as e:
                    st.error(f"Image generation failed: {e}")

            with st.spinner("Generating voiceover... 🎙️"):
                try:
                    audio_paths = generate_all_audio(st.session_state["sections"])
                    st.session_state["audio_paths"] = audio_paths
                    st.success("Voiceover ready!")
                except Exception as e:
                    st.error(f"Audio generation failed: {e}")
            with st.spinner("Assembling video... 🎬"):
                try:
                    video_path = generate_video(
                        st.session_state["image_paths"],
                        st.session_state["audio_paths"]
                    )
                    st.session_state["video_path"] = video_path
                    st.success("Video ready!")
                except Exception as e:
                    st.error(f"Video generation failed: {e}")
                

# --- Display Script ---
if "sections" in st.session_state:
    st.divider()
    st.subheader("📄 Generated Script")

    for section in st.session_state["sections"]:
        with st.expander(f"Section {section['section']}: {section['title']}"):
            st.write(section["narration"])

if "image_paths" in st.session_state:
    st.divider()
    st.subheader("🎨 Generated Images")
    cols = st.columns(len(st.session_state["image_paths"]))
    for i, path in enumerate(st.session_state["image_paths"]):
        with cols[i]:
            st.image(path, caption=st.session_state["sections"][i]["title"])

if "audio_paths" in st.session_state:
    st.divider()
    st.subheader("🎙️ Generated Voiceover")
    for i, path in enumerate(st.session_state["audio_paths"]):
        st.audio(path, format="audio/mp3")
if "video_path" in st.session_state:
    st.divider()
    st.subheader("🎬 Final Video")
    st.video(st.session_state["video_path"])