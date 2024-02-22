from ultralytics import YOLO
from decide_card_to_play import decide_card_based_on_pattern_with_strategy
import pyautogui
import numpy as np
from PIL import Image
import random
import time
import threading
import configparser
# 关闭pyautogui的安全模式，防止程序在移动鼠标时抛出异常
pyautogui.FAILSAFE = False

# 加载模型
accept_model = YOLO('bestaccept.pt')
acts_model = YOLO('acts_best.pt')
model = YOLO('best.pt')
matchconfirm_model= YOLO('rk_best.pt')
# 定义检测区域
accept_region = (1624, 939, 240, 97)  # 接受按钮区域
region = (243, 906, 1521, 155)        # 手牌区域
acts_region = (439, 774, 1103, 115)       # 吃碰剛和區域
#rank NE_region
left_top = (1129, 460)
right_bottom = (1408,529)
#rank NS_region
NSleft_top = (1487, 459)
NSright_bottom = (1788, 546)
matchconfirm_region=(148, 25, 186, 56)
# 定義螢幕解析度
screen_width = 1366
screen_height = 768
game_active_event = threading.Event()
game_over_counter = 0 

# 牌的ID到名称的映射
id_to_card = {0: "1m", 1: "2m", 2: "3m", 3: "4m", 4: "5m", 5: "6m", 6: "7m", 7: "8m", 8: "9m", 
              9: "1p", 10: "2p", 11: "3p", 12: "4p", 13: "5p", 14: "6p", 15: "7p", 16: "8p", 17: "9p", 
              18: "1s", 19: "2s", 20: "3s", 21: "4s", 22: "5s", 23: "6s", 24: "7s", 25: "8s", 26: "9s", 
              27: "E", 28: "S", 29: "W", 30: "N", 31: "P", 32: "F", 33: "C",34:"5mr",35:"5pr",36:"5sr"}

# 動作的ID到名称的映射
id_to_act = {0: "skip", 1: "ron", 2: "tsumo", 3: "pon", 4: "eat", 5: "north", 6: "kan", 7: "richi"}

def load_config(config_filename):
    config = configparser.ConfigParser()
    config.read(config_filename)
    return config

config = load_config('settings.ini')
rank_option = config.get('UserSettings', 'rank_option', fallback='NE')

def run_game():

  while True:
    
    # 内层循环持续识别和点击牌
    while True:
        models = YOLO('best.pt')
        
        regions = (243, 906, 1521, 155) 


        hand, boxes = recognize_hand_cards(models, regions, id_to_card)
        print (len(hand))
        # 判断手牌数
        if len(hand) >= 14:
            # 根據全牌效判斷並決定該出哪張牌
            strategy_used, card_name = decide_card_based_on_pattern_with_strategy(hand)
            print(f"對於手牌 {hand}，使用策略 {strategy_used}，建議丟棄的牌是：{card_name}")
            # 取最后一张牌的名字 
            #card_name = "4p"  
        
            # 尝试点击这张牌
            result = click_on_card(models, regions, card_name)  
        
            if result:
                print("Successfully clicked", card_name)
            else:
                print("Failed to click", card_name)
      
    # 延时后继续        
    time.sleep(2)

    # 游戏结束,退出内层循环
    break
  
# 辨識手牌函式
def recognize_hand_cards(model, region, id_to_card):
    time.sleep(1)
    screenshot = pyautogui.screenshot(region=region)
    screenshot_image = Image.fromarray(np.array(screenshot)[..., :3])
    
    
    results = model(screenshot_image, conf=0.8)
    for result in results:
        detected_items = result.boxes.xyxy.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy()
        sorted_indices = np.argsort([item[0] for item in detected_items])[:14]
        hand_ids = [int(class_ids[index]) for index in sorted_indices]
        hand = [id_to_card.get(id, "") for id in hand_ids]
    return hand, detected_items[sorted_indices]
# 辨識手牌函式
def test_recognize_hand_cards(model, region, id_to_card):
    
    screenshot_image = Image.open("4.png")
    
    screenshot_image = Image.fromarray(np.array(screenshot_image)[..., :3])
    results = model(screenshot_image)
    for result in results:
        detected_items = result.boxes.xyxy.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy()
        sorted_indices = np.argsort([item[0] for item in detected_items])[:14]
        hand_ids = [int(class_ids[index]) for index in sorted_indices]
        hand = [id_to_card.get(id, "") for id in hand_ids]
    return hand, detected_items[sorted_indices]

def random_click_on_screen(width, height, clicks=3):
    for _ in range(clicks):
        # 生成螢幕範圍內的隨機坐標
        x = random.randint(0, width)
        y = random.randint(0, height)

        # 在生成的隨機坐標上進行點擊
        pyautogui.click(x, y)
        time.sleep(2)

