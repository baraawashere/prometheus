import streamlit as st
from pipeline.script_generator import generate_script
from pipeline.image_generator import generate_all_images
from pipeline.voice_generator import generate_all_audio
from pipeline.video_generator import generate_video

st.set_page_config(page_title="PROMETHEUS", page_icon="🔥", layout="wide")
st.title("🔥 PROMETHEUS")
st.caption("Text → Image → Voice → Video")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")
    
    tab1, tab2, tab3 = st.tabs(["Script", "Visuals", "Voice"])
    
    with tab1:
        num_sections = st.slider("Number of sections", min_value=3, max_value=6, value=4)
        length_mode = st.radio("Script length by", ["Words", "A4 Pages"])
        if length_mode == "Words":
            target_length = st.slider("Target words per section", min_value=50, max_value=200, value=80)
            length_instruction = f"Each section MUST be between {target_length - 25} and {target_length + 25} words."
        else:
            pages = st.slider("Total A4 pages", min_value=1, max_value=5, value=1)
            words_total = pages * 400
            words_per_section = words_total // num_sections
            length_instruction = f"Each section MUST be between {words_per_section - 25} and {words_per_section + 25} words."
        
        tone = st.selectbox("Tone", ["Documentary", "Educational", "Dramatic", "Casual", "Inspirational"])
    
    with tab2:
        image_style = st.selectbox("Image style", [
            "Cinematic documentary",
            "Realistic photograph",
            "Watercolor painting",
            "Digital art",
            "Cartoon illustration"
        ])
        use_music = st.toggle("Enable background music", value=False)
        if use_music:
            uploaded_music = st.file_uploader("Upload an MP3", type=["mp3"])
        else:
            uploaded_music = None
    
    with tab3:
        voice_options = {
            "Aria (Female, US)": "en-US-AriaNeural",
            "Guy (Male, US)": "en-US-GuyNeural",
            "Sonia (Female, UK)": "en-GB-SoniaNeural",
            "Ryan (Male, UK)": "en-GB-RyanNeural",
            "Natasha (Female, AU)": "en-AU-NatashaNeural",
        }
        voice_label = st.selectbox("Voice", options=list(voice_options.keys()))
        voice = voice_options[voice_label]

# --- Main Input ---
topic = st.text_input("Enter a topic", placeholder="e.g. How black holes are formed")

if st.button("Generate", type="primary"):
    if not topic:
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Writing script..."):
            try:
                sections = generate_script(topic, num_sections, length_instruction, tone)
                st.session_state["sections"] = sections
                st.success("Script ready!")
            except Exception as e:
                st.error(f"Something went wrong: {e}")

        if "sections" in st.session_state:
            with st.spinner("Generating images... ⏳"):
                try:
                    image_paths = generate_all_images(st.session_state["sections"], image_style)
                    st.session_state["image_paths"] = image_paths
                    st.success("Images ready!")
                except Exception as e:
                    st.error(f"Image generation failed: {e}")

        if "image_paths" in st.session_state:
            with st.spinner("Generating voiceover... 🎙️"):
                try:
                    audio_paths = generate_all_audio(st.session_state["sections"], voice)
                    st.session_state["audio_paths"] = audio_paths
                    st.success("Voiceover ready!")
                except Exception as e:
                    st.error(f"Audio generation failed: {e}")

        music_path = None
        if use_music:
            if uploaded_music:
                music_path = "outputs/audio/background_music.mp3"
                with open(music_path, "wb") as f:
                    f.write(uploaded_music.getbuffer())
                st.success("Music loaded!")
            else:
                st.warning("No music uploaded, continuing without music.")

        if "audio_paths" in st.session_state:
            with st.spinner("Assembling video... 🎬"):
                try:
                    video_path = generate_video(
                        st.session_state["image_paths"],
                        st.session_state["audio_paths"],
                        music_path
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
        word_count = len(section["narration"].split())
        with st.expander(f"Section {section['section']}: {section['title']} — {word_count} words"):
            st.write(section["narration"])

# --- Display Images ---
if "image_paths" in st.session_state:
    st.divider()
    st.subheader("🎨 Generated Images")
    cols = st.columns(len(st.session_state["image_paths"]))
    for i, path in enumerate(st.session_state["image_paths"]):
        with cols[i]:
            st.image(path, caption=st.session_state["sections"][i]["title"])

# --- Display Audio ---
if "audio_paths" in st.session_state:
    st.divider()
    st.subheader("🎙️ Generated Voiceover")
    for i, path in enumerate(st.session_state["audio_paths"]):
        st.audio(path, format="audio/mp3")

# --- Display Video ---
if "video_path" in st.session_state:
    st.divider()
    st.subheader("🎬 Final Video")
    st.video(st.session_state["video_path"])
    with open(st.session_state["video_path"], "rb") as f:
        st.download_button(
            label="📥 Download Video",
            data=f,
            file_name="prometheus_video.mp4",
            mime="video/mp4"
        )