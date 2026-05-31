import os
import cv2
import torch
from ultralytics import YOLO
from collections import Counter


class Model:

    def __init__(self, model_path):
        
        self.model = YOLO(model_path)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def file_type(self,path_file):
        
        file = path_file.lower().split('.')[-1]
        
        if  file in ('jpg', 'png', 'jpeg'):

            return self.detected_photo(path_file)

        else:

            return self.detected_video(path_file)


    def detected_photo(self,file_path):

        result_detected = self.model(file_path, device = self.device)[0]
        
        classes = [self.model.names[int(box.cls[0])] for box in result_detected.boxes] if result_detected.boxes else []
        counts = Counter(classes)
        count_class = [{'name': name, 'count': cnt} for name, cnt in counts.items()]
        return count_class

    def detected_video(self, file_path):
        
        step_cadr = 10
        video = cv2.VideoCapture(file_path)
        cadr = 0
        max_class = Counter()

        while True:
            g, frame = video.read()

            if not g :
                break
                
            cadr +=1

            if cadr % step_cadr != 0 :
                continue

            video_result = self.model(frame, device = self.device)[0]
            
            if video_result.boxes:
                
                classes = [self.model.names[int(box.cls[0])] for box in video_result.boxes]
                frame_count = Counter(classes)
                for name_class, count in frame_count.items():
                    
                    max_class[name_class] = max(max_class[name_class], count)
                    
        video.release()
        return [{'name': name, 'count' : max_class[name]} for name in max_class]