def click_on_card(model, region, card_name):
    # 重新进行牌的识别
    screenshot = pyautogui.screenshot(region=region)
    screenshot_image = Image.fromarray(np.array(screenshot)[..., :3])
    results = model(screenshot_image, conf=0.7)
    all_detected_items = results[0].boxes.xyxy.cpu().numpy()[:14]  # 获取前14张牌的位置

    # 识别出的牌的ID
    class_ids = results[0].boxes.cls.cpu().numpy()

    # 存储与指定牌名匹配的所有牌的位置
    matching_cards = []
    for i, box in enumerate(all_detected_items):
        detected_card_id = int(class_ids[i])
        detected_card_name = id_to_card.get(detected_card_id, "")
        if detected_card_name == card_name:
            matching_cards.append(box)

    # 如果找到匹配的牌，点击最左边的一张
    if matching_cards:
        leftmost_card = min(matching_cards, key=lambda x: x[0])  # 根据 x_min 值找到最左边的牌
        x_min, y_min, x_max, y_max = leftmost_card[:4]
        center_x = (x_min + x_max) / 2
        center_y = (y_min + y_max) / 2
        screen_x = center_x + region[0]
        screen_y = center_y + region[1]
        pyautogui.moveTo(screen_x, screen_y, duration=0.2)
        pyautogui.click()
        pyautogui.moveTo(1366, 768, duration=0.2)
        
        return True  # 成功点击牌
    return False  # 未找到指定牌

# 持續偵測新牌並輸出牌名的函式
def detect_new_card(model, region, id_to_card):
    while True:
        screenshot = pyautogui.screenshot(region=region)
        screenshot_image = Image.fromarray(np.array(screenshot)[..., :3])
        results = model(screenshot_image, conf=0.6)
        for result in results:
            detected_items = result.boxes.xyxy.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy()
            sorted_indices = np.argsort([item[0] for item in detected_items])
            if len(sorted_indices) >= 14:
                new_card_id = int(class_ids[sorted_indices[13]])
                new_card_name = id_to_card.get(new_card_id, "")
                print("New card detected:", new_card_name)
        time.sleep(2)  # 检测间隔（以秒为单位）
        
def rank_NE(top_left, bottom_right):
    # 生成矩形範圍內的隨機坐標
    x = random.randint(top_left[0], bottom_right[0])
    y = random.randint(top_left[1], bottom_right[1])

    # 在生成的隨機坐標上進行點擊
    pyautogui.click(x, y)
def rank_SE(top_left, bottom_right):
    # 生成矩形範圍內的隨機坐標
    x = random.randint(top_left[0], bottom_right[0])
    y = random.randint(top_left[1], bottom_right[1])

    # 在生成的隨機坐標上進行點擊
    pyautogui.click(x, y)
def recognize_hand_after_delay(model, region, delay, max_attempts=3):
    global game_over_counter
    time.sleep(15)
    model=YOLO('best.pt')
    region= (243, 890, 1524, 171) 
    id_to_card = {0: "1m", 1: "2m", 2: "3m", 3: "4m", 4: "5m", 5: "6m", 6: "7m", 7: "8m", 8: "9m", 
              9: "1p", 10: "2p", 11: "3p", 12: "4p", 13: "5p", 14: "6p", 15: "7p", 16: "8p", 17: "9p", 
              18: "1s", 19: "2s", 20: "3s", 21: "4s", 22: "5s", 23: "6s", 24: "7s", 25: "8s", 26: "9s", 
              27: "E", 28: "S", 29: "W", 30: "N", 31: "P", 32: "F", 33: "C",34:"5mr",35:"5pr",36:"5sr"}
    attempts = 0
    
    while attempts < max_attempts:
        hand, _ = recognize_hand_cards(model, region, id_to_card)
        hand_count = len(hand)
        print("hands_count",hand_count)
        
        if hand_count < 10:
            game_over_counter += 1
        else:
            game_over_counter = 0  # 重置計數器
            print("New round with full hand detected")
            break
        
        if game_over_counter >= max_attempts:
            
            print("Game over detected")
            
            start_matchconfirm_thread()
            print("rank match") 
            
            
            
    

        
            
        break
        
        attempts += 1
        time.sleep(1)  # 在連續嘗試之間等待
# 随机点击屏幕重新配对的函数
def click_for_new_game():
  

  if rank_option == 'NE':
    rank_NE(left_top, right_bottom) 
  else:
    rank_SE(NSleft_top, NSright_bottom)
