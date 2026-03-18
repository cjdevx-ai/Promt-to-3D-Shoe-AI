import os
import requests
import shutil
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("STABILITY_API_KEY")
OUTPUT_DIR = "outputs_test"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_pipeline():
    # Clear input buffer and get prompt
    user_prompt = input("Enter shoe description (e.g., 'red sneakers'): ")
    if not user_prompt:
        user_prompt = "futuristic running shoe"
    
    # 1. Generate Image (Pollinations is reliable)
    print("\n--- Step 1: Generating Image via Pollinations.ai ---")
    refined_prompt = f"A single high-quality {user_prompt}, white background, 3D model style, professional photography, studio lighting"
    encoded_prompt = requests.utils.quote(refined_prompt)
    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=42&model=flux"
    
    img_path = os.path.join(OUTPUT_DIR, "input_image.png")
    print(f"Downloading from: {image_url}")
    
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        with open(img_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        print(f"Image saved: {img_path}")
    except Exception as e:
        print(f"Error generating image: {e}")
        return

    # 2. Convert to 3D (Stability AI - Reliable & Fast)
    print("\n--- Step 2: Converting to 3D via Stability AI ---")
    if not API_KEY:
        print("Error: STABILITY_API_KEY not found in .env")
        print("Please ensure .env contains STABILITY_API_KEY='sk-...'")
        return

    # Remove any extra quotes or spaces from the API key
    clean_key = API_KEY.strip().replace('"', '').replace("'", "")
    headers = {"Authorization": f"Bearer {clean_key}"}
    
    try:
        with open(img_path, "rb") as f:
            files = {"image": f}
            data = {
                "texture_resolution": "1024",
                "foreground_ratio": "0.85",
            }

            response = requests.post(
                "https://api.stability.ai/v2beta/3d/stable-fast-3d",
                headers=headers,
                files=files,
                data=data
            )

        if response.status_code == 200:
            glb_path = os.path.join(OUTPUT_DIR, "output_model.glb")
            with open(glb_path, "wb") as f:
                f.write(response.content)
            print(f"SUCCESS! 3D Model saved: {glb_path}")
            
            print("\nOpening results...")
            os.startfile(img_path)
            os.startfile(glb_path)
        else:
            print(f"Stability AI Error ({response.status_code})")
            print(f"Response: {response.text}")
            if "invalid_api_key" in response.text.lower():
                print("\nTIP: Check your STABILITY_API_KEY in .env. It should look like 'sk-...'")
    except Exception as e:
        print(f"Error during 3D generation: {e}")

if __name__ == "__main__":
    run_pipeline()
