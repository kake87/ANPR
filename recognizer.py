import cv2
import pytesseract
import numpy as np

# Указание пути к исполняемому файлу Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\user\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'


def segment_license_plate(image):
    # Преобразование изображения в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Пороговая обработка для выделения номера
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Морфологические операции для удаления шума и объединения близких областей
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel, iterations=2)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    # Нахождение контуров номера
    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Выбор самого большого контура (номера)
    max_contour = max(contours, key=cv2.contourArea)
    # Создание маски для контура
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [max_contour], -1, (255), thickness=cv2.FILLED)
    
    # Применение маски к изображению для извлечения номера
    segmented_plate = cv2.bitwise_and(image, image, mask=mask)

    return segmented_plate



def recognize_text(image):

    seg = segment_license_plate(image)

    cv2.imshow('title',seg)
    cv2.waitKey(0)
    # Преобразование в оттенки серого
    gray = cv2.cvtColor(seg, cv2.COLOR_BGR2GRAY)
    
    # Пороговая обработка для выделения номера
    _, threshold = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Нахождение контуров
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Обрезка изображения по контуру номера
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 50 and h > 10:  # Убедимся, что контур достаточно большой
            roi = image[y:y+h, x:x+w]
            break  # Предполагаем, что номер только один
    
    # Увеличение изображения
    resized = cv2.resize(roi, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # Настройки Tesseract
    custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789'
    text = pytesseract.image_to_string(resized, config=custom_config)
    
    return text.strip()

def recognize(file_path):
    # Загрузка изображения
    image = cv2.imread(file_path)
    
    # Сегментация номера
    segmented_plate = segment_license_plate(image)
    
    # Распознавание текста
    text = recognize_text(segmented_plate)
    
    return text