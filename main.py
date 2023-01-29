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


def main(folder_with_images, text_position, output_path, datetime_format="%H:%M:%S", margin="3%", font_path="OpenSans-Regular.ttf", font_size="5%",
         font_color="black", duration=500, resize=None):
    images = [os.path.join(folder_with_images, filename) for filename in os.listdir(folder_with_images)]
    with PIL.Image.open(images[0]) as img:
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

    font = PIL.ImageFont.truetype(font_path, font_size)

    frames = []
    for img_path in images:
        with PIL.Image.open(img_path) as img:
            verify_size(img_size=img.size, expected_img_size=expected_img_size)
            creation_time_str = img._getexif().get(36867)
            if creation_time_str is None:
                raise RuntimeError(f"Failed to extract timestamp from image metadata: {os.path.basename(img_path)}."
                                   f" Consider retrieving timestamp from filename.")
            else:
                pass

            creation_time = datetime.datetime.strptime(creation_time_str, "%Y:%m:%d %H:%M:%S")
            timestamp = creation_time.strftime(datetime_format)
            draw = PIL.ImageDraw.Draw(img)

            pic_width, pic_height = img.size
            text_width, text_height = draw.textsize(timestamp, font)

            # Consider font's offset.
            x_offset = font.getoffset(timestamp)[0]
            y_offset = font.getoffset(timestamp)[1]

            print("x offset:", x_offset)
            print("y offset:", y_offset)

            if text_position == "top-left":
                xy = (margin - x_offset, margin - y_offset)
            elif text_position == "top":
                xy = (pic_width / 2 - text_width / 2, margin - y_offset)
            elif text_position == "top-right":
                xy = (pic_width - margin - text_width, margin - y_offset)
            elif text_position == "right":
                xy = (pic_width - margin - text_width, pic_height / 2 - text_height / 2)
            elif text_position == "bottom-right":
                xy = (pic_width - margin - text_width, pic_height - text_height - margin)
            elif text_position == "bottom":
                xy = (pic_width / 2 - text_width / 2, pic_height - text_height - margin)
            elif text_position == "bottom-left":
                xy = (margin - x_offset, pic_height - text_height - margin)
            elif text_position == "left":
                xy = (margin - x_offset, pic_height / 2 - text_height / 2)
            else:
                raise ValueError(f"Provided position {text_position} is invalid. Select a correct position.")

            print(f"Picture size (width, height): {pic_width} x {pic_height} px")
            print(f"Text size (width, height): {text_width} x {text_height} px")
            print("Margin", margin)
            print("Text position (xy):", xy)

            draw.text(xy=xy, text=timestamp, fill=font_color, font=font)

            if resize is not None:
                img = resize_img(img, resize)

            frames.append(img)

    frame_one = frames[0]

    # loop = Integer number of times the GIF should loop. 0 means that it will loop forever. By default, the image will not loop.
    frame_one.save(output_path, format="GIF", append_images=frames[1:],
                   save_all=True, duration=duration, loop=0)

if __name__ == "__main__":
    main()
