# app.py
import streamlit as st
from generator import generate_asset, MODEL_LOADED 
from PIL import Image
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Garvit's AI Icon Studio",
    page_icon="✨",
    layout="centered" 
)

# --- 2. INITIALIZE SESSION STATE ---
# We use session_state to keep track of generated images across reruns.
if 'generated_images' not in st.session_state:
    st.session_state.generated_images = []
# This will hold the single, most recently generated image for prominent display.
if 'latest_image' not in st.session_state:
    st.session_state.latest_image = None
if 'latest_prompt' not in st.session_state:
    st.session_state.latest_prompt = ""


# --- 3. CUSTOM CSS FOR A PREMIUM & MINIMALIST FEEL ---
st.markdown("""
<style>
    /* Core layout and background */
    .stApp {
        background-color: #111111; /* A very dark, near-black background */
        color: #EAEAEA;
    }
    
    /* Main title style */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    /* Subtitle style */
    .sub-title {
        font-size: 1.1rem;
        text-align: center;
        color: #AAAAAA; /* Lighter grey for subtitle */
        margin-bottom: 2rem;
    }

    /* Custom button style */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #8A2BE2, #6A0DAD);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 12px 24px;
        font-size: 1rem;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
        width: 100%;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 20px rgba(138, 43, 226, 0.7);
        transform: translateY(-2px);
    }
    
    /* Container for the prompt input */
    .input-container {
        background-color: #1C1C1C;
        border-radius: 12px;
        padding: 1.5rem 2rem 2rem 2rem;
        border: 1px solid #333333;
    }

    /* Container for the output */
    .output-container {
        background-color: #1C1C1C;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #333333;
        margin-top: 1rem;
    }
    
    /* Hiding the default Streamlit "Made with Streamlit" footer */
    footer {
        visibility: hidden;
    }
            
/* REVISED RULE: This specifically targets the anchor links in your
   custom h1 (with class "main-title") and your h3 headings. */
.main-title a, h3 a {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# --- 4. HEADER ---
st.markdown('<h1 class="main-title">Garvit\'s AI Game Icon Studio</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Your personal artist for fantasy game assets.</p>', unsafe_allow_html=True)

# --- 5. MAIN GENERATION INTERFACE ---
# We wrap the input and button in a st.form. This allows the user to submit
# by pressing 'Enter' in the text field, in addition to clicking the button.
# This improves user experience without changing the layout or style.
with st.container(border=True):
    with st.form(key="icon_generator_form"):
        prompt_input = st.text_input(
            label="Describe the icon you want to create:",
            placeholder="e.g., epic crystal sword, glowing health potion...",
            label_visibility="collapsed"
        )

        # This is now a form_submit_button. It still looks the same due to the CSS.
        # use_container_width=True ensures it spans the full width like before.
        submitted = st.form_submit_button(
            label="✨ Generate Icon",
            use_container_width=True
        )

        # The generation logic now runs only when the form is submitted.
        if submitted:
            if prompt_input:
                if not MODEL_LOADED:
                    st.error("Model is not loaded. Please check the terminal for errors.")
                else:
                    with st.spinner("Conjuring your icon..."):
                        try:
                            generated_image = generate_asset(prompt_input)
                            if generated_image:
                                # Store the latest image for immediate display
                                st.session_state.latest_image = generated_image
                                st.session_state.latest_prompt = prompt_input
                                # Add to the beginning of the gallery list
                                st.session_state.generated_images.insert(0, (prompt_input, generated_image))
                            else:
                                st.error("Image generation failed.")
                        except Exception as e:
                            st.error(f"An unexpected error occurred: {e}")
            else:
                st.warning("Please enter a description to generate an icon.")

# --- 6. LATEST GENERATION OUTPUT ---
# This section provides the immediate feedback the user is looking for.
if st.session_state.latest_image:
    st.markdown('<div class="output-container">', unsafe_allow_html=True)
    st.image(st.session_state.latest_image, caption=st.session_state.latest_prompt, use_container_width=True)
    
    # Save the latest image to a temporary file for download
    image_path = "latest_icon.png"
    st.session_state.latest_image.save(image_path)
    with open(image_path, "rb") as file:
        st.download_button(
            label="Download This Icon",
            data=file,
            file_name=f"{st.session_state.latest_prompt[:20].replace(' ', '_')}_icon.png",
            mime="image/png",
            use_container_width=True
        )
    os.remove(image_path) # Clean up the temp file
    st.markdown('</div>', unsafe_allow_html=True)


# --- 7. GALLERY OF PAST ICONS ---
if st.session_state.generated_images:
    st.divider()
    st.markdown("<h3 style='text-align: center;'>Your Generation History</h3>", unsafe_allow_html=True)
    
    # We only show past generations here, skipping the most recent one which is already displayed above.
    # Display up to the 8 most recent images in the history.
    gallery_images_to_show = st.session_state.generated_images[1:9]
    
    if gallery_images_to_show:
        cols = st.columns(4) 
        for i, (prompt, image) in enumerate(gallery_images_to_show):
            with cols[i % 4]: 
                st.image(image, use_container_width=True, caption=prompt)
    else:
        st.info("Your previously generated icons will appear here.")


# --- 8. FOOTER AND ABOUT SECTION ---
st.divider()
with st.expander("About This Project"):
    st.write("""
        This application is created for the **Zynga AI Hackathon**. 
        
        It uses the `proximasanfinetuning/fantassified_icons_v2` model from Hugging Face, 
        running locally via `PyTorch` and `Diffusers`. The user interface is built with `Streamlit`.
        
        The goal is to provide a tool that accelerates the creative workflow for game designers and artists.
    """)
