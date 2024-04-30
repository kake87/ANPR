import os
import cv2
import recognizer
from flask import Flask, render_template

app = Flask(__name__)

def resize_image(image, target_size=(400, 300)):
    """
    Ресайз изображения до заданного размера.
    """
    return cv2.resize(image, target_size)

@app.route('/')
def index():
    # Путь к папке с изображениями
    image_folder = 'static'
    results = []
    
    # Цикл по всем файлам изображений в папке
    for filename in os.listdir(image_folder):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            # Загрузка оригинального изображения
            image_path = os.path.join(image_folder, filename)
            original_image = cv2.imread(image_path)
            
            # Ресайз изображения для отображения на странице
            resized_image = resize_image(original_image)
            
            # Распознавание текста на оригинальном изображении
            recognized_text = recognizer.recognize_text(image=original_image)
            rate = False

            if 9>len(recognized_text)>=6:
                rate = True
            
            # Добавление результатов в список
            results.append({'filename': filename, 'image_path': image_path, 'resized_image': resized_image, 'recognized_text': recognized_text, 'rate':rate})
    
    # Отображение шаблона с результатами
    return render_template('index.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)