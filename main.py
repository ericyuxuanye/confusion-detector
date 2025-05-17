from feat import Detector
from webcam import Webcam
import torch

detector = Detector()

webcam = Webcam(src=0,max_frame_rate=1)

print(f"Frame size: {webcam.w} x {webcam.h}")

for frame in webcam:
    frame_tensor = torch.from_numpy(frame).unsqueeze(0).permute(0, 3, 1, 2)
    res = detector.detect(frame_tensor, data_type="tensor")
    print(res.emotions)
