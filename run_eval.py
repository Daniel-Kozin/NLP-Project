import json
import cv2

from evaluation import *

data_path = 'data/examples.jsonl'

def eval():
    with open(data_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()  # remove trailing newline
            if not line:
                continue
            try:
                obj = json.loads(line)
                line = obj["description"]
                print(line)
            except json.JSONDecodeError:
                print("Skipping invalid JSON line:", line)

def eval_test():
    with open(data_path, 'r', encoding='utf-8') as f:
        obj_line = f.readline()
        obj = json.loads(obj_line)
        line = obj["description"]

        prompt_answer(line)

#eval_test()

def x():


    # Load image and convert to grayscale
    img = cv2.imread('gemini-native-image.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Load pre-trained eye cascade classifier
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Detect eyes
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    print(f"Number of eyes detected: {len(eyes)}")

    # Optional: Draw rectangles around detected eyes
    for (x, y, w, h) in eyes:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Eyes detected', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

x()