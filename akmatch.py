from ultralytics import YOLO
import pyautogui
import numpy as np
from PIL import Image
import random
import time
import threading
import configparser

pyautogui.FAILSAFE = False

homescreen_models= YOLO('homescreen.pt')
#rank _region
left_top = (953, 323)
right_bottom = (1355, 397)
#rank3e _region


e3_left_top = (983, 677)  #SLIVER3 east
e3_right_bottom = (1306, 727)

# e3_left_top = (988, 532)#jade4south
# e3_right_bottom = (1296, 594)
#rankbz _region


# bz_regionleft_top = (972, 396)
# bz_regionright_bottom = (1347, 464)

bz_regionleft_top = (983, 531)  #SLIVER
bz_regionright_bottom = (1303, 590)


# bz_regionleft_top = (1003, 669)  #GOLD
# bz_regionright_bottom = (1300, 729)

# bz_regionleft_top = (986, 817)  #jade
# bz_regionright_bottom = (1301, 838)
#rank NS_region


NSleft_top = (976, 534)
NSright_bottom = (1302, 599)

game_active_event = threading.Event()
def load_config(config_filename):
    config = configparser.ConfigParser()
    config.read(config_filename)
    return config

config = load_config('settings.ini')

rank_option = config.get('UserSettings', 'rank', fallback='NE')



matchconfirm_region = (734, 149, 49, 38)
home_screen=(1405, 149, 67, 43)



       
        

def click_for_new_game():
  

  if rank_option == 'NE':
    rank_NE(left_top, right_bottom) 
    time.sleep(1) 
    rank_bz(bz_regionleft_top, bz_regionright_bottom) 
    time.sleep(1) 
    rank_e3(e3_left_top, e3_right_bottom)
    time.sleep(12)
  else:
    print("none")    

def rank_NE(top_left, bottom_right):
   
    x = random.randint(top_left[0], bottom_right[0])
    y = random.randint(top_left[1], bottom_right[1])

    
    pyautogui.click(x, y)
def rank_bz(bz_regionleft_top, bz_regionright_bottom):
   
    x = random.randint(bz_regionleft_top[0], bz_regionright_bottom[0])
    y = random.randint(bz_regionleft_top[1], bz_regionright_bottom[1])

    
    pyautogui.click(x, y)

def rank_e3(e3_left_top, e3_right_bottom):
   
    x = random.randint(e3_left_top[0], e3_right_bottom[0])
    y = random.randint(e3_left_top[1], e3_right_bottom[1])

    
    pyautogui.click(x, y)
def rank_SE(top_left, bottom_right):
    
    x = random.randint(top_left[0], bottom_right[0])
    y = random.randint(top_left[1], bottom_right[1])
   


def handle_homescreen_detection():
    while True:  # ???���頦���剖��??���頦���剔��????���頦���剖��??????���??���頦���剖��????畾瑁��??���頦���剖��??���頦���剖��頦���剖��頦���剖��頦���剖��頦���剖��頦����?
        screenshot = pyautogui.screenshot(region=home_screen)
        screenshot_image = Image.fromarray(np.array(screenshot)[..., :3])
        results = homescreen_models(screenshot_image)
        detected_items =[result for result in results if 0 < len(result.boxes.xyxy.cpu().numpy()) < 2]
        
        if detected_items:
            click_for_new_game()  # ���頦���剔��????���頦���剖��???���頦���剖��????畾瑁��??���頦���剖��??���頦���剖��頦���剖��頦����????���頦���剖��??????���頦���剖��??
            return
        else:
            pyautogui.moveTo(1430, 932)  # ���頦���剖��?????���頦���剔��????���頦���剖��???���頦���剖��??????���頦���剖��??���頦���剖��?????
            pyautogui.click()
            time.sleep(5)
            pyautogui.moveTo(1455, 238)  # ���頦���剖��?????���頦���剔��????���頦���剖��???���頦���剖��??????���頦���剖��??���頦���剖��?????
            pyautogui.click()
            time.sleep(5)  # ���頦���剖��??5���頦���剖��??���頦���剖��?????���頦���剖��??���頦���剖��??
def main_loop():
    while True:  # ??���頦���剖��???���頦���剛��?���頦����?���頦���剖��頦���剖��鞈�?��貉�剖��??���頦���剖��??���頦���剖��?????���頦���剖��?????���頦���剖��??
        handle_homescreen_detection()
if __name__ == '__main__':
    main_loop()

# start_matchconfirm_thread()