import cv2
import numpy as np
import math
from paddleocr import PaddleOCR
import re
from scipy.ndimage import interpolation as inter
import easyocr

class OcrMeter:
    def __init__(self, num_digit, meter_type) -> None:
        self.paddleocr = PaddleOCR(use_angle_cls="False", lang="en", show_log=False)
        self.easyocr = easyocr.Reader(['en'],gpu="False")
        self.num_digit = num_digit + 1
        self.meter_type = meter_type
    
    def cal(self, x1, y1, x2, y2, length):
        dx = x1-x2
        dy = y1-y2
        dist = math.sqrt(dx*dx + dy*dy)
        dx /= dist
        dy /= dist
        x3 = x1 + (0)*dy 
        y3 = y1 - (0)*dx
        x4 = x1 - (length)*dy
        y4 = y1 + (length)*dx

        x5 = x2 + (0)*dy 
        y5 = y2 - (0)*dx
        x6 = x2 - (length)*dy
        y6 = y2 + (length)*dx
        return [int(x4),int(y4)],[int(x6),int(y6)]
    
    def crop_rect(self, img, rect):
        # get the parameter of the small rectangle
        center, size, angle = rect[0], rect[1], rect[2]
        center, size = tuple(map(int, center)), tuple(map(int, size))

        # get row and col num in img
        height, width = img.shape[0], img.shape[1]

        # calculate the rotation matrix
        M = cv2.getRotationMatrix2D(center, angle, 1)
        # rotate the original image
        img_rot = cv2.warpAffine(img, M, (width, height))

        # now rotated rectangle becomes vertical, and we crop it
        img_crop = cv2.getRectSubPix(img_rot, size, center)
        if img_crop.shape[0] > img_crop.shape[1]:
          img_crop = cv2.rotate(img_crop, cv2.ROTATE_90_CLOCKWISE)

        return img_crop
    
    def correct_skew(self, image, delta=1, limit=5):
        def determine_score(arr, angle):
            data = inter.rotate(arr, angle, reshape=False, order=0)
            histogram = np.sum(data, axis=1, dtype=float)
            score = np.sum((histogram[1:] - histogram[:-1]) ** 2, dtype=float)
            return histogram, score
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] 
        scores = []
        angles = np.arange(-limit, limit + delta, delta)
        for angle in angles:
            histogram, score = determine_score(thresh, angle)
            scores.append(score)
        best_angle = angles[scores.index(max(scores))]
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
        corrected = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, \
                borderMode=cv2.BORDER_REPLICATE)
        return corrected

    def inference_single(self, img_path):
        output = {}
        img = cv2.imread(img_path)
        h, w, _ = img.shape
        img = img[int(h/4):int(h-h/4), int(w/5.5):int(w-w/5.5), :]
        img = self.correct_skew(img)
        if self.meter_type == "water" or self.meter_type == "electricity":
            result = self.paddleocr.ocr(img, det=True, cls=False)
            # print(result)
            result = result[-1]
            for i in range(len(result)):
                ocr_res = "".join(re.findall(r"\d+", result[i][1][0]))
                box = result[i][0]
                if len(ocr_res) == self.num_digit and ocr_res.isdigit():
                    output["black_digits"] = ocr_res[:-1]
                    output["red_digit"] = ocr_res[-1]
                    break
                if len(ocr_res) == self.num_digit - 1 and ocr_res.isdigit():

                    for j in range(len(result)):
                        if i == j:
                            continue
                        mid_point = (box[0][1] + box[3][1]) / 2
                        if (
                            mid_point > result[j][0][1][1]
                            and mid_point < result[j][0][2][1]
                            and result[j][1][0].isdigit()
                        ):
                            ocr_res += result[j][1][0]
                    if len(ocr_res) == self.num_digit:
                        output["black_digits"] = ocr_res[:-1]
                        output["red_digit"] = ocr_res[-1]
                        break

                    length = int((box[1][0] - box[0][0]) / (self.num_digit-1))
                    x1, y1 = box[1]
                    x2, y2 = box[2]
                    box[1], box[2] = self.cal(x1, y1, x2, y2, length)
                    cnt = np.array(box).astype(int)
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    img_crop = self.crop_rect(img, rect)
                    cv2.imwrite(f"{i}a.png", img_crop)
                    
                    result_crop = self.paddleocr.ocr(img_crop, det=False, cls=False)
                    digits = "".join(re.findall(r"\d+", result_crop[0][0][0]))
                    if len(digits) > self.num_digit:
                        output["black_digits"] = digits[:self.num_digit-1]
                        output["red_digit"] = digits[self.num_digit-1]
                        break
                    elif len(digits) == self.num_digit:
                        output["black_digits"] = digits[:-1]
                        output["red_digit"] = digits[-1]
                        break
                    else:
                        while True:
                            digits += "x"
                            if len(digits) >= self.num_digit:
                                break
                        output["black_digits"] = digits[:-1]
                        output["red_digit"] = digits[-1]
                        break
        elif self.meter_type == "gas":
            result = self.easyocr.readtext(img)
            for i in range(len(result)):
                ocr_res = "".join(re.findall(r"\d+", result[i][1]))
                box = result[i][0]
                if len(ocr_res) == self.num_digit and ocr_res.isdigit():
                    output["black_digits"] = ocr_res[:-1]
                    output["red_digit"] = ocr_res[-1]
                    break
                if len(ocr_res) >= self.num_digit - 3 and len(ocr_res) <= self.num_digit - 1 and ocr_res.isdigit():
                    for j in range(len(result)):
                        if i == j:
                            continue
                        mid_point = (box[0][1] + box[3][1]) / 2
                        if (
                            mid_point > result[j][0][1][1]
                            and mid_point < result[j][0][2][1]
                            and result[j][1][0].isdigit()
                        ):
                            ocr_res += result[j][1][0]
                    if len(ocr_res) == self.num_digit:
                        output["black_digits"] = ocr_res[:-1]
                        output["red_digit"] = ocr_res[-1]
                        break

                    lack_digits = self.num_digit - len(ocr_res)
                    length = int(((box[1][0] - box[0][0]) / lack_digits) * lack_digits) + 10
                    x1, y1 = box[1]
                    x2, y2 = box[2]
                    box[1], box[2] = self.cal(x1, y1, x2, y2, length)
                    cnt = np.array(box).astype(int)
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    img_crop = self.crop_rect(img, rect)
                    
                    result_crop = self.easyocr.recognize(img_crop)

                    digits = "".join(re.findall(r"\d+", result_crop[0][1]))
                    if len(digits) > self.num_digit:
                        output["black_digits"] = digits[:self.num_digit-1]
                        output["red_digit"] = digits[self.num_digit-1]
                        break
                    elif len(digits) == self.num_digit:
                        output["black_digits"] = digits[:-1]
                        output["red_digit"] = digits[-1]
                        break
                    else:
                        while True:
                            digits += "x"
                            if len(digits) >= self.num_digit:
                                break
                        output["black_digits"] = digits[:-1]
                        output["red_digit"] = digits[-1]
                        break
        return output