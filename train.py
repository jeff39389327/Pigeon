#nohup python train.py > train.log 2>&1 & echo $! > run.pid
#pip install opencv-python==4.8.0.74
#pip install ultralytics
#pip install protobuf==3.19.0

from ultralytics import YOLO
import torch
def main():
    # 加载模型，不带 'data' 参数
    model = YOLO("yolov8n.yaml")  # 确保 yolov8n.yaml 包含正确的模型配置

    # 使用您的数据集训练模型
    results = model.train(data='matchconfirm.yaml', 
                          epochs=50,
                          batch=32,
                          imgsz=640,  # Adjust image size if necessary
                          
                           
                            # Make sure to train on GPU device '0'
                          ) 

    # 评估模型在验证集上的性能
    results = model.val(data='matchconfirm.yaml')  # 同样，'data' 参数在这里
    
    

    success = model.export(format='onnx')
if __name__ == '__main__':
    main()