import os
import time
import requests
import uuid
import shutil
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Enable CORS (still useful for local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
if STABILITY_API_KEY:
    STABILITY_API_KEY = STABILITY_API_KEY.strip().replace('"', '').replace("'", "")

STABILITY_IMAGE_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"
STABILITY_3D_URL = "https://api.stability.ai/v2beta/3d/stable-fast-3d"

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
OUTPUT_DIR = os.path.join(STATIC_DIR, "outputs")
FRONTEND_DIR = os.path.join(STATIC_DIR, "dist") # Where the React build will live

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FRONTEND_DIR, exist_ok=True)

class GenerateRequest(BaseModel):
    prompt: str

# Store task status in memory
tasks = {}

# --- API ENDPOINTS ---

@app.get("/api/health")
async def health():
    return {"status": "online", "message": "ShoeAI API is running"}

def process_stability_pipeline(task_id: str, prompt: str, base_url: str):
    try:
        tasks[task_id]["status"] = "GENERATING_IMAGE"
        tasks[task_id]["progress"] = 20
        
        headers = {"authorization": f"Bearer {STABILITY_API_KEY}", "accept": "image/*"}
        data = {"prompt": f"A single high-quality right-foot {prompt}, side view, white background, professional studio lighting, 4k", "output_format": "webp"}
        
        response = requests.post(STABILITY_IMAGE_URL, headers=headers, files={"none": ''}, data=data)
        if response.status_code != 200:
            raise Exception(f"Image generation failed: {response.text}")
        
        image_path = os.path.join(OUTPUT_DIR, f"{task_id}.webp")
        with open(image_path, "wb") as f:
            f.write(response.content)
            
        tasks[task_id]["status"] = "CONVERTING_TO_3D"
        tasks[task_id]["progress"] = 60
        
        with open(image_path, "rb") as image_file:
            sf3d_response = requests.post(
                STABILITY_3D_URL,
                headers={"authorization": f"Bearer {STABILITY_API_KEY}"},
                files={"image": image_file},
            )

        if sf3d_response.status_code != 200:
            raise Exception(f"3D conversion failed: {sf3d_response.text}")
            
        glb_filename = f"{task_id}.glb"
        glb_path = os.path.join(OUTPUT_DIR, glb_filename)
        with open(glb_path, "wb") as f:
            f.write(sf3d_response.content)
            
        tasks[task_id].update({
            "status": "SUCCEEDED",
            "progress": 100,
            "model_url": f"/static/outputs/{glb_filename}",
            "thumbnail_url": f"/static/outputs/{task_id}.webp"
        })
        
    except Exception as e:
        tasks[task_id].update({"status": "FAILED", "progress": 0, "error": str(e)})

@app.post("/generate")
async def generate_3d(request: GenerateRequest, background_tasks: BackgroundTasks, fastapi_request: Request):
    if not STABILITY_API_KEY:
        raise HTTPException(status_code=500, detail="STABILITY_API_KEY not configured")
    
    base_url = str(fastapi_request.base_url)
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "PENDING", "progress": 0}
    background_tasks.add_task(process_stability_pipeline, task_id, request.prompt, base_url)
    return {"task_id": task_id}

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

# --- STATIC FILE SERVING ---

# Serve generated assets (images and models)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Serve the React Frontend (must be last)
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    file_path = os.path.join(FRONTEND_DIR, full_path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    # Default to index.html for SPA routing
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not found. Did you build it?"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
