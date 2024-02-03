import cv2
from pathlib import Path

current_directory = Path(__file__).parent
act1_pic_path = current_directory / "Pictures" / "act1wagoon.png"

if act1_pic_path.exists():
    act1_image = cv2.imread(str(act1_pic_path), cv2.IMREAD_COLOR)
    if act1_image is not None:
        print("Image loaded successfully.")
    else:
        print("Error: Image could not be loaded.")
else:
    print("Error: File does not exist.")