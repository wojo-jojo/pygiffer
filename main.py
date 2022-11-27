import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import os
import datetime


samples_dir = "test-images"
samples = [os.path.join(samples_dir, filename) for filename in os.listdir("test-images")]

# positions = ["top-left", "top", "top-right", "right", "bottom-right",
#              "bottom", "bottom-left", "left"]

# Arguments
position = "top"
margin = 50  # in pixels

for img_path in samples[:1]:
    with PIL.Image.open(img_path) as img:
        # Different ways
        # https://stackoverflow.com/questions/23064549/get-date-and-time-when-photo-was-taken-from-exif-data-using-pil
        # creation_time = exif.get(36867)  # Returns None
        creation_time_str = img._getexif().get(36867)
        creation_time = datetime.datetime.strptime(creation_time_str, "%Y:%m:%d %H:%M:%S")
        timestamp = creation_time.strftime("%H:%M:%S")
        draw = PIL.ImageDraw.Draw(img)
        font = PIL.ImageFont.truetype("arial", 30)
        # draw.text((1, 1), "Sample text", fill=(0, 0, 0), font=font)
        # img.show()

        pic_width, pic_height = img.size
        text_width, text_height = draw.textsize(timestamp)

        print(f"Picture size (width, height): {pic_width} x {pic_height} px")
        print(f"Text size (width, height): {text_width} x {text_height} px")

        if position == "top-left":
            xy = (margin, margin)
        elif position == "top":
            xy = (pic_width / 2, margin)
        elif position == "top-right":
            xy = (pic_width - margin, margin)
        elif position == "right":
            xy = (pic_width - margin, pic_height / 2)
        elif position == "bottom-right":
            xy = (pic_width - margin, pic_height - margin)
        elif position == "bottom":
            xy = (pic_width / 2, pic_height - margin)
        elif position == "bottom-left":
            xy = (margin, pic_height - margin)
        elif position == "left":
            xy = (margin, pic_height / 2)
        else:
            raise ValueError(f"Provided position {position} is invalid. Select a correct postion.")

        # TODO add margin as percent of width

        draw.text(xy=xy, text=timestamp, fill=(0, 0, 0), font=font)
        draw.text(xy=(1920/2, 1280/2), text="|", fill=(0, 0, 0), font=font)
        img.show()

        # break  # only execute once for testing
