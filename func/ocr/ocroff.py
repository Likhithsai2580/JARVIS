import difflib
from time import time
import cv2
import easyocr
import numpy as np
import pyautogui as pg
from PIL import ImageGrab
from concurrent.futures import ThreadPoolExecutor

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

def ocr_off(target_string, double_click=False, target_region=None):
    """Performs OCR and interacts with the UI based on the results."""
    
    start_time = time()
    screen = np.array(ImageGrab.grab(bbox=target_region)) if target_region else np.array(ImageGrab.grab())
    ocr_time = time() - start_time
    print(f"Screenshot captured in {ocr_time:.3f} seconds")

    # Perform OCR on the entire screen
    start_time = time()
    result = reader.readtext(screen)
    ocr_time = time() - start_time
    print(f"OCR completed in {ocr_time:.3f} seconds")

    # Extract words and find closest match
    arr_of_words = [i[1].lower() for i in result]
    closest_match = difflib.get_close_matches(target_string.lower(), arr_of_words, n=1, cutoff=0.8)
    
    if closest_match:
        print(f"The best match for '{target_string}' is '{closest_match[0]}'.")

        # Find matching word's coordinates and click
        for item in result:
            if item[1].lower() == closest_match[0]:
                center_x, center_y = center(item[0])
                action = "Double-clicked" if double_click else "Clicked"
                pg.click(center_x, center_y)
                if double_click:
                    pg.sleep(0.35)  # Adjust delay for double-click accuracy
                    pg.click(center_x, center_y)
                return f"{action} {target_string} button."
    else:
        return f"No button named '{target_string}' found."

def center(points):
    """Calculates the centroid of a set of points."""
    
    sum_x = sum(point[0] for point in points)
    sum_y = sum(point[1] for point in points)
    center_x = int(sum_x / len(points))
    center_y = int(sum_y / len(points))
    return center_x, center_y
