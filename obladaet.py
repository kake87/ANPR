import cv2 
import numpy as np 
from skimage import color, data, img_as_float 
from skimage.restoration import (denoise_wavelet, estimate_sigma)  


# Считываем изображение и делаем его черно-белым 

image = cv2.imread("2.jpg") 
image = img_as_float(image) 
image = color.rgb2gray(image)
H, W = image.shape[:2]

des_h = 600

scale = int(des_h/H)
des_w = int(W)*scale


image = cv2.resize(image, (des_w, des_h), interpolation=cv2.INTER_LINEAR)
# Функция преобразования Хаара 
def haarTransformation(val):     
    alpha = val/8     
    beta = ( 1.0 - alpha )     
    denoised_image = denoise_wavelet(image, sigma = 0.08, wavelet = "haar",  rescale_sigma=True) 
    #Создаем преобразованную матрицу     
    result = cv2.addWeighted(image, alpha, denoised_image, beta, 0.0) 
    # Получаем итоговое изображение     
    cv2.imshow("Image", result) 
    # Выводим изображение на экран  


cv2.namedWindow('Image') 
cv2.createTrackbar("Noise level", "Image", 0, 30, haarTransformation) # Создаем ползунок 
    
haarTransformation(0) # Вызываем преобразование Хаара  
cv2.waitKey(0) 
cv2.destroyAllWindows() 