import subprocess
import json
import time
from ultralytics import YOLO
import pyautogui
import numpy as np
from PIL import Image
import random
import time
import threading

def interact_with_mortal():
    # Python 解?器的完整路?
    
    mortal_script_path = 'C:\\Users\\M1lk\\Desktop\\richi\\Mortal\\mortal\\mortal.py'

    # 使用完整路????程
    proc = subprocess.Popen(['python', mortal_script_path, '2'], 
                            stdin=subprocess.PIPE, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            text=True)

    # ?送指令到 mortal.py
    commands = [
        '{"type":"start_game"}',
        '{"type":"start_kyoku","bakaze":"E","dora_marker":"3s","kyoku":3,"honba":0,"kyotaku":0,"oya":2,"scores":[22000,23700,26000,28300],"tehais":[["?","?","?","?","?","?","?","?","?","?","?","?","?"],["?","?","?","?","?","?","?","?","?","?","?","?","?"],["1m","1m","4m","5m","1p","5p","8p","1s","4s","4s","6s","8s","N"],["?","?","?","?","?","?","?","?","?","?","?","?","?"]]}',
        '{"type":"tsumo","actor":2,"pai":"6p"}'
    ]

    for command in commands:
        print("Sending:", command)
        proc.stdin.write(command + '\n')
        #proc.stdin.flush()

        time.sleep(1)  # 等待 mortal.py ?理?入并返回?出

        output = proc.stdout.readline()
        error = proc.stderr.readline()  # ?取??信息
        if error:
            print(f"Error: {error.strip()}")
        if output:
            print(f"Received: {output.strip()}")
            process_mortal_output(json.loads(output.strip()))
        else:
            print("No output received.")

    proc.terminate()

def process_mortal_output(output):
    # ?理? mortal.py ?得的?出
    pass

interact_with_mortal()
