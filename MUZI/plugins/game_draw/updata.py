import asyncio
import re
from pathlib import Path
from random import randint

import nonebot
from bs4 import BeautifulSoup
from httpx import AsyncClient
from nonebot.log import logger

from .config import Config, dump_json
from .draw_info import Ark
from .extra_data import Extra


async def _download_img(url: str, save_path: Path, name:str):
    await asyncio.sleep(randint(20,200)/100)
    async with AsyncClient() as client:
        img = await client.get(url, timeout=120)
        if img.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(img.content)
            logger.info(f'\033[36m{name}.png\033[0m \033[32m下载完成\033[0m')
        else:
            logger.info(f'\033[36m{name}.png\033[0m \033[31m下载失败\033[0m')

async def _check_img(game: str, data: dict):
    async_tasks = []
    path = Config.image_path[game]
    for i in data:
        img_path = Path(path / f'{i}.png')
        if not img_path.exists():           
            async_tasks.append(_download_img(data[i]['img_url'], img_path, i))
    if async_tasks:
        await asyncio.wait(async_tasks)

async def _ckeck_extra_data(game: str, data: dict):
    async_tasks = []
    path = Config.extra_data_path[game]
    for i in data:
        img_path = Path(path / f'{i}.png')
        if not img_path.exists():           
            async_tasks.append(_download_img(data[i], img_path, i))
    if async_tasks:
        await asyncio.wait(async_tasks)


async def check_updata_Arknights():
    """检查更新明日方舟信息"""
    logger.info('\033[35m正在获取最新\033[0m \033[36m明日方舟\033[0m \033[35m信息\033[0m')
    Ark.reload()
    async with AsyncClient() as client:
        ark_role_data = {}
        resp_1 = await client.get(url='https://prts.wiki/w/干员一览', timeout=60)
        resp_2 = await client.get(url='https://prts.wiki/w/首页', timeout=60)
        soup_1=BeautifulSoup(resp_1.content, 'lxml')
        soup_2=BeautifulSoup(resp_2.content, 'lxml')

        for i in soup_1.find_all('div',class_='smwdata'):
            ark_role_data[i.get('data-cn')] = {
                'rarity': int(i.get('data-rarity'))+1,
                'class': i.get('data-class'),
                'approach': i.get('data-approach'),
                'img_url': f"https://prts.wiki/images/{re.search(r'thumb/(.*)/%',i.get('data-half')).group(1)}/半身像_{i.get('data-cn')}_1.png"
            }
        up_operator = [i.a.get('title') for i in soup_2.find('i', class_="fa-user-plus fas").parent.parent.contents[1].contents]

        for role in ark_role_data:
            Ark.role_class[role] = ark_role_data[role]['class']
            if '标准寻访' in ark_role_data[role]['approach']:
                if ark_role_data[role]['rarity'] == 6:
                    if role in up_operator:
                        Ark.up_role_6.append(role)
                    else:
                        Ark.role_6.append(role)
                elif ark_role_data[role]['rarity'] == 5:
                    if role in up_operator:
                        Ark.up_role_5.append(role)
                    else:
                        Ark.role_5.append(role)
                elif ark_role_data[role]['rarity'] == 4:
                    if role in up_operator:
                        Ark.up_role_4.append(role)
                    else:
                        Ark.role_4.append(role)
                elif ark_role_data[role]['rarity'] == 3:
                    Ark.role_3.append(role)
            elif role in up_operator and '限定寻访' in ark_role_data[role]['approach']:
                Ark.xd_role.append(role)

    ark_role_data['阿米娅(近卫)']['img_url'] = 'https://prts.wiki/images/8/85/半身像_阿米娅(近卫)_2.png'
    await _check_img('Arknights', ark_role_data)
    await _ckeck_extra_data('Arknights', Extra.arknights)

    dump_json(Config.role_path['Arknights'],**ark_role_data)
    logger.success('\033[36m明日方舟\033[0m \033[33m信息已更新\033[0m')
    


driver = nonebot.get_driver()
@driver.on_bot_connect
async def check_updata_all():
    async_tasks = [
        check_updata_Arknights(),
    
    ]
    await asyncio.wait(async_tasks)
    
# scheduler_updata = nonebot.require("nonebot_plugin_apscheduler").scheduler

# @scheduler_updata.scheduled_job('cron',hour=4,minute=1,)
# async def _():
#     await check_updata_all()

# @scheduler_updata.scheduled_job('cron',hour=16,minute=1,)
# async def _():
#     await check_updata_all()