def detect_accept_button(model, region, event):
    while True:

        event.wait()  # 等待事件被設置
        time.sleep(1)
        screenshot = pyautogui.screenshot(region=region)
        screenshot_image = Image.fromarray(np.array(screenshot)[..., :3])
        
        results = model(screenshot_image)
        
        for result in results:
            detected_items = result.boxes.xyxy.cpu().numpy()
            if len(detected_items) > 0:
                x_min, y_min, x_max, y_max = detected_items[0][:4]
                center_x = (x_min + x_max) / 2
                center_y = (y_min + y_max) / 2
                screen_x = center_x + region[0]
                screen_y = center_y + region[1]
                pyautogui.moveTo(screen_x, screen_y, duration=0.2)
                pyautogui.click()
                pyautogui.moveTo(1366, 768, duration=0.2)
                print("Clicked accept button")

                # 在另一個線程中延遲5秒後執行手牌辨識
                threading.Thread(target=recognize_hand_after_delay, args=(model, region, 60)).start()

                break  # 跳出for迴圈，重新開始偵測按鈕

       


        time.sleep(1)  # 短暫休息後繼續偵測按鈕

# 啟動偵測接受按鈕的線程
def start_accept_button_thread():
    game_active_event.set()  # 啟動事件
    accept_button_thread = threading.Thread(target=detect_accept_button, args=(accept_model, accept_region, game_active_event))
    accept_button_thread.start()
# 啟動偵測matchconfirm按鈕的線程
def start_matchconfirm_thread():
    game_active_event.set()  # 啟動事件
    accept_button_thread = threading.Thread(target=detect_matchconfirm_button, args=(matchconfirm_model, matchconfirm_region, game_active_event))
    accept_button_thread.start()
# 啟動偵測接受按鈕的線程
def accept_acts_thread():
    game_active_event.set()  # 啟動事件
    act="skip"
    accept_acts_thread = threading.Thread(target=detect_acts_button, args=(acts_model, acts_region, act,game_active_event))
    accept_acts_thread.start()


def detect_acts_button(model, region, act_name,event):
    while True:
        event.wait()  # 等待事件被設置
        time.sleep(2)
        x_start, y_start, width, height = region
        screenshot = pyautogui.screenshot(region=region)
        screenshot_image = Image.fromarray(np.array(screenshot)[..., :3])
        

        results = model(screenshot_image, conf=0.7)
        for result in results:
            detected_items = result.boxes.xyxy.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy()

            for i, class_id in enumerate(class_ids):
                detected_card_name = id_to_act.get(int(class_id), "")
                if detected_card_name == act_name:
                    x_min, y_min, x_max, y_max = detected_items[i][:4]
                    center_x = (x_min + x_max) / 2
                    center_y = (y_min + y_max) / 2
                    screen_x = center_x + x_start
                    screen_y = center_y + y_start
                    pyautogui.moveTo(screen_x, screen_y, duration=0.2)
                    pyautogui.click()
                    print(act_name+" click access")
                    break  # 成功点击牌
       
        time.sleep(1)  # 短暫休息後繼續偵測按鈕
                
def detect_matchconfirm_button(model, region, event):
    while True:
        event.wait() 
        time.sleep(1)  
        screenshot = pyautogui.screenshot(region=region)
        screenshot_image = Image.fromarray(np.array(screenshot)[..., :3])
        screenshot_image.save("a2.jpg")

        results = model(screenshot_image)  
        for result in results:
            
            
            detected_items = result.boxes.xyxy.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy()
            
            if  len(detected_items) ==1 :
                print("Match confirm button detected.")
                click_for_new_game()
                print("Match confirm button click.")
                 
                return  

        time.sleep(1)  
            


       
        
        

# 在遊戲開始時呼叫這個函數
#start_accept_button_thread()
# 创建并启动偵測新牌的線程
#card_detection_thread = threading.Thread(target=detect_new_card, args=(model, region, id_to_card))
#card_detection_thread.start()

# 创建并启动偵測動作按鈕的線程
#game_active_event.set()
#act="skip"
#accept_acts_thread = threading.Thread(target=detect_acts_button, args=(acts_model, acts_region, act,game_active_event))
#accept_acts_thread.start()
 #手牌辨識
#hand, sorted_boxes = recognize_hand_cards(model, region, id_to_card)
#hand, sorted_boxes=test_recognize_hand_cards(model, region, id_to_card)
#print("Hand cards:", hand)

# 根据检测到的牌数量，点击相应的牌
##card_name = "9p"
#click_result = click_on_card(model, region, card_name)
#if click_result:
#    print(card_name + " click success")
#else:
#    print(card_name + " click failed")


# 如果在某個時刻需要停止線程（例如，遊戲結束時）
#stop_accept_button_thread()

# 如果偵測到新的手牌，並且想要重新開始線程
#resume_accept_button_thread()


#hand, sorted_boxes=test_recognize_hand_cards(model, region, id_to_card)
#print("Hand cards:", hand)
#start_matchconfirm_thread()