"""OCR and image preprocessing services."""
import os
import cv2
import numpy as np
from backend.model_loader import load_ocr_model


def preprocess_image(image_path):
    """Preprocess image for better OCR results."""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image at path: {image_path}")
    
    # Resize
    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    
    # CLAHE enhancement
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    enhanced_lab = cv2.merge((cl, a, b))
    enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    
    # Bilateral filter
    filtered = cv2.bilateralFilter(enhanced, d=9, sigmaColor=75, sigmaSpace=75)
    
    # Sharpen
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(filtered, -1, kernel)
    
    # Save preprocessed image
    output_path = "temp_preprocessed_image.jpg"
    cv2.imwrite(output_path, sharpened)
    return output_path


def extract_text_from_image(image_path):
    """Extract text from image using OCR."""
    ocr = load_ocr_model()
    processed_path = preprocess_image(image_path)
    result = ocr.predict(processed_path)
    
    extracted_text = ""
    if result and isinstance(result, list) and "rec_texts" in result[0]:
        extracted_text = " ".join(result[0]["rec_texts"])
    
    # Cleanup
    if os.path.exists(processed_path):
        os.remove(processed_path)
    
    return extracted_text