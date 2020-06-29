from django.conf import settings

from torchvision.models import detection
import cv2
import torch

import json
import os
from pathlib import Path


models = {
    "fasterrcnn_resnet50_fpn": detection.fasterrcnn_resnet50_fpn(pretrained=True).eval(),
}

with open(os.path.join(settings.BASE_DIR, 'detection_demo/labels.json')) as f:
    coco_labels = json.load(f)

CONF_THRESH = 0.85


def detect_image(img_name, model_name="fasterrcnn_resnet50_fpn"):
    img_path = os.path.join(settings.BASE_DIR, f'static/detection_demo/raw_images/{img_name}.png')
    result_path = os.path.join(settings.BASE_DIR, f'static/detection_demo/detected_images/{img_name}_detected.png')

    img = cv2.imread(img_path)[:, :, ::-1]
    img_tensor = torch.from_numpy(img.astype('float32') / 255).permute(2, 0, 1)[None, :]

    predictions = models[model_name](img_tensor)[0]
    boxes = predictions['boxes'][predictions['scores'] > CONF_THRESH]
    labels = predictions['labels'][predictions['scores'] > CONF_THRESH]
    scores = predictions['scores'][predictions['scores'] > CONF_THRESH]

    detected_img = img.copy()
    for box, label, score in zip(boxes, labels, scores):
        multiplier = max(detected_img.shape) / 100
        font_multiplier = multiplier / 13
        thick_multiplier = round(multiplier * 0.125)
        deltax = multiplier * 0.5
        deltay = multiplier * 3

        detected_img = cv2.rectangle(
            detected_img,
            (int(box[0]), int(box[1])),
            (int(box[2]), int(box[3])),
            (255, 255, 255))
        detected_img = cv2.putText(
            detected_img,
            f"{coco_labels[int(label) - 1]}: {float(score):0.4f}",
            (int(box[0] + deltax), int(box[1] + deltay)),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_multiplier,
            (255, 255, 255),
            thick_multiplier,
            cv2.LINE_AA
        )
    cv2.imwrite(result_path, detected_img[:, :, ::-1])
