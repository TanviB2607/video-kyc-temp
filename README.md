# video_kyc_app

AI-powered Video KYC (Know Your Customer) Verification System

## Features
- Modular Flask application for KYC verification
- Upload video and ID document (Aadhaar/PAN)
- Keyframe extraction (OpenCV)
- Face detection (YOLOv8)
- Face matching (DeepFace ArcFace)
- Passive & active liveness detection
- Document detection & cropping (YOLO)
- OCR text extraction (Tesseract/PaddleOCR)
- Decision engine with thresholds
- Structured JSON output

## Setup Instructions

1. **Clone or download this repo**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Flask app:**
   ```bash
   python app.py
   ```
4. **Open in browser:**
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Folder Structure
```
video_kyc_app/
├── app.py
├── requirements.txt
├── /models
├── /services
│   ├── face_match_service.py
│   ├── liveness_service.py
│   ├── document_service.py
│   └── decision_engine.py
├── /utils
│   ├── video_utils.py
│   ├── image_utils.py
│   ├── ocr_utils.py
│   └── score_utils.py
├── /static/uploads
├── /templates
│   └── upload.html
└── README.md
```

## Demo
- Upload your ID and video via the web form
- See the decision output (APPROVED/REVIEW/REJECTED)

## Notes
- Pretrained models (YOLO, DeepFace) should be placed in `/models`
- For production, add proper error handling, logging, and security
