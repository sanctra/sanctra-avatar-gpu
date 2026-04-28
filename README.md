# sanctra-avatar-gpu

GPU-accelerated SadTalker REST service for rendering 1080p MP4 replies.
- POST /render with JSON:
  {
    ""session_id"": ""sess_xyz"",
    ""image_gcs_uri"": ""gs://bucket/path/face.jpg"",
    ""audio_gcs_uri"": ""gs://bucket/path/audio.wav"",
    ""fps"": 30,
    ""out_res"": ""1080p""
  }
- The service downloads inputs from GCS, aligns face if needed, caches coefficients,
  runs SadTalker with natural head motion and blinking, uploads:
  gs://avatars-renders/<session_id>/reply.mp4, and returns that GCS URL.

## Quickstart (GPU host)
docker build -f Dockerfile.gpu -t sanctra-avatar-gpu:dev .
docker run --rm --gpus all -p 9100:9100 sanctra-avatar-gpu:dev

## Health
GET /healthz -> 200 ""ok""

## Notes
- Place SadTalker checkpoints under server/models (or mount as a volume).
- For production, use GCS with Workload Identity or a service account key mounted as a secret.
