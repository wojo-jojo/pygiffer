import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import os.path
import datetime


samples_dir = "test-images"
samples = [os.path.join(samples_dir, filename) for filename in os.listdir("test-images")]

positions = ["top-left", "top", "top-right", "right", "bottom-right",
             "bottom", "bottom-left", "left"]

# Arguments
# position = "top-left"
# position = "top"
# position = "top-right"
# position = "right"
# position = "bottom-right"
position = "bottom"
# position = "bottom-left"
# position = "left"
margin = 0  # in pixels
# TODO add arguments: font color, resize
# TODO (maybe) add text size add margin as percentage of picture width

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

        draw.text(xy=xy, text=timestamp, fill=(255, 255, 255), font=font)

        frames.append(img)

frame_one = frames[0]
frame_one.save("test.gif", format="GIF", append_images=frames[1:],
               save_all=True, duration=500, loop=0)
