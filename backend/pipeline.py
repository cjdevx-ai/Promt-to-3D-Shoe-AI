import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("STABILITY_API_KEY")

if not API_KEY:
    print("Error: STABILITY_API_KEY not found in environment or .env file.")
    exit(1)

user_prompt = input('Enter prompt: ')

# Refine prompt for better results
prompt_eng = f"A single high-quality right-foot {user_prompt}, side view, white background, professional studio lighting, 4k"

print(f"Generating image for prompt: {prompt_eng}")

# Step 1: Generate Image using Stable Image Core
# Note: The 'files' parameter should not be empty if using multipart/form-data with requests for some endpoints, 
# but for Stability 'none' is a specific way they sometimes show in docs, let's use data for everything if possible 
# or follow their latest spec.
response = requests.post(
    "https://api.stability.ai/v2beta/stable-image/generate/core",
    headers={
        "authorization": f"Bearer {API_KEY}",
        "accept": "image/*"
    },
    files={"none": ''},
    data={
        "prompt": prompt_eng,
        "output_format": "webp",
    },
)

# Check if request was successful
if response.status_code == 200:
    image_path = "image.webp"
    with open(image_path, "wb") as file:
        file.write(response.content)
    print(f"Image generated successfully: {image_path}")
else:
    print(f"Error generating image: {response.status_code}")
    print(response.text)
    exit(1)

# Step 2: Convert Image to 3D Model using Stable Fast 3D
print("Converting image to 3D model...")
try:
    with open(image_path, "rb") as image_file:
        sf3d_response = requests.post(
            "https://api.stability.ai/v2beta/3d/stable-fast-3d",
            headers={
                "authorization": f"Bearer {API_KEY}",
                # The 3D API returns the file directly as content
            },
            files={"image": image_file},
        )

    if sf3d_response.status_code == 200:
        glb_path = "shoe.glb"
        with open(glb_path, "wb") as file:
            file.write(sf3d_response.content)
        print(f"3D model generated successfully: {glb_path}")
    else:
        print(f"Error generating 3D model: {sf3d_response.status_code}")
        print(sf3d_response.text)
        exit(1)

except FileNotFoundError:
    print(f"Error: {image_path} not found.")
    exit(1)

# Step 3: Open the results
if os.path.exists(image_path):
    print(f"Opening image: {image_path}")
    os.startfile(image_path)

if os.path.exists(glb_path):
    print(f"Opening 3D model: {glb_path}")
    os.startfile(glb_path)
