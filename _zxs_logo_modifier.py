import os
from PIL import Image

images_folder_path = input("Images folder path :: ")
temp_folder_path = "_temp_images"
target_size_input = input("Please type default size of your images (recommended - 2048 x 1149 for best results) :: ")
trgt = target_size_input.split("x")
target_size = (int(trgt[0].strip()), int(trgt[1].strip()))
logo_image_path = input("Logo image path :: ")
output_image_path = "_output_images"

overlay_position = (10, 10)
overlay_size = (500, 350)

def manipulate_images(input_folder, output_folder, target_size):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            image = Image.open(input_path)
            aspect_ratio = image.width / image.height
            new_width = target_size[0]
            new_height = int(new_width / aspect_ratio)

            resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

            final_image = Image.new("RGB", target_size)

            paste_x = 0
            paste_y = (target_size[1] - new_height) // 2
            final_image.paste(resized_image, (paste_x, paste_y))

            final_image.save(output_path)

manipulate_images(images_folder_path, temp_folder_path, target_size)

def overlay_images(background_folder, overlay_image_path, output_folder, overlay_position=(0, 0), overlay_size=None, alpha=0.5):
    overlay = Image.open(overlay_image_path)
    if overlay_size:
        overlay = overlay.resize(overlay_size, Image.ANTIALIAS)
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(background_folder):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            background_path = os.path.join(background_folder, filename)
            output_path = os.path.join(output_folder, filename)

            background = Image.open(background_path)

            overlay = overlay.convert("RGBA")
            background = background.convert("RGBA")

            result = Image.new("RGBA", background.size)
            result.paste(background, (0, 0))
            result.paste(overlay, overlay_position, overlay)

            result.save(output_path, format="PNG")

overlay_position = (10, 10)
overlay_size = (500, 350)
overlay_images(temp_folder_path, logo_image_path, output_image_path, overlay_position, overlay_size)
try:
    files = os.listdir(temp_folder_path)
    for file in files:
        file_path = os.path.join(temp_folder_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
except OSError:
                print("Error occurred while deleting files.")