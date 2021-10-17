import time
import cv2
from mercator.mapper.mapper import Mapper
from mercator.mapper.mapping import ScreenMap
import mercator.mapper.utils as utils
from mercator.mapper.mapping_algorithms import ocr_space_methods
import logging
import pytesseract
import re
import os
# TODO: test extract text using ocr.space vs pytesseract


def extract_text(image, flag: str, ocr="ocr.space") -> str:
    """
    Extract text from an image using Google Tesseract.
    :param image: button image returned by contour mapping. Also accepts filepath
    :param flag:
    :param ocr: selects ocr.space or pytesseract
    """
    start_time = time.time()

    # We can't extract a label from the main window
    if "main_window" in flag:
        return "fullscreen"

    # Check if we have an image or a filepath
    if isinstance(image, str):
        # Open a file as an image
        filepath = image
        image = cv2.imread(filepath)

        # Extract the text from the image
        return text_extracter(image, ocr, flag, start_time)
        # Return extracted text

    else:
        image = image
        return text_extracter(image, ocr, flag, start_time)


def text_extracter(image, ocr, flag, start_time):
    if ocr.lower() == "ocr.space" or ocr.lower() == "ocr space" or ocr.lower() == "ocr_space":
        return ocr_space_text_extracter(image, start_time)
    if ocr.lower() == "pytesseract" or ocr.lower() == "tesseract":
        return py_text_extracter(image, flag, start_time)
    return ocr_space_text_extracter(image, start_time)


def ocr_space_text_extracter(image, start_time):
    # TODO: test the method against py_text_extracter
    # make a file from the image
    fname = 'temp_file.jpg'
    cv2.imwrite(fname, image)

    # extract text using the ocr.space file request
    ocr_result = ocr_space_methods.ocr_space_file_request(
        filename=os.path.abspath(fname))
    json_of_ocr_result = ocr_space_methods.make_beautified_json(
        ocr_result, target_image_filename=fname)
    if (ocr_space_methods.ocr_request_error(json_of_ocr_result)):
        pass
        # if there was an error in processing the file, skip that image and print an error message
    else:  # otherwise if the image was successfuly parsed by ocr.space, return all the words and their locations
        all_lines, all_locations = ocr_space_methods.ocr_space_text_map(
            json_file_to_parse=json_of_ocr_result)

    # delete the temporary file
    os.remove('temp_file.jpg.json')

    cleaned_text = all_lines
    print(
        f"Extracting Text: {cleaned_text} ocr.space Elapsed Time: {elapsed_time(start_time)}")
    logging.debug(
        f"Extracting Text: {cleaned_text} ocr.space Elapsed Time: {elapsed_time(start_time)}")

    return str(cleaned_text)


def py_text_extracter(image, flag, start_time):
    # Enlarge image (helps with OCR accuracy)
    enlarged_image = cv2.resize(src=image,
                                dsize=(0, 0),
                                fx=3,
                                fy=3)

    # We need the image in grayscale to apply thresholding
    threshold = None

    # Apply different thresholding technique based on button's features
    if "begin_case" in flag:
        enlarged_image = cv2.resize(src=image,
                                    dsize=(0, 0),
                                    fx=9,
                                    fy=9)

        gray_image = cv2.cvtColor(enlarged_image.copy(), cv2.COLOR_BGR2GRAY)
        threshold = cv2.threshold(src=gray_image,
                                  thresh=127,
                                  maxval=255,
                                  type=cv2.THRESH_BINARY_INV)[1]
    # self.show_result("ButtonThreshold", threshold, 1)

    # final_image = cv.medianBlur(src=final_image, ksize=1)

    # Run OCR on image
    extracted_text = None
    if threshold is None:
        extracted_text = pytesseract.image_to_string(
            image=image.copy(), config='--psm 6')
    if threshold is not None:
        extracted_text = pytesseract.image_to_string(
            image=threshold.copy(), config='--psm 3')

    # Remove punctuation and etc from string
    cleaned_text = utils.clean_string(extracted_text)
    cleaned_text = re.sub('sre.*', '', cleaned_text)

    print(
        f"Extracting Text: {cleaned_text} Pytesseract Elapsed Time: {elapsed_time(start_time)}")
    logging.debug(
        f"Extracting Text: {cleaned_text} Pytesseract Elapsed Time: {elapsed_time(start_time)}")

    return cleaned_text


def elapsed_time(start_time):
    return round(time.time() - start_time, 2)