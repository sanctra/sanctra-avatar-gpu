from fastapi import FastAPI
from pydantic import BaseModel
from server.sadtalker_runner import render_talking_head

app = FastAPI(title="Sanctra Avatar GPU")

class RenderReq(BaseModel):
  image_gcs_uri: str
  audio_gcs_uri: str
  out_gcs_uri: str
  out_res: str = "1080p"
  fps: int = 30

@app.post("/render")
def render(req: RenderReq):
  out_uri = render_talking_head(
    image_gcs_uri=req.image_gcs_uri,
    audio_gcs_uri=req.audio_gcs_uri,
    out_gcs_uri=req.out_gcs_uri,
    out_res=req.out_res,
    fps=req.fps,
  )
  return {"video_gcs_uri": out_uri}
