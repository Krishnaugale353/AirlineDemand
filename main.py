from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from ui import create_dashboard
import gradio as gr
app = FastAPI(title="Airline Market Demand Dashboard")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "airline-demand-dashboard"}

# Mount Gradio app
demo = create_dashboard()
app = gr.mount_gradio_app(app, demo, path="/")