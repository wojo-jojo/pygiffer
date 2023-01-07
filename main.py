import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import os.path
import datetime


def resize_img(img, resize):
    """
    Resize image to specific value or by ratio.

    Parameters
    ----------
    img : PIL.Image object
        Image to resize.
    resize : tuple of (int, int) or float
        The requested size in pixels, as a 2-tuple: (width, height)
        or a float specifying resize ratio in relation to original size.
    Returns
    -------
    img : PIL.Image object
        Resized image.
    """
    if isinstance(resize, tuple) and len(resize) >= 2:
        pass
    elif isinstance(resize, float):
        x = int(round(img.size[0] * resize))
        y = int(round(img.size[1] * resize))
        resize = (x, y)
    else:
        raise TypeError(f"expected float or tuple of (int, int), got {type(resize)}")

    img = img.resize(resize)
    return img


samples_dir = "test-images"
samples = [os.path.join(samples_dir, filename) for filename in os.listdir("test-images")]

positions = ["top-left", "top", "top-right", "right", "bottom-right",
             "bottom", "bottom-left", "left"]

# Arguments
# position = "top-left"
# position = "top"
# position = "top-right"
position = "right"
# position = "bottom-right"
# position = "bottom"
# position = "bottom-left"
# position = "left"
margin = 0  # in pixels

# Text color
text_color = (255, 255, 0)
text_color = "#66ff99"
text_color = "dodgerblue"

# Resize
resize = 0.2
resize = ()

# TODO add arguments: font color, resize
# colors in pillow: https://www.geeksforgeeks.org/python-pillow-colors-on-an-image/
# TODO (maybe) add text size; add margin as percentage of picture width

frames = []

for img_path in samples:
    with PIL.Image.open(img_path) as img:
        # creation_time = exif.get(36867)  # Returns None
        creation_time_str = img._getexif().get(36867)
        if creation_time_str is None:
            raise RuntimeError(f"Failed to extract timestamp from image metadata: {os.path.basename(img_path)}."
                               f" Consider retrieving timestamp from filename.")
        else:
            pass

        creation_time = datetime.datetime.strptime(creation_time_str, "%Y:%m:%d %H:%M:%S")
        timestamp = creation_time.strftime("%H:%M:%S")
        draw = PIL.ImageDraw.Draw(img)
        font = PIL.ImageFont.truetype("arial", 30)

        pic_width, pic_height = img.size
        text_width, text_height = draw.textsize(timestamp, font)

        if position == "top-left":
            xy = (margin, margin)
        elif position == "top":
            xy = (pic_width / 2, margin)
        elif position == "top-right":
            xy = (pic_width - margin - text_width, margin)
        elif position == "right":
            xy = (pic_width - margin - text_width, pic_height / 2)
        elif position == "bottom-right":
            xy = (pic_width - margin - text_width, pic_height - text_height - margin)
        elif position == "bottom":
            xy = (pic_width / 2, pic_height - text_height - margin)
        elif position == "bottom-left":
            xy = (margin, pic_height - text_height - margin)
        elif position == "left":
            xy = (margin, pic_height / 2)
        else:
            raise ValueError(f"Provided position {position} is invalid. Select a correct position.")

        print(f"Picture size (width, height): {pic_width} x {pic_height} px")
        print(f"Text size (width, height): {text_width} x {text_height} px")
        print("Margin", margin)
        print("Text position (xy):", xy)

        draw.text(xy=xy, text=timestamp, fill=text_color, font=font)


        if resize is not None:
            img = resize_img(img, resize)

        frames.append(img)

frame_one = frames[0]

gif_path = os.path.join(os.getcwd(), "test.gif")
frame_one.save(gif_path, format="GIF", append_images=frames[1:],
               save_all=True, duration=500, loop=0)

os.startfile(gif_path, "open")  # testing


