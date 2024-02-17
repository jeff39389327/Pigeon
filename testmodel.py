from ultralytics import YOLO
import pyautogui
import numpy as np
from PIL import Image
import random
import time
import threading
import configparser
from game import id_to_card

# 設�??模�??路�??
accept_model = YOLO('rk_best.pt')



# 辨識手牌函式
def recognize_hand_cards(model,  id_to_card):
    time.sleep(1)
    screenshot_image = Image.open("a1.jpg")
    screenshot_image = Image.fromarray(np.array(screenshot_image)[..., :3])
    results = accept_model(screenshot_image)

    for result in results:
            
        # 假設result有boxes屬性且boxes有xyxy和cls方法
        # 並假設這些方法可以直接給出所需的numpy數據
            detected_items = result.boxes.xyxy.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy()
            sorted_indices = np.argsort([item[0] for item in detected_items])[:14]
            hand_ids = [int(class_ids[index]) for index in sorted_indices]
            hand = [id_to_card.get(id, "") for id in hand_ids]
            
            return hand, detected_items[sorted_indices]   

hand, boxes = recognize_hand_cards(accept_model, id_to_card)   
print(hand)