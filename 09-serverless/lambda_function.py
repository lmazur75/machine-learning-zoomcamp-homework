import os
import numpy as np
import onnxruntime as ort
from io import BytesIO
from urllib import request
from PIL import Image

# Initialize the model once (outside the handler for reuse)
model_name = os.getenv("MODEL_NAME", "hair_classifier_empty.onnx")
session = ort.InferenceSession(
    model_name, providers=["CPUExecutionProvider"]
)
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name


def download_image(url):
    """Download image from URL"""
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img


def prepare_image(img, target_size=(200, 200)):
    """Prepare image: convert to RGB and resize"""
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img


def preprocess_image(img):
    """Preprocess image for model inference"""
    # Convert to numpy array with float32
    img_array = np.array(img, dtype=np.float32)
    
    # Scale to [0, 1]
    img_array = img_array / 255.0
    
    # Apply ImageNet normalization
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    img_array = (img_array - mean) / std
    
    # Transpose to (C, H, W) format and add batch dimension
    img_array = img_array.transpose(2, 0, 1)  # (H, W, C) -> (C, H, W)
    img_array = np.expand_dims(img_array, axis=0)  # -> (1, C, H, W)
    
    return img_array


def predict(url):
    """Main prediction function"""
    # Download and prepare image
    img = download_image(url)
    img = prepare_image(img, target_size=(200, 200))
    
    # Preprocess image
    img_array = preprocess_image(img)
    
    # Run inference
    outputs = session.run(None, {input_name: img_array})
    
    # Apply sigmoid to get probability
    logit = outputs[0][0][0]
    #probability = 1 / (1 + np.exp(-logit))
    
    #return float(probability)
    return float(logit)


def lambda_handler(event, context):
    """AWS Lambda handler function"""
    url = event['url']
    #probability = predict(url)
    prediction = predict(url)
    
    result = {
        #'prediction': probability
        'prediction': prediction
    }
    
    return result
