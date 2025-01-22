"""
Object Detection module
"""

import io
from typing import Dict, Any
from ultralytics import YOLO
from PIL import Image


def load_model(model_uri: str):
    """Load YOLO  model"""

    model = YOLO(model_uri)
    return model


def object_detection(
    model: object,
    image_bytes: bytes,
    conf_threshold: float = 0.25,
    iou_threshold: float = 0.45,
) -> Dict[str, Any]:
    """Perform object detection task"""

    print("Object detection...")
    # url = "http://images.cocodataset.org/val2017/000000039769.jpg"
    # image = Image.open(requests.get(url, stream=True).raw)

    img = Image.open(io.BytesIO(image_bytes))
    # print('inputs', inputs)
    results = model.predict(
        source=img,
        conf=conf_threshold,
        iou=iou_threshold,
        show_labels=True,
        show_conf=True,
        imgsz=320,
    )

    # Detection bounding boxes - ultralytics object with attributes
    boxes = results[0].boxes.cpu().numpy()

    # Generate dictionary object as prediction response
    scores = boxes.conf.tolist()
    boxes_xyxy = boxes.xyxy.tolist()
    labels = [int(x) for x in boxes.cls]

    prediction = {
        "scores": scores,
        "boxes": boxes_xyxy,
        "labels": labels,
    }

    return prediction
