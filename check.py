import pyautogui

print("将鼠标移动到屏幕上的不同位置，并按下Enter键来记录坐标。按下Ctrl-C结束。")

try:
    while True:
        input("按下Enter键记录位置，或者Ctrl-C退出...")
        position = pyautogui.position()
        print("记录的位置：", position)
except KeyboardInterrupt:
    print("\n程序已退出。")


