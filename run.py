#pyinstaller --onefile --noconsole --icon=app.ico  run.py
import game
#
# 启动线程

while True:
  
 

  # 运行游戏
  game.accept_acts_thread() 
  game.start_accept_button_thread()
  game.run_game()
  
