import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from api.routes import streams, training

app = FastAPI()

app.include_router(streams.router, prefix="/streams", tags=["streams"])
app.include_router(training.router, prefix="/api", tags=["training"])

@app.get("/health")
def read_root():
    return {"status": "ok"}
