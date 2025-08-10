from datetime import datetime
import requests
from PIL import Image, ImageOps
from epd7in3f import EPD


URL = "https://photos.app.goo.gl/HgmxBfjKhmcMRd2S6" # REAL
# Using the waveshare 7.3in e-paper - https://waveshare.com/7.3inch-e-paper-hat-f.htm
FRAME_HEIGHT = 480
FRAME_WIDTH = 800
FRAME_SIZE=(FRAME_WIDTH, FRAME_HEIGHT)

resp = requests.get(URL)
import re
links: list[str] = re.findall(r'lh3\.googleusercontent\.com\/pw\/([^"]+)"', resp.text)
# filter out added effects 
clean_links = []
for link in links:
    if link.endswith('-k-no') or link.endswith('-d-ip'):
        continue
    clean_links.append(link)

# dedupe
clean_links = list(set(clean_links))

for link in clean_links:
    full_link = f'https://lh3.googleusercontent.com/pw/{link}'
    
# download image
img_data: bytes = requests.get(full_link).content

# save for logging
timestamp = datetime.now()
filename = f'{timestamp.strftime("%Y-%m-%d_%H:%M:%S")}.jpg'
with open(filename,'wb') as file:
    file.write(img_data)

PADDING_COLOR = "#FFFFFF"
# convert to PIL Image and resize
img = Image.open(filename)
img = ImageOps.pad(img, size=FRAME_SIZE, centering=(0.5,0.5), color=PADDING_COLOR)
img.save("resized"+filename)

# convert to bmp
# bitmap_data = img.tobitmap()

# then run the code


epd = EPD()
# from waveshare_epd import epd7in3f
# epd = epd7in3f.EPD()   
epd.display(epd.getbuffer(img))