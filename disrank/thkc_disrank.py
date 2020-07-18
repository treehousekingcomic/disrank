from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests
import math
import os

default_bg = os.path.join(os.path.dirname(__file__), 'assets', 'card.png')
online     = os.path.join(os.path.dirname(__file__), 'assets', 'online.png')
offline    = os.path.join(os.path.dirname(__file__), 'assets', 'offline.png')
idle       = os.path.join(os.path.dirname(__file__), 'assets', 'idle.png')
dnd        = os.path.join(os.path.dirname(__file__), 'assets', 'dnd.png')
streaming  = os.path.join(os.path.dirname(__file__), 'assets', 'streaming.png')
font1      = os.path.join(os.path.dirname(__file__), 'assets', 'font.ttf')
font2      = os.path.join(os.path.dirname(__file__), 'assets', 'font2.ttf')

class DisrankGenerator:
    def __init__(self, bg_image:str=None, profile_image:str=None, level:int=1, current_xp:int=0, user_xp:int=20, next_xp:int=100, user_position:int=1, user_name:str='AliTheKing#9129', user_status:str='online'):
        self.user_name = user_name
        self.user_position = user_position
        self.level = level
        self.current_xp = current_xp
        self.user_xp = user_xp
        self.next_xp = next_xp
        
        if not bg_image:
            card = Image.open(default_bg).convert("RGBA")
        else:
            bg_bytes = BytesIO(requests.get(bg_image).content)
            card = Image.open(bg_bytes).convert("RGBA")

            width, height = card.size
            if width == 900 and height == 238:
                pass
            else:
                x1 = 0
                y1 = 0
                x2 = width
                nh = math.ceil(width * 0.264444)
                y2 = 0

                if nh < height:
                    y1 = (height / 2) - 119
                    y2 = nh + y1

                card = card.crop((x1, y1, x2, y2)).resize((900, 238))
        self.card = card
        
        profile_bytes = BytesIO(requests.get(profile_image).content)
        profile = Image.open(profile_bytes)
        profile = profile.convert('RGBA').resize((180, 180))
        self.profile = profile
        
        if user_status == 'online':
            status = Image.open(online)
        if user_status == 'offline':
            status = Image.open(offline)
        if user_status == 'idle':
            status = Image.open(idle)
        if user_status == 'streaming':
            status = Image.open(streaming)
        if user_status == 'dnd':
            status = Image.open(dnd)
        status = status.convert("RGBA").resize((40,40))
        self.status = status
        
        # ======== Fonts to use =============
        self.font_normal = ImageFont.truetype(font1, 36)
        self.font_small = ImageFont.truetype(font1, 20)
        self.font_signa = ImageFont.truetype(font2, 25)

        # ======== Colors ========================
        self.WHITE = (189, 195, 199)
        self.DARK = (252, 179, 63)
        self.YELLOW = (255, 234, 167)
        

    def generate(self):
        profile_pic_holder = Image.new(
            "RGBA", self.card.size, (255, 255, 255, 0)
        )  # Is used for a blank image so that i can mask

        # Mask to crop image
        mask = Image.new("RGBA", self.card.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse(
            (29, 29, 209, 209), fill=(255, 25, 255, 255)
        )  # The part need to be cropped

        # Editing stuff here
        def get_str(xp):
            if xp < 1000:
                return str(xp)
            if xp >= 1000 and xp < 1000000:
                return str(round(xp / 1000, 1)) + "K"
            if xp > 1000000:
                return str(round(xp / 1000000, 1)) + "M"

        draw = ImageDraw.Draw(self.card)
        draw.text((245, 22), self.user_name, self.DARK, font=self.font_normal)
        draw.text((245, 98), f"Rank #{self.user_position}", self.DARK, font=self.font_small)
        draw.text((245, 123), f"Level {self.level}", self.DARK, font=self.font_small)
        draw.text(
            (245, 150),
            f"Exp {get_str(self.user_xp)}/{get_str(self.next_xp)}",
            self.DARK,
            font=self.font_small,
        )

        # Adding another blank layer for the progress bar
        # Because drawing on card dont make their background transparent
        blank = Image.new("RGBA", self.card.size, (255, 255, 255, 0))
        blank_draw = ImageDraw.Draw(blank)
        blank_draw.rectangle(
            (245, 185, 750, 205), fill=(255, 255, 255, 0), outline=self.DARK
        )

        xpneed = self.next_xp - self.current_xp
        xphave = self.user_xp - self.current_xp

        current_percentage = (xphave / xpneed) * 100
        length_of_bar = (current_percentage * 4.9) + 248

        blank_draw.rectangle((248, 188, length_of_bar, 202), fill=self.DARK)
        blank_draw.ellipse((20, 20, 218, 218), fill=(255, 255, 255, 0), outline=self.DARK)

        profile_pic_holder.paste(self.profile, (29, 29, 209, 209))

        pre = Image.composite(profile_pic_holder, self.card, mask)
        pre = Image.alpha_composite(pre, blank)

        # Status badge
        # Another blank
        blank = Image.new("RGBA", pre.size, (255, 255, 255, 0))
        blank.paste(self.status, (169, 169))

        final = Image.alpha_composite(pre, blank)
        final_bytes = BytesIO()
        final.save(final_bytes, 'png')
        final_bytes.seek(0)
        return final_bytes
