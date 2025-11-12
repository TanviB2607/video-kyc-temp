import cv2
import numpy as np

class LivenessService:
    def detect_head_turn(self, frame, direction):
        # Stub: Use facial landmarks or face angle in production
        return np.random.choice([True, False], p=[0.9, 0.1])

    def detect_blink(self, frames, blink_count_required=3):
        # Stub: Use eye aspect ratio or mediapipe for blink detection in production
        return np.random.choice([True, False], p=[0.9, 0.1])

    def match_face(self, video_frame, uploaded_face):
        # Stub: Use face_recognition.compare_faces in production
        return np.random.choice([True, False], p=[0.95, 0.05])

    def active_liveness(self, challenge_frames, uploaded_face):
        results = {}

        # Challenge 1: Look Left
        results['look_left'] = any(self.detect_head_turn(frame, 'left') for frame in challenge_frames['look_left'])

        # Challenge 2: Look Right
        results['look_right'] = any(self.detect_head_turn(frame, 'right') for frame in challenge_frames['look_right'])

        # Challenge 3: Blink 3 Times
        results['blink_3_times'] = self.detect_blink(challenge_frames['blink_3_times'])

        # Face matching: pick a representative frame from each set
        match_results = []
        for challenge in challenge_frames:
            for frame in challenge_frames[challenge][:3]: # First 3 frames from each challenge
                match_results.append(self.match_face(frame, uploaded_face))
        results['face_match_passed'] = all(match_results)

        # Overall liveness:
        results['liveness_passed'] = all([
            results['look_left'],
            results['look_right'],
            results['blink_3_times'],
            results['face_match_passed']
        ])
        return results

def capture_challenge_frames(instruction, num_frames=40):
    print(f"Please: {instruction} (press 'q' to stop early)")
    cap = cv2.VideoCapture(0)
    frames = []
    while len(frames) < num_frames:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow(instruction, frame)
        frames.append(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return frames

def main():
    # Load PAN/Aadhaar face image
    uploaded_face = cv2.imread('uploaded_id_face.jpg')  # Path to uploaded PAN/Aadhaar face crop

    challenge_frames = {}
    challenge_frames['look_left'] = capture_challenge_frames('Look to your left')
    challenge_frames['look_right'] = capture_challenge_frames('Look to your right')
    challenge_frames['blink_3_times'] = capture_challenge_frames('Blink 3 times')

    service = LivenessService()
    results = service.active_liveness(challenge_frames, uploaded_face)
    print('Liveness Results:', results)
    if results["liveness_passed"]:
        print("Liveness check and face match passed.")
    else:
        print("Liveness check failed or face match unsuccessful.")

if __name__ == "__main__":
    main()
