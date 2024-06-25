import pytesseract
import cv2
import time
import numpy as np
from PIL import ImageGrab
from difflib import SequenceMatcher

tesseract_location = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = tesseract_location

class Reader:
    def __init__(self, window_handle, window_rect):
        self.window_handle = window_handle
        self.window_rect = window_rect
        self.main_color = (216, 229, 236)
        self.set_color = (216, 229, 236)
        self.cost_color = (106, 155, 170)
        self.possible_main_1 = ["HP", "ATK", "DEF"]
        self.possible_main_3 = ["HP", "ATK", "DEF", "Energy Regen", "Glacio DMG Bonus", "Fusion DMG Bonus", "Electro DMG Bonus", "Aero DMG Bonus", "Spectro DMG Bonus", "Havoc DMG Bonus"]
        self.possible_set = ["Freezing Frost", "Molten Rift", "Void Thunder", "Sierra Gale", "Celestial Light", "Sun-sinking Eclipses", "Rejuvenating Glow", "Moonlit Clouds", "Lingering Tunes"]

    def screenshot(self, test=None):
        if test:
            # return cv2.imread(test)

            im = ImageGrab.grabclipboard()
            if im is not None:
                return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        else:
            im_arr = np.array(ImageGrab.grab(bbox=self.window_rect))
            return cv2.cvtColor(im_arr, cv2.COLOR_RGB2BGR)

    def find_cost(self, im_arr):
        im_cost = self.post_process(im_arr, self.cost_color)
        cost = pytesseract.image_to_string(im_cost, config="--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789")
        try:
            return int(cost)
        except ValueError:
            time.sleep(3)
            return self.find_cost(self.screenshot())

    def find_main(self, im_arr, cost):
        im_main = self.post_process(im_arr, self.main_color)
        text = pytesseract.image_to_string(im_main, config="--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz").split("\n")
        if cost == 1:
            possible_main = self.possible_main_1
        else:
            possible_main = self.possible_main_3
        for t in text:
            for main in possible_main:
                if main.replace(" ", "") in t:
                    return main

    def find_set(self, im_arr):
        im_set = self.post_process(im_arr, self.main_color)
        text = pytesseract.image_to_string(im_set, config="--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-").split("\n")
        for t in text[::-1]:
            for set in self.possible_set:
                if SequenceMatcher(None, set.replace(" ", ""), t).ratio() > 0.75:
                    return set

    def post_process(self, im_arr, color):
        # mask image to only show color
        lower = self.get_lower_bounds(color)
        upper = self.get_upper_bounds(color)
        mask = cv2.inRange(im_arr, lower, upper)

        im_mask = im_arr.copy()
        im_mask[mask == 0] = (255, 255, 255)
        im_mask[mask != 0] = (0, 0, 0)

        # convert image to grayscale and apply Otsu's thresholding
        gray = cv2.cvtColor(im_mask, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # remove noise and  dilate to connect text regions
        open_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, open_kernel, iterations=1)
        dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        dilate = cv2.morphologyEx(opening, cv2.MORPH_DILATE, dilate_kernel, iterations=2)

        # find contours and get rid of small ones
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            area = cv2.contourArea(c)
            if area < 50:
                cv2.drawContours(dilate, [c], -1, 0, -1)

        return dilate

    def get_lower_bounds(self, color):
        return np.array(
            [color[0] - 10,
             color[1] - 10,
             color[2] - 10])

    def get_upper_bounds(self, color):
        return np.array(
            [color[0] + 10,
             color[1] + 10,
             color[2] + 10])
