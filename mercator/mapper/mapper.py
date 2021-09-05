# !/usr/bin/env python
# title           :view.py
# description     :Interface Mapping Class using OpenCV
# author          :Juan Maldonado
# recent editor   :Dan Fu
# date            :08/08/2021
# version         :0.0
# usage           :SEE README.md
# python_version  :3.7.10
# conda_version   :4.9.2
# ========================================================================================================

from mercator.mapper.preprocessing import clean_image
from mercator.mapper.mapping_algorithms import contour_matching
from mercator.mapper.mapping import ScreenMap
import time
import argparse
import os
"""
The UIReader maps out the screen locations of interface widgets using OpenCV.
Currently implemented with template matching and contour matching.
"""

# TODO:
# DAN:
# fix map_interface to generalize to any matching algorithm
# add method for automatically getting (via screen capture? if possible?) an image of the interface
# test if cleaning the image actually improves algorithm performance on ocr.space web app
# change all cv references in read_screen to cv2 for clarity
# test all code in test_view
# verify contour_matching still works after fixing map_interface
# compare contour_matching+pytesseract time VS contour_matching+ocr.space time VS ocr_space_matching time
# add widget needs to be done using the OUTPUT of each matching algorithm

# JUAN:
# Strip Mapper to essentials. If a developer wants to test something out, he/she should build his solution using
# UTILS.py, OCR.py and PREPROCESSING.py

PRODUCTION_ALGO = "CONTOUR_MATCHING"


class Mapper:
    def __init__(self):
        """
        Constructor
        """
        self.program_name = None  # To Do: Exception Handling
        self.page_name = None  # To Do: Exception Handling
        # Directory location of templates.
        self.assets_directory = "/assets/"
        # Class in charge of tracking widgets identified by Mapper
        self.gui_map = ScreenMap()
        self.current_view = None

    def map_screen(self, client_image):
        self.update_current_view(client_image)
        return "Coordinates"

    def check_mapper(self, client_image):
        if client_image is not None:
            return "OK"

    def update_current_view(self, client_image):
        self.current_view = client_image

    def map_interface(self, client_image):
        self.update_current_view(client_image)
        # TODO: map_interface is implemented specifically for contour_matching and needs to be generalized to any matching algorithm

        start_time = time.time()
        # specifiy the interface to map
        # "../interface_assets/steris/home_page_templates/home_page_root.jpg"
        source_filepath = self.current_view
        # specify where the contours in the interface (templates) to map are stored
        template_fileroot = os.path.abspath(
            '../Mercator/mercator/mapper/assets/steris/home-page-templates/')
        # /Users/zahza/Documents/PycharmProjects/Mercator/mercator/mapper/assets/steris/home-page-templates
        contour_names = [
            "main window", "sources", "destinations", "square buttons",
            "rect buttons"
        ]
        template_filenames = [
            "main_window.jpg", "vitals_camera.jpg", "surgical_display_1.jpg",
            "mute.jpg", "begin_case.jpg"
        ]
        template_flags = [
            "main_window_template", "sources_template",
            "destinations_template", "bottom_buttons_template",
            "bottom_buttons_template"
        ]

        # Find Main Window, Sources, Destinations, Square Bottom Buttons, Rectangular Bottom Buttons
        for i in range(len(contour_names)):
            # Finds the contour by the name of contour_name. The contour to map is stored in template_filepath
            print(f"FINDING {contour_names[i].upper()}")
            contour_matching.contour_matching(
                self,
                template_filepath=template_fileroot + "/" +
                template_filenames[i],
                client_image=self.current_view,
                map=self.gui_map)

        # Dan: I'm a bit confused why this helper function should be run if the same work is being done above?
        # self.map_interface_helper(self, contour_names[i], template_fileroot+template_filenames[i], show_flag, template_flags[i])
        end_time = time.time()

        print("Elapsed Time - Full Scan: {}".format(end_time - start_time))

    def map_interface_helper(self, contour_name, template_filepath,
                             template_flag, show_flag):
        # Finds the contour by the name of contour_name. The contour to map is stored in template_filepath
        print(f"FINDING {contour_name.upper()}")
        self.session_logger.record_picture(
            self.contour_matching(template_filepath,
                                  show_results=show_flag,
                                  template_flag=template_flag))


def main():
    ap = argparse.ArgumentParser(description="Test Mapping Methods.")
    ap.add_argument(
        "--map_method",
        nargs='?',
        default=PRODUCTION_ALGO,
        type=str,
        choices=["TEMPLATE_MATCHING", "FEATURE_MATCHING", "CONTOUR_MATCHING"],
        help="Mapping method applied to locate widgets.")
    ap.add_argument(
        "--source",
        nargs='?',
        default=
        "interface_assets/steris/home_page_templates/home_page_root.jpg",
        type=str,
        help="Source image where mapping will be performed.")
    ap.add_argument(
        "--template",
        nargs='?',
        default="interface_assets/steris/home_page_templates/vitals_camera.jpg",
        help="Template that will be searched in source image.",
        type=str)
    ap.add_argument("--show",
                    nargs='?',
                    default=0,
                    type=int,
                    choices=[0, 1],
                    help="Display image transformations on screen.")
    args = vars(ap.parse_args())

    viewer = Mapper()
    viewer.source_filepath = args["source"]
    viewer.template_filepath = args["template"]
    viewer.map_interface(args["show"])
    viewer.gui_map.get_map()


if __name__ == "__main__":
    main()
