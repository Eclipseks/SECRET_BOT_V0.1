import os
from PIL import Image, ImageDraw, ImageFont

def get_photo_from_card(login, date, room, amount):
    path = os.path.abspath(f"func/img.png")
    image = Image.open(path)

    font = ImageFont.truetype("func/pride.ttf", 35)
    # font1 = ImageFont.truetype("secret_bot/func/pride.ttf", 27)

    drawer = ImageDraw.Draw(image)
    drawer.text((131, 635), login, font=font, fill='white')

    drawer1 = ImageDraw.Draw(image)
    drawer1.text((610, 635), date, font=font, fill='white')

    drawer2 = ImageDraw.Draw(image)
    drawer2.text((914, 635), room, font=font, fill='white')

    drawer3 = ImageDraw.Draw(image)
    drawer3.text((1180, 635), amount, font=font, fill='white')

    image.save(f'func/{login}.png')
    return os.path.abspath(f"func/{login}.png")
