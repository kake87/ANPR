import cv2
import numpy as np
from sklearn.cluster import KMeans

def visualise_colors(cluster, centroids, bar_width):
    labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    (hist, _) = np.histogram(cluster.labels_, bins=labels)
    hist = hist.astype('float')
    hist /= hist.sum()

    # Создаем прямоугольник для гистограммы с заданной шириной
    rect = np.zeros((50, bar_width, 3), dtype=np.uint8)
    colors = sorted([(percent, color) for percent, color in zip(hist, centroids)])
    start = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    for (percent, color) in colors:
        end = start + (percent * bar_width)
        cv2.rectangle(rect, (int(start), 0), (int(end), 50), color.astype('uint8').tolist(), -1)
        text_position = int(start + (end - start) / 2)
        cv2.putText(rect, "{:0.1f}%".format(percent * 100), (text_position, 35), font, 0.3, (0, 0,0), 1)
        start = end
    return rect

img = cv2.imread('2.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Задаем ширину изображения
desired_width = 900
img_resized = cv2.resize(img, (desired_width, int(desired_width * img.shape[0] / img.shape[1])))

reshape = img_resized.reshape((img_resized.shape[0] * img_resized.shape[1], 3))

cluster = KMeans(n_clusters=7).fit(reshape)
visual = visualise_colors(cluster, cluster.cluster_centers_, desired_width)

combined = cv2.vconcat([img_resized, visual])  # Вертикальное соединение изображения и гистограммы
combined = cv2.cvtColor(combined, cv2.COLOR_RGB2BGR)
cv2.imshow('Combined Image and Color Histogram', combined)
cv2.waitKey(0)
cv2.destroyAllWindows()