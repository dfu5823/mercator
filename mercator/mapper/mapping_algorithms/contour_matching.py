import time
import cv2 as cv
import imutils
from mercator.mapper.preprocessing import clean_image
from mercator.mapper.ocr_algorithms.ocr import extract_text
from mercator.mapper.mapping import ScreenMap


def contour_matching(self, template_filepath: str, client_image, map: ScreenMap):
    """
    The Contour Matching Algorithm matches the contour area extracted from the target button
    (template) with those observed in the interface image (source)
    :param template_filepath: <Add description>
    :param client_image: Image of interface sent by client device located in OR
    :param map: Reference to map tracking location of widgets detected in interface
    """

    start_time = time.time()

    if template_filepath == None:
        print("Must set a template filepath, eg. contour_matching(show_results, template_flag, template_filepath = path_to_your_target_contour,source_filepath = path_to_your_interface_to_map)")

    ##### EXTRACTING CONTOUR AREA FROM TEMPLATE ######

    print(template_filepath)

    template_image = cv.imread(template_filepath)
    if template_image is None:
        print("FILE NOT LOADED PROPERLY")

    image_gray_threshold = clean_image(template_image)

    # Only pay attention to outer most contours that trace shape of button
    contours = cv.findContours(image_gray_threshold, cv.RETR_EXTERNAL,
                               cv.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    # Filter for contour with largest area
    largest_cnt = max(contours, key=cv.contourArea)

    # Extract Area of Contour
    area = cv.contourArea(largest_cnt)

    ### EXTRACTING AND FILTERING CONTOURS FROM SOURCE THAT MATCH TEMPLATE CONTOUR AREA ###

    # Make Copies of Interface Image

    interface_image = client_image
    #cv.imwrite(interface_image, "hehe.png")

    # Convert Interface Image to Grayscale
    interface_gray = cv.cvtColor(client_image, cv.COLOR_BGR2GRAY)

    # Apply Threshold to Grayscale Interface Image
    ret1, thresh1 = cv.threshold(interface_gray, 127, 255, 0)

    # Find Contours In Interface Image With Applied Threshold
    contours = cv.findContours(thresh1.copy(), cv.RETR_LIST,
                               cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    # Establish lower and upper bound for contours areas detected in interface that match the target contour area
    # IMPORTANT: Bounds arbitrarily defined
    lower_bound = area * 0.90
    upper_bound = area * 1.10

    # Filter for contours that fall within established bounds.
    targets = []
    for i in contours:
        cnt = cv.contourArea(i)
        if lower_bound <= cnt <= upper_bound:
            targets.append(i)

    # Trace rectangles over filtered contours
    rects_result = interface_image.copy()
    for i in targets:
        # Render a bounding rectangle for each target contour
        x, y, w, h = cv.boundingRect(i)

        # Capture region of interest within bounded rectangle (button)
        button = rects_result[y:y + h, x:x + w]

        # Extract name of button using OCR algo
        button_label = extract_text(
            image=button, flag=template_filepath, ocr="pytesseract")

        # Calculate & Render Center Point of Rectangle
        center_x = int(x + w / 2)
        center_y = int(y + h / 2)

        # Add Widget To Map
        # Point To ScreenMap Reference??
        map.add_widget(button_label, center_x, center_y)

    print(time.time() - start_time)
