import PySimpleGUI as sg
import configparser

def save_config(config_filename, values):
    config = configparser.ConfigParser()
    config['UserSettings'] = {}
    # 保存matchconfirm_region的坐标
    config['UserSettings']['left_top_x'] = str(values['left_top_x'])
    config['UserSettings']['left_top_y'] = str(values['left_top_y'])
    config['UserSettings']['width'] = str(values['width'])
    config['UserSettings']['height'] = str(values['height'])
    # 确定哪个单选按钮被选中，并保存其名称
    if values['rank_NE']:
        config['UserSettings']['rank'] = 'NE'
    elif values['rank_SE']:
        config['UserSettings']['rank'] = 'SE'
    with open(config_filename, 'w') as configfile:
        config.write(configfile)

def load_config(config_filename):
    config = configparser.ConfigParser()
    config.read(config_filename)
    return config

# GUI布局
layout = [
    [sg.Text('请设置matchconfirm_region的位置：')],
    [sg.Text('左上角X:'), sg.InputText(key='left_top_x')],
    [sg.Text('左上角Y:'), sg.InputText(key='left_top_y')],
    [sg.Text('宽度:'), sg.InputText(key='width')],
    [sg.Text('高度:'), sg.InputText(key='height')],
    [sg.Radio('rank_NE', "RADIO1", default=True, key='rank_NE'), sg.Radio('rank_SE', "RADIO1", key='rank_SE')],
    [sg.Button('保存'), sg.Button('取消')]
]

# 创建窗口
window = sg.Window('配置matchconfirm_region', layout)

# 事件循环
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == '取消':
        break
    elif event == '保存':
        save_config('settings.ini', values)
        sg.popup('配置已保存!')
        break

window.close()
