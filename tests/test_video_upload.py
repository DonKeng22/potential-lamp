import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Use SQLite database for tests
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

# Ensure backend is importable
backend_path = Path(__file__).parent.parent / "platform" / "backend"
sys.path.append(str(backend_path))

from main import app  # noqa: E402


def test_video_upload():
    client = TestClient(app)
    video_path = Path(__file__).parent.parent / "dummy_video.mp4"
    with video_path.open("rb") as file:
        response = client.post(
            "/api/v1/videos/upload",
            files={"file": ("dummy_video.mp4", file, "video/mp4")},
        )
    assert response.status_code == 200
    data = response.json()
    for field in ["id", "filename", "status", "message"]:
        assert field in data


def test_video_upload_invalid_extension(tmp_path):
    client = TestClient(app)
    tmp_file = tmp_path / "sample.txt"
    tmp_file.write_bytes(b"not a video")
    with tmp_file.open("rb") as file:
        response = client.post(
            "/api/v1/videos/upload",
            files={"file": ("sample.txt", file, "video/mp4")},
        )
    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported video file extension"
