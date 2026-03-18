# ShoeAI: Prompt to 3D Generation System

ShoeAI is a high-fidelity 3D generative system designed specifically for footwear. It transforms simple text descriptions into detailed, interactive 3D shoe models (.glb) using an optimized pipeline combining the latest Stability AI and Pollinations.ai generative models.

## Architecture

The system consists of three main parts:
- **Backend (FastAPI)**: A Python-based server that manages the generation pipeline, handles background tasks, and provides a REST API for the frontend.
- **AI Pipeline**:
  - Image Generation: Stable Image Core (via Stability AI API) or Pollinations.ai (FLUX) to create high-quality, professional shoe imagery.
  - 3D Conversion: Stable Fast 3D API for rapid mesh generation and PBR texturing.
- **Frontend (React + TypeScript)**: A modern, glassmorphic interface featuring a 3D interactive background (Tubes Cursor) and a real-time generation dashboard.

## Key Features

- **Prompt-to-3D**: Convert any creative footwear concept into a textured 3D mesh.
- **Interactive Previews**: Rotate, zoom, and inspect generated models directly in the browser using @google/model-viewer.
- **Glassmorphic UI**: High-end aesthetic with translucent surfaces and cinematic animations.
- **Performance Optimized**: Models are generated in under 60 seconds.
- **Production Ready**: Exports standard .glb files compatible with Blender, Unity, Unreal Engine, and WebGL.

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Stability AI API Key (Required for high-quality 3D generation)

## Installation and Setup

### 1. Backend Setup
Navigate to the backend directory and set up the Python environment:
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:
```env
STABILITY_API_KEY=your_api_key_here
```

Start the backend server:
```bash
python main.py
```
The server will run on http://localhost:8001.

### 2. Frontend Setup
Navigate to the frontend directory and install dependencies:
```bash
cd frontend
npm install
```

Start the development server:
```bash
npm run dev
```
The frontend will be available at http://localhost:5173.

## API Documentation

- **POST /generate**: Submit a prompt for 3D generation. Returns a task_id.
- **GET /tasks/{task_id}**: Check the status and retrieve links to the generated image and 3D model.
- **GET /static/outputs/**: Direct access to generated assets.

## Acknowledgments

- Generative models provided by Stability AI.
- Interactive background based on Threejs-components.
- 3D rendering powered by @google/model-viewer.
