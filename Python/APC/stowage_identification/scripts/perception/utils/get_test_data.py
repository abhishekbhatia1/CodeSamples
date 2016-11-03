# This fine contains configuration information
# for testing the scene identification approach

import numpy as np
import os

class image_data:
    def __init__(self, folder):
        self.image_list, self.mask_list = get_image_list(folder)
        self.item_list = get_item_list(self.image_list)
        self.numbers = getNumbers()
        self.names = getNames()

def get_image_list(folder):
    image_list = []
    mask_list = []
    for fn in os.listdir(folder):
        image_folder = folder
        mask_folder = folder.replace("images","masks")
        image_list.append(image_folder + fn)
        mask_list.append(mask_folder + fn)
    return image_list, mask_list

def get_item_list_ros(item_list, target):
    numbers = getNumbers()
    image_item_list = []
    for item in item_list:
        if (item != 0):
            itemNumToIndex = numbers.index(str(item))
            image_item_list.append(itemNumToIndex)
    target_item = numbers.index(str(target))
    return image_item_list, target_item

def get_item_list(image_list):
    item_list = []
    numbers = getNumbers()
    for image in image_list:
        image_item_list = []
        image_split = image.split("-")
        for text in image_split:
            if (text.isdigit()):
                itemNumToIndex = numbers.index(text)
                image_item_list.append(itemNumToIndex)
        item_list.append(image_item_list)
    return item_list  

def getNumbers():
    numbers = []
    for i in range (38):
        numbers.append(str(i+1))
    return numbers

def getNames():
    
    names =["bunny_book",
            "lol_joke_book",
            "scotch_bubble_mailer",
            "glucose_tablets",
            "dasani_water_bottle", #5
            "rawlings_baseball",
            "folgers_coffee",
            "elmers_glue",
            "hanes_socks",
            "womens_knit_gloves", #10
            "cherokee_shirt",
            "peva_shower_liner",
            "plush_bear",
            "beefhide_bones",
            "plush_puppies_squeakin_eggs", #15
            "mini_glue_sticks",
            "chenille_stems",
            "40w_lightbulb",
            "outlet_plugs",
            "toothbrush",  #20
            "dr_browns_brush",
            "command_hooks",
            "turtle_sippy_cup",
            "fiskars_scissors",
            "duct_tape",  #25
            "extension_cord",
            "dog_bowl",
            "3lb_dumbbell",
            "wire_mesh_pencil_holder",
            "clorox_brush",  #30
            "paper_towels",
            "expo_eraser",
            "kleenex_tissues",
            "pencils_12_count",
            "crayola_crayons", #35
            "jane_eyre_dvd",
            "dove_soap",
            "staples_index_cards"]
    return names

# def getColorArray():
#     colorArray = np.array(
#     [[96,144,206],
#     [100,242,28],
#     [198,59,104],
#     [223,147,150],
#     [126,233,255],
#     [252,244,37],
#     [23,28,130 ],
#     [134,166,170],
#     [184,243,170],
#     [114,83,248 ],
#     [176,73,7 ]])

#     return colorArray
