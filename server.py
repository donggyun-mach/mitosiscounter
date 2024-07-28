from flask import Flask, request, jsonify
import cv2
import numpy as np
# Import necessary YOLOv3 modules
from darknet import Darknet

# Configure Flask app
app = Flask(__name__)

# Load YOLOv3 model (replace with your model path and class names)
yolo = Darknet("path/to/yolov3.cfg", "path/to/yolov3.weights", "path/to/yolov3.data")
class_names = yolo.class_names

# Function to process ROI image and detect mitosis regions
def process_roi(roi_image):
    # Preprocess ROI image (resize, normalize, etc.)
    roi_image = cv2.resize(roi_image, (416, 416))  # Assuming YOLOv3 expects 416x416
    roi_image = roi_image.astype(np.float32) / 255.0
    roi_image = np.expand_dims(roi_image, axis=0)

    # Run YOLOv3 detection
    results = yolo.detect(roi_image)

    # Process detections: filter mitosis boxes and classify them
    mitosis_boxes = []
    for det in results:
        if det[0] in class_names and "mitosis" in det[0]:  # Filter for mitosis class
            x1, y1, x2, y2, conf, cls_id = det
            mitosis_boxes.append({
                "x1": int(x1),
                "y1": int(y1),
                "x2": int(x2),
                "y2": int(y2),
                "confidence": float(conf),
                "class": cls_id,
                "classification": "equivocal"  # Initial classification
            })

    # Implement your custom logic for "yes/no" classification based on confidence, heuristics, or additional models
    # ... (replace with your classification logic)

    return mitosis_boxes

# Flask route for processing ROI image
@app.route("/process_roi", methods=["POST"])
def process_roi_endpoint():
    # Retrieve ROI image data from request
    try:
        roi_data = request.get_data()
        roi_image = cv2.imdecode(np.fromstring(roi_data, np.uint8), cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"Error reading ROI image: {e}")
        return jsonify({"error": "Failed to read ROI image"}), 400

    # Process ROI image and get mitosis boxes
    mitosis_boxes = process_roi(roi_image)

    # Return JSON response with mitosis boxes and classifications
    return jsonify({"mitosis_boxes": mitosis_boxes})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
