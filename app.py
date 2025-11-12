from flask import Flask, request, render_template, jsonify
from services.face_match_service import FaceMatchService
from services.liveness_service import LivenessService, capture_challenge_frames
from services.document_service import DocumentService
from services.decision_engine import DecisionEngine
import os
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/', methods=['GET'])
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Handle file uploads
    id_doc = request.files.get('id_doc')
    saved_files = []
    if id_doc:
        id_doc_path = os.path.join(app.config['UPLOAD_FOLDER'], id_doc.filename)
        id_doc.save(id_doc_path)
        saved_files.append(id_doc.filename)

        # Extract face from ID document (stub: assume face is cropped and saved as 'doc_face.jpg')
        doc_face_path = os.path.join(app.config['UPLOAD_FOLDER'], 'doc_face.jpg')
        # In production, use OCR or face detection to extract face
        doc_face = cv2.imread(id_doc_path)  # Placeholder: read the whole image as face
        cv2.imwrite(doc_face_path, doc_face)

        # Capture real-time challenge frames
        challenge_frames = {}
        challenge_frames['look_left'] = capture_challenge_frames('Look to your left')
        challenge_frames['look_right'] = capture_challenge_frames('Look to your right')
        challenge_frames['blink_3_times'] = capture_challenge_frames('Blink 3 times')

        # Run KYC pipeline
        face_matcher = FaceMatchService()
        liveness = LivenessService()
        document = DocumentService()
        decision_engine = DecisionEngine()

        # Face matching: compare doc face with a frame from video (stub)
        S_face = face_matcher.compare_faces(None, None)  # Stub

        # Liveness: passive stub, active from captured frames
        S_live_p = liveness.passive_liveness(None)  # Stub
        results = liveness.active_liveness(challenge_frames, doc_face)
        S_live_a = 1.0 if results['liveness_passed'] else 0.0

        S_doc = 0.84  # Stub value
        S_docmatch = document.compare_id_data({}, {})  # Stub

        decision = decision_engine.decide(S_face, S_live_p, S_live_a, S_doc, S_docmatch)
        scores = {
            "face_similarity": S_face,
            "liveness_passive": S_live_p,
            "liveness_active": S_live_a,
            "doc_authenticity": S_doc,
            "doc_match": S_docmatch
        }
        remarks = "Face matched and liveness verified successfully" if decision == "APPROVED" else "Review or rejected"
        return jsonify({
            "status": decision,
            "scores": scores,
            "remarks": remarks,
            "files": saved_files
        })
    else:
        return jsonify({'error': 'No ID document uploaded'}), 400

@app.route('/verify', methods=['POST'])
def verify():
    # Example: Simulate KYC pipeline using stubs
    face_matcher = FaceMatchService()
    liveness = LivenessService()
    document = DocumentService()
    decision_engine = DecisionEngine()

    # Simulate input (replace with actual file processing)
    S_face = face_matcher.compare_faces(None, None)
    S_live_p = liveness.passive_liveness(None)
    S_live_a = liveness.active_liveness(None)
    S_doc = 0.84  # Stub value
    S_docmatch = document.compare_id_data({}, {})

    decision = decision_engine.decide(S_face, S_live_p, S_live_a, S_doc, S_docmatch)
    scores = {
        "face_similarity": S_face,
        "liveness_passive": S_live_p,
        "liveness_active": S_live_a,
        "doc_authenticity": S_doc,
        "doc_match": S_docmatch
    }
    remarks = "Face matched and liveness verified successfully" if decision == "APPROVED" else "Review or rejected"
    return jsonify({
        "status": decision,
        "scores": scores,
        "remarks": remarks
    })

@app.route('/status', methods=['GET'])
def status():
    # Return verification result
    # ...stub...
    return jsonify({'status': 'APPROVED'})

if __name__ == '__main__':
    app.run(debug=True)
