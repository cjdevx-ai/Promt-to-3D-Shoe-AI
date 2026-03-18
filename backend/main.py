import os
import time
import requests
import uuid
import shutil
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
# Remove any extra quotes or spaces from the API key
if STABILITY_API_KEY:
    STABILITY_API_KEY = STABILITY_API_KEY.strip().replace('"', '').replace("'", "")

STABILITY_IMAGE_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"
STABILITY_3D_URL = "https://api.stability.ai/v2beta/3d/stable-fast-3d"

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
OUTPUT_DIR = os.path.join(STATIC_DIR, "outputs")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class GenerateRequest(BaseModel):
    prompt: str

# Store task status in memory
tasks = {}

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Stability AI 3D Generation API (Pipeline-style) is running",
        "endpoints": {
            "generate": "/generate (POST)",
            "tasks": "/tasks/{task_id} (GET)",
            "static": "/static"
        }
    }

def process_stability_pipeline(task_id: str, prompt: str, base_url: str):
    try:
        tasks[task_id]["status"] = "GENERATING_IMAGE"
        tasks[task_id]["progress"] = 20
        
        # Step 1: Generate Image using Stable Image Core
        prompt_eng = f"A single high-quality right-foot {prompt}, side view, white background, professional studio lighting, 4k"
        
        headers = {
            "authorization": f"Bearer {STABILITY_API_KEY}",
            "accept": "image/*"
        }
        
        data = {
            "prompt": prompt_eng,
            "output_format": "webp",
        }
        
        # files={"none": ''} is required by Stability's multipart/form-data spec for core
        response = requests.post(STABILITY_IMAGE_URL, headers=headers, files={"none": ''}, data=data)
        
        if response.status_code != 200:
            raise Exception(f"Image generation failed ({response.status_code}): {response.text}")
        
        image_path = os.path.join(OUTPUT_DIR, f"{task_id}.webp")
        with open(image_path, "wb") as f:
            f.write(response.content)
            
        tasks[task_id]["status"] = "CONVERTING_TO_3D"
        tasks[task_id]["progress"] = 60
        
        # Step 2: Convert Image to 3D Model using Stable Fast 3D
        with open(image_path, "rb") as image_file:
            sf3d_response = requests.post(
                STABILITY_3D_URL,
                headers={"authorization": f"Bearer {STABILITY_API_KEY}"},
                files={"image": image_file},
            )

        if sf3d_response.status_code != 200:
            raise Exception(f"3D conversion failed ({sf3d_response.status_code}): {sf3d_response.text}")
            
        glb_filename = f"{task_id}.glb"
        glb_path = os.path.join(OUTPUT_DIR, glb_filename)
        with open(glb_path, "wb") as f:
            f.write(sf3d_response.content)
            
        tasks[task_id].update({
            "status": "SUCCEEDED",
            "progress": 100,
            "model_url": f"{base_url}static/outputs/{glb_filename}",
            "thumbnail_url": f"{base_url}static/outputs/{task_id}.webp"
        })
        print(f"Task {task_id} completed successfully")
        
    except Exception as e:
        print(f"Error processing pipeline {task_id}: {e}")
        tasks[task_id]["status"] = "FAILED"
        tasks[task_id]["progress"] = 0
        tasks[task_id]["error"] = str(e)

@app.post("/generate")
async def generate_3d(request: GenerateRequest, background_tasks: BackgroundTasks, fastapi_request: Request):
    if not STABILITY_API_KEY:
        raise HTTPException(status_code=500, detail="STABILITY_API_KEY not configured in .env")

    # Determine base URL
    base_url = str(fastapi_request.base_url)

    # Create local task
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "PENDING", "progress": 0}
    
    # Add to background tasks
    background_tasks.add_task(process_stability_pipeline, task_id, request.prompt, base_url)
    
    return {"task_id": task_id}

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

if __name__ == "__main__":
    import uvicorn
    print("Starting Stability Pipeline Backend on http://localhost:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001)
