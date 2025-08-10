from datetime import datetime
import requests
import random
from PIL import Image, ImageOps, ImageEnhance
from epd7in3f import EPD


URL = "https://photos.app.goo.gl/HgmxBfjKhmcMRd2S6"
# Using the waveshare 7.3in e-paper - https://waveshare.com/7.3inch-e-paper-hat-f.htm
# using it vertically
FRAME_HEIGHT = 800
FRAME_WIDTH = 480
# how PIL expects the frame size (width, height)
FRAME_SIZE=(FRAME_WIDTH, FRAME_HEIGHT)

# TODO - maybe a softer white?
PADDING_COLOR = "#FFFFFF"

resp = requests.get(URL)
import re
links = re.findall(r'lh3\.googleusercontent\.com\/pw\/([^"]+)"', resp.text)
# filter out added effects 
clean_links = []
for link in links:
    if link.endswith('-k-no') or link.endswith('-d-ip'):
        continue
    clean_links.append(link)

# dedupe
clean_links = list(set(clean_links))
chosen_link = random.choice(clean_links)
full_link = f'https://lh3.googleusercontent.com/pw/{chosen_link}'

# download image
img_data: bytes = requests.get(full_link).content

# save for logging
timestamp = datetime.now()
filename = f'{timestamp.strftime("%Y-%m-%d_%H:%M:%S")}.jpg'
with open(filename,'wb') as file:
    file.write(img_data)

# convert to PIL Image
img = Image.open(filename)
enhancer =ImageEnhance.Color(img)
# img = enhancer.enhance(1.5)
img = img.convert("P", palette=Image.ADAPTIVE, dither=Image.FLOYDSTEINBERG)
img = ImageOps.pad(img, size=FRAME_SIZE, centering=(0.5,0.5), color=PADDING_COLOR)
# img.save("resized"+filename)

# use the waveshare demo's code to handle the drawing
epd = EPD()
epd.init()
epd.display(epd.getbuffer(img))