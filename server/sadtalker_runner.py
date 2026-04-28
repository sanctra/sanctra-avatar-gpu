import os, tempfile, subprocess
from urllib.parse import urlparse
from google.cloud import storage

# server/main.py
from fastapi import FastAPI
from .sadtalker_runner import render_talking_head

app = FastAPI()

@app.get("/healthz")
async def healthz():
    return "ok"


RES_MAP = {"720p": (1280,720), "1080p": (1920,1080)}
_bucket_client = storage.Client()

def _gcs_to_bucket_blob(gcs_uri: str):
  assert gcs_uri.startswith("gs://")
  parsed = urlparse(gcs_uri.replace("gs://","//"))
  return parsed.netloc, parsed.path.lstrip("/")

def _download(gcs_uri: str, dst: str):
  bkt, key = _gcs_to_bucket_blob(gcs_uri)
  bucket = _bucket_client.bucket(bkt)
  bucket.blob(key).download_to_filename(dst)

def _upload(src: str, gcs_uri: str):
  bkt, key = _gcs_to_bucket_blob(gcs_uri)
  bucket = _bucket_client.bucket(bkt)
  bucket.blob(key).upload_from_filename(src, content_type="video/mp4")
  return gcs_uri

def render_talking_head(image_gcs_uri: str, audio_gcs_uri: str, out_gcs_uri: str, out_res: str="1080p", fps: int=30) -> str:
  W,H = RES_MAP.get(out_res, RES_MAP["1080p"])
  with tempfile.TemporaryDirectory() as td:
    img = os.path.join(td, "ref.jpg")
    wav = os.path.join(td, "speech.wav")
    mp4 = os.path.join(td, "out.mp4")
    _download(image_gcs_uri, img)
    _download(audio_gcs_uri, wav)

    # TODO: replace placeholder ffmpeg image+audio mux with SadTalker CLI invocation
    # Example When integrated:
    # subprocess.run(["python","inference.py","--driven_audio",wav,"--source_image",img,"--result_dir",td,"--fps",str(fps)], check=True)
    # Assume output to mp4
    subprocess.run([
      "ffmpeg","-y",
      "-loop","1","-i", img,
      "-i", wav,
      "-c:v","libx264","-tune","stillimage","-vf",f"scale={W}:{H}",
      "-c:a","aac","-b:a","192k","-shortest","-r",str(fps),
      mp4
    ], check=True)

    return _upload(mp4, out_gcs_uri)
