import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import os.path
import datetime


def verify_size(img_size, expected_img_size):
    if img_size == expected_img_size:
        pass
    else:
        raise ValueError("Image of incorrect size was provided. All images should be of the same size.")


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
    elif isinstance(resize, (float, int)):
        x = round(img.size[0] * resize)
        y = round(img.size[1] * resize)
        resize = (x, y)
    else:
        raise TypeError(f"expected float or tuple of (int, int), got {type(resize)}")

    img = img.resize(resize)
    return img


def percentage_of(percentage, value):
    """
    Calculate percentage of a numeric value. Expected input like '42%'.

    Parameters
    ----------
    percentage : str
        Percentage.
    value : int or float
        The value to calculate percentage of.

    Returns
    -------
    float
        Percentage of a numeric value.

    """

    ratio = float(percentage.rstrip(" %")) / 100
    return ratio * value

samples_dir = "test-images"
samples = [os.path.join(samples_dir, filename) for filename in os.listdir("test-images")]

positions = ["top-left", "top", "top-right", "right", "bottom-right",
             "bottom", "bottom-left", "left"]

# Position
position = "top-left"
# position = "top"
# position = "top-right"
# position = "right"
# position = "bottom-right"
# position = "bottom"
# position = "bottom-left"
# position = "left"
margin = 0  # in pixels
# margin = "10%"  # in percentage

# Resize
resize = None
# resize = (960, 640)
# resize = (960.2, 640.1)  # should raise error

# Font
# font_size = 128
font_size = "10%"
# font_name = "arial"
font_name = "OpenSans-Regular.ttf"

# Text color
text_color = (255, 255, 0)
text_color = "#66ff99"
text_color = "dodgerblue"

# Duration
duration = 500  # The display duration of each frame of the multiframe gif, in milliseconds

# TODO add text size and margin as percentage of picture height

with PIL.Image.open(samples[0]) as img:
    expected_img_size = img.size

# If margin is given as percentage of picture height, calculate margin in pixels
if isinstance(margin, str):
    margin = round(percentage_of(margin, expected_img_size[1]))
else:
    pass

# If font size is given as percentage of picture height, calculate font size in pixels
if isinstance(font_size, str):
    font_size = round(percentage_of(font_size, expected_img_size[1]))
else:
    pass

font = PIL.ImageFont.truetype(font_name, font_size)

frames = []
for img_path in samples:
    with PIL.Image.open(img_path) as img:
        verify_size(img_size=img.size, expected_img_size=expected_img_size)
        creation_time_str = img._getexif().get(36867)
        if creation_time_str is None:
            raise RuntimeError(f"Failed to extract timestamp from image metadata: {os.path.basename(img_path)}."
                               f" Consider retrieving timestamp from filename.")
        else:
            pass

        creation_time = datetime.datetime.strptime(creation_time_str, "%Y:%m:%d %H:%M:%S")
        timestamp = creation_time.strftime("%H:%M:%S")
        draw = PIL.ImageDraw.Draw(img)

        pic_width, pic_height = img.size
        text_width, text_height = draw.textsize(timestamp, font)

        # Consider font's offset.
        x_offset = font.getoffset(timestamp)[0]
        y_offset = font.getoffset(timestamp)[1]

        print("x offset:", x_offset)
        print("y offset:", y_offset)

        if position == "top-left":
            xy = (margin - x_offset, margin - y_offset)
        elif position == "top":
            xy = (pic_width / 2 - text_width / 2, margin - y_offset)
        elif position == "top-right":
            xy = (pic_width - margin - text_width, margin - y_offset)
        elif position == "right":
            xy = (pic_width - margin - text_width, pic_height / 2 - text_height / 2)
        elif position == "bottom-right":
            xy = (pic_width - margin - text_width, pic_height - text_height - margin)
        elif position == "bottom":
            xy = (pic_width / 2 - text_width / 2, pic_height - text_height - margin)
        elif position == "bottom-left":
            xy = (margin - x_offset, pic_height - text_height - margin)
        elif position == "left":
            xy = (margin - x_offset, pic_height / 2 - text_height / 2)
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

# loop = Integer number of times the GIF should loop. 0 means that it will loop forever. By default, the image will not loop.
frame_one.save(gif_path, format="GIF", append_images=frames[1:],
               save_all=True, duration=duration, loop=0)

os.startfile(gif_path, "open")  # testing
