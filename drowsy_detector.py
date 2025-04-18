import cv2
import mediapipe as mp
import numpy as np
import winsound

# === Constants ===
EYE_AR_THRESHOLD = 0.25     # EAR below this → closed eye
CONSEC_FRAMES = 30          # How many frames to count as drowsy
BEEP_FREQ = 2500            # Frequency of beep
BEEP_DUR = 1000             # Duration in ms

# === Mediapipe Setup ===
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils

# === Eye Landmark Indexes ===
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def calculate_EAR(landmarks, eye_indices, frame_w, frame_h):
    coords = [(int(landmarks[i].x * frame_w), int(landmarks[i].y * frame_h)) for i in eye_indices]

    # Vertical distances
    A = np.linalg.norm(np.array(coords[1]) - np.array(coords[5]))
    B = np.linalg.norm(np.array(coords[2]) - np.array(coords[4]))
    # Horizontal distance
    C = np.linalg.norm(np.array(coords[0]) - np.array(coords[3]))

    ear = (A + B) / (2.0 * C)
    return ear

# === Main Loop ===
cap = cv2.VideoCapture(0)
closed_frames = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    h, w = frame.shape[:2]
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        mesh = results.multi_face_landmarks[0].landmark

        left_ear = calculate_EAR(mesh, LEFT_EYE, w, h)
        right_ear = calculate_EAR(mesh, RIGHT_EYE, w, h)
        avg_ear = (left_ear + right_ear) / 2.0

        # Debug: show EAR value
        cv2.putText(frame, f'EAR: {avg_ear:.2f}', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if avg_ear < EYE_AR_THRESHOLD:
            closed_frames += 1
            if closed_frames >= CONSEC_FRAMES:
                winsound.Beep(BEEP_FREQ, BEEP_DUR)
                cv2.putText(frame, 'DROWSINESS ALERT!', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        else:
            closed_frames = 0
    else:
        # No face detected
        cv2.putText(frame, 'WARNING: NO FACE DETECTED!', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

    cv2.imshow('Driver Monitor', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
