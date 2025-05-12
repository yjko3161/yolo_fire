import os
import cv2
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
from ultralytics import YOLO

app = Flask(__name__)
app.secret_key = "fire_detection_secret_key"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULT_FOLDER'] = 'static/results'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# 상대 경로 대신 절대 경로 사용
base_dir = os.path.abspath(os.path.dirname(__file__))
upload_dir = os.path.join(base_dir, app.config['UPLOAD_FOLDER'])
result_dir = os.path.join(base_dir, app.config['RESULT_FOLDER'])

# 폴더 생성
try:
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir, exist_ok=True)
        print(f"업로드 폴더 생성됨: {upload_dir}")
    else:
        print(f"업로드 폴더 이미 존재함: {upload_dir}")
        
    if not os.path.exists(result_dir):
        os.makedirs(result_dir, exist_ok=True)
        print(f"결과 폴더 생성됨: {result_dir}")
    else:
        print(f"결과 폴더 이미 존재함: {result_dir}")
except Exception as e:
    print(f"폴더 생성 중 오류 발생: {e}")

# Load YOLO model
model = None

try:
    # Try to load default YOLOv8 model (will download if not available)
    model = YOLO('yolov8s.pt')
except Exception as e:
    print(f"Error loading model: {e}")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # 파일 저장 경로 설정
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        print(f"원본 파일 저장됨: {file_path}")
        
        if model is None:
            flash('YOLO model not loaded')
            return redirect(url_for('index'))
        
        try:
            # Process the image with YOLO
            results = model(file_path)
            
            # 결과 이미지 저장
            result_filename = f"result_{filename}"
            result_path = os.path.join(result_dir, result_filename)
            
            # 이미지 생성 및 저장
            result_img = results[0].plot()
            cv2.imwrite(result_path, result_img)
            print(f"결과 파일 저장됨: {result_path}")
            
            # 웹에서 사용할 경로 - 상대 경로로 지정
            # static 폴더는 Flask에서 자동으로 찾기 때문에 static/ 접두사 없이 사용
            original_web_path = os.path.join('uploads', filename)
            result_web_path = os.path.join('results', result_filename)
            
            print(f"웹 표시용 원본 경로: {original_web_path}")
            print(f"웹 표시용 결과 경로: {result_web_path}")
            
            # Get detection info
            detections = []
            result = results[0]
            for box in result.boxes:
                class_id = int(box.cls[0].item())
                class_name = result.names[class_id]
                confidence = float(box.conf[0].item())
                
                # Only add fire detections or keep all detections based on your requirements
                # Uncomment the next line to filter only fire detections
                # if class_name.lower() == 'fire':
                detections.append({
                    'class': class_name,
                    'confidence': f"{confidence:.2f}"
                })
            
            return render_template('result.html', 
                                  original=original_web_path,
                                  result=result_web_path,
                                  detections=detections)
        
        except Exception as e:
            flash(f'Error processing image: {str(e)}')
            return redirect(url_for('index'))
    
    flash('File type not allowed')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 