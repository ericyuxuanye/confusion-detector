import cv2
from feat import Detector
import torch

detector = Detector()
webcam = cv2.VideoCapture(0)

while True:
    state = input("Input 'c' for confused, 'n' for not confused, 'q' to quit: ")
    if state == 'q':
        break
    webcam.grab()
    ret, frame = webcam.retrieve()
    print("Took photo")
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    tensor_hwc = torch.from_numpy(frame_rgb)
    tensor_chw = tensor_hwc.permute(2, 0, 1)
    tensor_bchw = tensor_chw.unsqueeze(0)
    res = detector.detect(tensor_bchw, data_type="tensor")

    with open(f"data_{state}.csv", "a") as f:
        f.write(",".join(map(str, res.aus.to_numpy()[0])) + "\n")
        f.flush()
