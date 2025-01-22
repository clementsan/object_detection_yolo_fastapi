"""
FastAPI module
"""

from contextlib import asynccontextmanager
from typing import Optional
from mangum import Mangum
from fastapi import FastAPI, File, UploadFile, Query, HTTPException
from .detection import ml_detection, ml_utils


def detection_pipeline(yolo_model: object, image_bytes: bytes) -> str:
    """detection pipeline: load ML model, perform object detection and return json object"""

    # Object detection
    results = ml_detection.object_detection(yolo_model, image_bytes)

    # Convert dictionary to JSON
    result_json = ml_utils.convert_dict_to_json(results)

    return result_json


# Example with global variable as dict
# ml_yolo = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan - startup and shutdown logic
      - Load ML model at startup
    """

    # Load the ML model
    # ml_yolo = ml_detection.load_model()
    app.model_nano = ml_detection.load_model("yolo11n")
    app.model_small = ml_detection.load_model("yolo11s")

    yield
    # Clean up the ML model and release the resources
    del app.model_nano
    del app.model_small
    # ml_yolo.clear()


app = FastAPI(
    lifespan=lifespan,
    title="Object detection",
    description="Object detection on COCO dataset",
    version="1.0",
)
handler = Mangum(app)


@app.get("/")
def home():
    """Home function - return welcome message"""
    return {"message": "Welcome to the object detection API - use of Ultralytics YOLO"}


@app.get("/status")
def status():
    """Status function: return api status"""
    return {"status": "ok"}


@app.get("/info")
def info():
    """Info function: return info as json dict"""
    return {
        "name": "object-detection",
        "description": "object detection via YOLO model on COCO dataset",
    }


# Detection with optional model type
@app.post("/api/v1/detect")
async def detect(image: UploadFile = File(...), model: Optional[str] = Query(None)) -> str:
    """Detect function - run object detection task and return prediction"""

    # Read the image file
    image_bytes = await image.read()

    print("API ML model: ", model)

    # ML detection
    if (model is None) or (model == "yolo11n"):
        output_json = detection_pipeline(app.model_nano, image_bytes)  # pylint: disable=no-member
    elif model == "yolo11s":
        output_json = detection_pipeline(app.model_small, image_bytes)  # pylint: disable=no-member
    else:
        raise HTTPException(status_code=400, detail="Incorrect model type")
    return output_json
