import time
import os

from mercator.mapper.mapping_algorithms.ocr_space_methods import ocr_space_file_request, make_beautified_json, ocr_request_error, ocr_space_text_map
from mercator.mapper.mapping import ScreenMap
"""
Identify all lines of text in the image and assigns a location for each
"""


def ocr_space_matching(map: ScreenMap, showResults=False):
    """
    Identify all lines of text in the image and assigns a location for each
    """
    # TODO:
    # address edge cases where buttons that span two lines like Volume Up and Volume Down are represented as two buttons
    # (maybe if there are two identical lines, remove them both instead of adding to the gui map)
    # add cleaning for each file before it is sent to ocr.space to avoid image exceeding size limit
    # also can potentially add a source_filepath or source_directory input parameter so the directory can be changed
    # (reluctant to do so before refactoring other matching algorithms, which use a source_filepath, not source_directory)
    # (once tested sufficeintly, will likely change this to source_filepath)

    # directory = '../assets/steris/home_page_root_templates/'
    # directory = 'mercator/mapper/assets/steris/home_page_templates/'
    directory = 'mercator/mapper/assets/steris/home-page-templates/'
    num_images = 0
    start_time = time.time()
    for fn in os.listdir(directory):
        # if fn.endswith(".jpg") or fn.endswith(".png"):
        if fn.endswith("home_page_root2.jpg"):
            # opens each home page root template and requests ocr.space processing
            num_images += 1
            fname = directory + fn
            ocr_result = ocr_space_file_request(filename=fname)
            json_of_ocr_result = make_beautified_json(
                ocr_result, target_image_filename=fname)
            if (ocr_request_error(json_of_ocr_result)):
                pass
                # if there was an error in processing the file, skip that image and print an error message
            else:  # otherwise if the image was successfuly parsed by ocr.space, return all the words and their locations
                all_lines, all_locations = ocr_space_text_map(
                    json_file_to_parse=json_of_ocr_result)
                if showResults:
                    print(
                        f'The image {fn} was correctly parsed with outputs below:')
                    print(f'  All lines of text: {all_lines}')
                    print(f'  All locations of text: {all_locations}')
            for text_index in range(len(all_lines)):
                button_label = all_lines[text_index]
                center_x = all_locations[text_index][0]
                center_y = all_locations[text_index][1]
                map.add_widget(button_label, int(center_x), int(center_y))
        else:
            continue
    end_time = time.time()
    elapsed_time = end_time - start_time

############################ Here is a heuristic that should duplicate keys from the list (eg. Volume and volume)
    # Needs to be fixed so it actually removes duplicates and ignores case
    #  for key in map.gui_map.keys():
    #     if map.gui_map.keys().count(key) > 1:
    #         map.remove_widget(key)
############################

    if num_images == 0:
        print(f'The directory {directory} did not contain any .jpg or .png images.')
    else: 
        print(
        f"\n {num_images} different images were parsed using ocr.space. It took {round(elapsed_time, 1)} seconds, or {round(elapsed_time / num_images, 1)} seconds each.")
    return 0  # if the image/s were successfully processed, return 0 indicating success

map = ScreenMap()
ocr_space_matching(map)
map.print_map()
print('\n\n')
print(map.entity_to_widget("Windowing"))
print('\n')
print(map.entity_to_widget("Conference"))
print('\n')
print(map.entity_to_widget("Conference In"))
print('\n')
print(map.entity_to_widget("Volume Up"))
print('\n')
print(map.entity_to_widget("Aux 1"))
print('\n')
print(map.entity_to_widget("ox one"))
print('\n')
print(map.entity_to_widget("Wall Display One"))
print('\n')
print(map.entity_to_widget("Wall Display Two"))
print('\n')
print(map.entity_to_widget("Four K Surgical Display One"))
print('\n')
print(map.entity_to_widget("Four K Surgical Display Two"))
print('\n')
print(map.entity_to_widget("Surgical Display One"))
print('\n')