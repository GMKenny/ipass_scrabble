from PIL import Image as IT
from PIL import ImageTk as ITK

class ImageResizer:
    def __init__(self, n_width, n_height):
        self.list_of_images = {1: 'achtergrond_woord_menu.png', 0: 'achtergrond_main_menu.png', 2 : "achtergrond_blank.png"}
        self.image_resized_list = {}

        for key, value in self.list_of_images.items():
            self.resize_image(value, n_width, n_height, key)

    def resize_image(self, item, n_width, n_height, num):
        open_image = IT.open(("./gui/images/" + item))
        resized_image = open_image.resize((n_width, n_height), IT.ANTIALIAS)
        complete_image = ITK.PhotoImage(resized_image)
        self.image_resized_list.update({num: complete_image})

    def get_right_images(self):
        return self.image_resized_list
