from flask import Flask, request, render_template, jsonify
from services.face_match_service import FaceMatchService
from services.liveness_service import LivenessService
from services.document_service import DocumentService
from services.decision_engine import DecisionEngine
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/', methods=['GET'])
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Handle file uploads
    id_doc = request.files.get('id_doc')
    video = request.files.get('video')
    saved_files = []
    if id_doc:
        id_doc_path = os.path.join(app.config['UPLOAD_FOLDER'], id_doc.filename)
        id_doc.save(id_doc_path)
        saved_files.append(id_doc.filename)
    if video:
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
        video.save(video_path)
        saved_files.append(video.filename)
    if saved_files:
        # Run KYC pipeline after saving files
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
            "remarks": remarks,
            "files": saved_files
        })
    else:
        return jsonify({'error': 'No files uploaded'}), 400

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
