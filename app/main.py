from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from app.api.game_comparison import router as game_comparison_router

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

# Include the game_comparison_router for the new game comparison API endpoints
app.include_router(game_comparison_router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "app_name": "DRM-Free Game Comparison Tool", 
        "app_version": "1.0.0"
    })
