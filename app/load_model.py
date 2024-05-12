import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1' 

from keras.models import load_model
import numpy as np
import cv2

model = load_model('app/data/model1.h5')
print('Model loaded......................')


def filter_contours_by_area(contours,min_area=5000):
    return [c for c in contours if cv2.contourArea(c) > min_area]

def filter_contours_by_ratio(contours, aspect_ratio_range=(1.5, 5)):
    filtered_contours = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w) / h
        if aspect_ratio_range[0] <= aspect_ratio <= aspect_ratio_range[1]:
            filtered_contours.append(cnt)
    return filtered_contours

def extract_check(image):
    if image is None or image.size == 0:
        print("Error: The image is empty or None.")
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _,thresh =cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    image=thresh

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = filter_contours_by_area(contours)
    contours = filter_contours_by_ratio(contours)
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        check_image = image[y:y+h, x:x+w]
        check_image = cv2.resize(check_image, (975, 670))
        return check_image
    else:
        return image

def crop_interest_area(check_image):
    height, width = check_image.shape
    left = max(50, width - 320)
    top = int(height * 0.20)
    right = width - 100
    bottom = int(height * 0.28)
    cropped_image = check_image[top:bottom, left:right]
    return cropped_image

def invert_image(image):
    return cv2.bitwise_not(image)

def detect_and_crop_digit(image):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = filter_contours_by_area(contours, min_area=5)  
    contours = filter_contours_by_ratio(contours, aspect_ratio_range=(0.1, 1))  
    contours.sort(key=lambda cnt: cv2.boundingRect(cnt)[0])

    cropped_digits = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        margin = 5 
        digit = image[max(y-margin, 0):y+h+margin, max(x-margin, 0):x+w+margin]
        cropped_digits.append(digit)
        
    return cropped_digits


def extract_digit_from_image(cropped_image):
    digits = []
    print("len(cropped_image): ", len(cropped_image))
    for i, digit in enumerate(cropped_image):
        if len(digit.shape) == 3:
            digit = cv2.cvtColor(digit, cv2.COLOR_BGR2GRAY)
        
        digit = invert_image(digit)
        digit_resized = cv2.resize(digit, (28, 28))
        digit_smoothed = cv2.GaussianBlur(digit_resized, (5, 5), 0)
        if len(digit_smoothed.shape) == 2:
            digit_smoothed = cv2.cvtColor(digit_smoothed, cv2.COLOR_GRAY2BGR)
        image_yuv = cv2.cvtColor(digit_smoothed, cv2.COLOR_BGR2YUV)
        image_yuv[:,:,0] = cv2.equalizeHist(image_yuv[:,:,0])
        digit_contrast = cv2.cvtColor(image_yuv, cv2.COLOR_YUV2BGR)
        digit_gray = cv2.cvtColor(digit_contrast, cv2.COLOR_BGR2GRAY)
        digit_normalized = digit_gray / 255
        digit_reshaped = digit_normalized.reshape(1, 28, 28, 1)
        prediction = model.predict([digit_reshaped])
        predicted_digit = np.argmax(prediction)
        digits.append(predicted_digit)

    return digits


