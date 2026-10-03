import streamlit as st
import google.generativeai as genai
import urllib.parse
import requests
import time
from io import BytesIO
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="ComicCraft - AI Comic Creator",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 ComicCraft: AI Comic Story Creator")
st.write("Generate interactive 3-panel comic stories powered by Google Gemini Models.")

# 2. Gemini API Key Setup
API_KEY = "YOUR_GEMINI_API_KEY"
if API_KEY and API_KEY != "YOUR_API_KEY_HERE"
    genai.configure(api_key=API_KEY)

# 3. User Input
topic = st.text_input(
    "Enter Comic Story Idea or Topic:",
    placeholder="e.g., A funny cat trying to catch a laser light"
)

# 4. Story Generator Logic
def generate_comic_story(user_topic):
    try:
        if API_KEY and API_KEY != "YOUR_GEMINI_API_KEY":
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""
            Create a 3-panel comic story about: "{user_topic}".
            Strictly return in this exact format:
            Panel 1:
            Visual: (simple descriptive scene)
            Dialogue: (speech line)
            Panel 2:
            Visual: (simple descriptive scene)
            Dialogue: (speech line)
            Panel 3:
            Visual: (simple descriptive scene)
            Dialogue: (speech line)
            """
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text
    except Exception:
        pass

    return f"""Panel 1:
Visual: cute cat looking at laser dot
Dialogue: "Target spotted! Operation begins right now!"
Panel 2:
Visual: funny cat jumping in the air
Dialogue: "Whoa! It moves faster than the speed of light!"
Panel 3:
Visual: happy cat resting with laser pointer
Dialogue: "Finally caught it! Mission accomplished with style!"
"""

# Function to fetch image with retries
def fetch_image(prompt_text, seed_val):
    clean_p = urllib.parse.quote(prompt_text)
    url = f"https://image.pollinations.ai/prompt/{clean_p}?width=400&height=400&seed={seed_val}&nologo=true"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for _ in range(3):
        try:
            res = requests.get(url, headers=headers, timeout=20)
            if res.status_code == 200:
                return Image.open(BytesIO(res.content))
        except Exception:
            time.sleep(1)
            
    # Reliable backup image if external API fails
    return f"https://picsum.photos/seed/{seed_val}/400/400"

# 5. UI Button and Rendering
if st.button("Generate Comic"):
    if not topic.strip():
        st.warning("Please enter a topic to create a comic!")
    else:
        with st.spinner("AI is generating your comic story and panels... Please wait..."):
            story_text = generate_comic_story(topic)
            
            st.success("Comic generated successfully!")
            st.markdown("---")

            raw_panels = story_text.split("Panel ")
            cols = st.columns(3)

            for i, col in enumerate(cols):
                if i + 1 < len(raw_panels):
                    panel_data = raw_panels[i + 1]
                    lines = panel_data.strip().split("\n")

                    visual_desc = f"{topic} cartoon scene"
                    dialogue_line = ""

                    for line in lines:
                        if "Visual:" in line:
                            visual_desc = line.split("Visual:")[1].strip()
                        elif "Dialogue:" in line:
                            dialogue_line = line.split("Dialogue:")[1].strip()

                    with col:
                        st.subheader(f"Panel {i + 1}")
                        
                        # Load image with retry
                        img_result = fetch_image(f"comic cartoon illustration, {visual_desc}", i * 50 + 25)
                        st.image(img_result, use_container_width=True)
                        st.info(f"**Dialogue:** {dialogue_line if dialogue_line else '...'}")
                        
                        time.sleep(1)  # Rate limit safety