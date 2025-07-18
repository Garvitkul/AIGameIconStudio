# generator.py
import torch
from diffusers import StableDiffusionPipeline, EulerAncestralDiscreteScheduler

# --- CONFIGURATION ---
# This is the exact model ID you chose.
MODEL_ID = "proximasanfinetuning/fantassified_icons_v2"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print("--- Garvit's AI Game Icon Generator ---")
######print(f"Using device: {DEVICE}")

# --- LOAD THE MODEL AND SCHEDULER ---
# This model's creator recommends using the EulerAncestralDiscreteScheduler (Euler a) for best results.
try:
######    print(f"Loading scheduler for {MODEL_ID}...")
    # UPDATED: Changed DDIMScheduler to the recommended EulerAncestralDiscreteScheduler
    scheduler = EulerAncestralDiscreteScheduler.from_pretrained(MODEL_ID, subfolder="scheduler")
    
######    print(f"Loading model pipeline: {MODEL_ID}...")
    # This will download the model (approx. 2-4 GB) the first time it's run.
    pipe = StableDiffusionPipeline.from_pretrained(
        MODEL_ID,
        scheduler=scheduler,
        torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32
    )
    pipe = pipe.to(DEVICE)
######    print("Model loaded successfully.")
    MODEL_LOADED = True
except Exception as e:
    print(f"FATAL: Could not load the model. Error: {e}")
    MODEL_LOADED = False

# --- GENERATION FUNCTION ---
def generate_asset(prompt: str) -> 'Image':
    """
    Takes a text prompt and generates a single image asset. Returns a PIL Image object.
    """
    if not MODEL_LOADED:
        print("Cannot generate, the model failed to load.")
        return None

    # This is the "secret sauce." We add keywords to guide the AI.
    # For this model, simple, direct prompts are best.
    style_keywords = "fantasy icon, game icon, high quality, white background"
    full_prompt = f"{prompt}, {style_keywords}"

    # Things to avoid in the image
    negative_prompt = "text, watermark, characters, people, blurry, low-quality"
    
    print(f"Generating image for prompt: '{full_prompt}'")

    # Generate the image using the pipeline
    image = pipe(
        prompt=full_prompt,
        negative_prompt=negative_prompt,
        # We explicitly set the output image size to be larger.
        width=512,
        height=512,
        # We increase the steps for better detail, as suggested in the handbook.
        num_inference_steps=30, 
        # UPDATED: Changed guidance_scale to align with the model creator's recommendation.
        guidance_scale=7.5
    ).images[0]
    
    print("Image generation complete.")
    return image

# You can test this file directly to see if it works
if __name__ == '__main__':
    print("Running a standalone test...")
    test_prompt = "a crystal dagger"
    generated_image = generate_asset(test_prompt)
    if generated_image:
        # Save the image to a file to see if it worked
        generated_image.save("test_icon.png")
        print("Test successful. Image saved as 'test_icon.png'")
