import cv2
import numpy as np
from PIL import ImageGrab


class Scanner:
    def __init__(self, window_handle, window_rect):
        self.window_handle = window_handle
        self.window_rect = window_rect
        self.gold = (170, 239, 255)
        self.purple = (252, 187, 252)
        self.tolerance = 5

    def screenshot(self, test=None):
        if test:
            # return cv2.imread(test)

            im = ImageGrab.grabclipboard()
            if im is not None:
                return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        else:
            im_arr = np.array(ImageGrab.grab(bbox=self.window_rect))
            return cv2.cvtColor(im_arr, cv2.COLOR_RGB2BGR)

    def find_echos_order(self, im_arr):
        im_purple = self.post_process(im_arr, self.purple)
        im_gold = self.post_process(im_arr, self.gold)

        purple_x = self.get_x_coords(im_purple)
        gold_x = self.get_x_coords(im_gold)

        return ["gold" if x in gold_x else "purple" for x in sorted(purple_x + gold_x)]

    def post_process(self, im_arr, color):
        # mask image to only show color
        lower = self.get_lower_bounds(color, self.tolerance)
        upper = self.get_upper_bounds(color, self.tolerance)
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
        dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilate = cv2.morphologyEx(opening, cv2.MORPH_DILATE, dilate_kernel, iterations=3)

        # find contours and get rid of small ones
        cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            area = cv2.contourArea(c)
            if area < 500:
                cv2.drawContours(dilate, [c], -1, 0, -1)

        return dilate

    def get_lower_bounds(self, color, tolerance):
        return np.array(
            [color[0] - tolerance,
             color[1] - tolerance,
             color[2] - tolerance])

    def get_upper_bounds(self, color, tolerance):
        return np.array(
            [color[0] + tolerance,
             color[1] + tolerance,
             color[2] + tolerance])

    def get_x_coords(self, im_arr):
        cnts = cv2.findContours(im_arr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        x_coords = []
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            x_coords.append(x + w // 2)
        return x_coords
