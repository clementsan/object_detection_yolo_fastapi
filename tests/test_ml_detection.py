from app.detection import ml_detection
import os
import pytest


# Test model loading
@pytest.mark.parametrize("test_model_uri",[
    ("yolo11n"),
    ("yolo11s"),
])
def test_load_model(test_model_uri):
    model = ml_detection.load_model(test_model_uri)
    assert model is not None


# Test image detection
@pytest.mark.parametrize("test_model_uri", [
    ("yolo11n"),
    ("yolo11s"),
])
def test_object_detection(test_model_uri):
    model = ml_detection.load_model(test_model_uri)

    # Get the directory of the current test file
    test_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the image path relative to the test directory
    image_path = os.path.join(test_dir, 'data', 'savanna.jpg')

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    results = ml_detection.object_detection(model, image_bytes)
    assert results is not None
    assert isinstance(results, dict)
