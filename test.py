import os
from dotenv import load_dotenv
from google import genai
from google.genai import types



# Load API key from .env file
load_dotenv()
api_key = os.getenv("API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
    )
)
print(response.text)



def x():
    # Load image and convert to grayscale
    img = cv2.imread('gemini_img/1_out_of_150.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Load pre-trained eye cascade classifier
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Detect eyes
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=13)

    print(f"Number of eyes detected: {len(eyes)}")

    # Optional: Draw rectangles around detected eyes
    for (x, y, w, h) in eyes:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Eyes detected', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#x()



def detect_basic_features(image_path):
    model = YOLO("yolov8n.pt")  # General pretrained model, auto-downloads

    img = cv2.imread(image_path)
    results = model(img)

    hands_count = 0
    faces_count = 0

    for box in results[0].boxes:
        label = model.names[int(box.cls[0])]
        if label == 'hand':
            hands_count += 1
        elif label == 'person':  # YOLOv8n detects person, but not face specifically
            faces_count += 1

    # Load Haar cascades if available for eyes and glasses
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    glasses_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, 1.1, 4) if not eye_cascade.empty() else []
    glasses = glasses_cascade.detectMultiScale(gray, 1.1, 4) if not glasses_cascade.empty() else []

    # Count fingers approx as 5 fingers per hand detected
    fingers_count = hands_count * 5

    print(f"Hands detected: {hands_count}")
    print(f"Fingers approx: {fingers_count}")
    print(f"Faces detected: {faces_count}")
    print(f"Eyes detected (OpenCV): {len(eyes)}")
    print(f"Glasses detected (OpenCV): {len(glasses)}")

    # Show image with boxes (optional)
    results[0].plot()  # draws YOLO detections on img
    cv2.imshow('Detection', results[0].orig_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
#detect_basic_features('gemini-native-image.png')

mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

def count_fingers(hand_landmarks, handedness):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = 0

    # Thumb: check different direction based on left/right hand
    if handedness.classification[0].label == 'Right':
        if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0] - 1].x:
            fingers += 1
    else:
        if hand_landmarks.landmark[tips_ids[0]].x > hand_landmarks.landmark[tips_ids[0] - 1].x:
            fingers += 1

    # Other fingers
    for id in range(1, 5):
        if hand_landmarks.landmark[tips_ids[id]].y < hand_landmarks.landmark[tips_ids[id] - 2].y:
            fingers += 1
    return fingers

def detect_features(image_path):
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    hands_count = 0
    total_fingers = 0
    eyes_detected = 0
    ears_detected = 0

    # Hands detection and finger counting
    with mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5) as hands:
        results = hands.process(img_rgb)
        if results.multi_hand_landmarks:
            hands_count = len(results.multi_hand_landmarks)
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                total_fingers += count_fingers(hand_landmarks, handedness)
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Face mesh for eyes and ears counting
    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5) as face_mesh:
        results = face_mesh.process(img_rgb)
        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            # Eyes landmarks indices from MediaPipe docs
            left_eye_idxs = [33, 133, 160, 159, 158, 157, 173]
            right_eye_idxs = [362, 263, 387, 386, 385, 384, 398]
            eyes_detected = 0
            for eye_idxs in [left_eye_idxs, right_eye_idxs]:
                # Check if landmarks exist (rough presence detection)
                eyes_detected += 1 if all(face_landmarks.landmark[idx].visibility > 0.5 for idx in eye_idxs) else 0

            # Ears landmarks (approximate)
            left_ear_idx = 234
            right_ear_idx = 454
            ears_detected = 0
            if face_landmarks.landmark[left_ear_idx].visibility > 0.5:
                ears_detected += 1
            if face_landmarks.landmark[right_ear_idx].visibility > 0.5:
                ears_detected += 1

            mp_drawing.draw_landmarks(img, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION)

    print(f"Hands detected: {hands_count}")
    print(f"Fingers detected: {total_fingers}")
    print(f"Eyes detected (approx): {eyes_detected}")
    print(f"Ears detected (approx): {ears_detected}")

    cv2.imshow("Detections", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Test it on your image
#detect_features("gemini-native-image.png")