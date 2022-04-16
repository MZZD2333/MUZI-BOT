import base64
from io import BytesIO
from pathlib import Path
from random import choice, randint
from turtle import st

from PIL import Image, ImageDraw

from .draw_info import Ark
from .config import Config
from .extra_data import Extra
async def Arknights_draw(times: int, id: int) -> list:
    """
    明日方舟抽卡算法\n
    * `times` 抽卡次数 1 或 10\n
    * `id` 缓存中的用户id\n
    """
    operators = []
    rarity_list = []
    for i in range(times):
        Ark.cache[id] = Ark.cache.get(id, 0) + 1
        x = randint(1, 100)
        x += (Ark.cache[id]-50)*2 if Ark.cache[id] > 50 else 0
        if 98 < x:
            rarity_list.append(6)
            Ark.cache[id] = 0
        elif 90 < x <= 98:
            rarity_list.append(5)
        elif 40 < x <= 90:
            rarity_list.append(4)
        else:
            rarity_list.append(3)

    for i in rarity_list:
        if i == 6:
            if Ark.xd_role and randint(1, 100) < 70:
                operators.append(choice(Ark.xd_role))
            elif Ark.up_role_6 and randint(1, 100) < 50:
                operators.append(choice(Ark.up_role_6))
            else:
                operators.append(choice(Ark.role_6))
        elif i == 5:
            if Ark.up_role_5 and randint(1, 100) < 50:
                operators.append(choice(Ark.up_role_5))
            else:
                operators.append(choice(Ark.role_5))
        elif i == 4:
            if Ark.up_role_4 and randint(1, 100) < 50:
                operators.append(choice(Ark.up_role_4))
            else:
                operators.append(choice(Ark.role_4))
        else:
            operators.append(choice(Ark.role_3))

    return CreateImg(operators,rarity_list).img()




class CreateImg:
    def __init__(self, operators: list, rarity_list: list):
        self.times = len(operators)
        self.bg_path: Path = Config.extra_data_path['Arknights'] / '背景.png'
        self.gradient_3 = [(  0,  0,  0,0), (255,255,255, 60)]
        self.gradient_4 = [(218,191,216,0), (159,121,238,200)]
        self.gradient_5 = [(238,223,204,0), (240,235,160,230)]
        self.gradient_6 = [(255,193, 37,0), (255, 165, 0,230)]
        ref = {3: '三星', 4: '四星', 5: '五星', 6: '六星'}
        rarity_list = [ref[i] for i in rarity_list]
        self.operators = zip(operators, rarity_list)

    def module(self, operator, rarity, gradient):
        image = Image.new(mode='RGBA', size=(180, 960), color=(0,0,0,0))
        operator_img = Image.open(Config.image_path['Arknights'] / f'{operator}.png').convert('RGBA')
        rarity_img = Image.open(Config.extra_data_path['Arknights'] / f'{rarity}.png').convert('RGBA')
        class_img = Image.open(Config.extra_data_path['Arknights'] / f'{Ark.role_class[operator]}.png').convert('RGBA')

        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 300, 180, 660), fill=(54, 54, 54))
        step_r = (gradient[1][0] - gradient[0][0]) / 300
        step_g = (gradient[1][1] - gradient[0][1]) / 300
        step_b = (gradient[1][2] - gradient[0][2]) / 300
        step_a = (gradient[1][3] - gradient[0][3]) / 300

        for y in range(0, 300):
            bg_r = round(gradient[0][0] + step_r * y)
            bg_g = round(gradient[0][1] + step_g * y)
            bg_b = round(gradient[0][2] + step_b * y)
            bg_a = round(gradient[0][3] + step_a * y)
            for x in range(0, 180):
                draw.point((x, y),fill = (bg_r,bg_g,bg_b,bg_a))
        for y in range(0, 300):
            bg_r = round(gradient[0][0] + step_r * y)
            bg_g = round(gradient[0][1] + step_g * y)
            bg_b = round(gradient[0][2] + step_b * y)
            bg_a = round(gradient[0][3] + step_a * y)
            for x in range(0, 180):
                draw.point((x, 960-y),fill = (bg_r,bg_g,bg_b,bg_a))
        
        sep = round((180-rarity_img.width)/2)
        image.paste(operator_img, (0, 300), mask=operator_img.split()[3])
        image.paste(rarity_img, (sep,280), mask=rarity_img.split()[3])
        image.paste(class_img, (36, 620), mask=class_img.split()[3])
        return image

    def img(self):
        self.image: Image = Image.open(self.bg_path)
        pos_x = round((1920 - self.times*180)/2)
        for o, r in self.operators:
            if r == '三星':
                g = self.gradient_3
            elif r == '四星':
                g = self.gradient_4
            elif r == '五星':
                g = self.gradient_5
            else:
                g = self.gradient_6
            single_image = self.module(o, r, g)
            self.image.paste(single_image, (pos_x, 60), mask=single_image.split()[3])
            pos_x += 180
        io = BytesIO()
        self.image.save(io, format='PNG')
        base64_str = base64.b64encode(io.getvalue()).decode()
        return f"[CQ:image,file=base64://{base64_str}]"
