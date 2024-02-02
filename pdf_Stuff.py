from glob import glob
from PIL import Image
glob = glob("filesss/*.png")
for f in glob:
    with Image.open(f) as image:
        cropped = image.rotate(-0.6, expand=True)
        cropped = cropped.crop((221, 121, 900, 1654))
        cropped.save(f"{f}")
