import base64
from httpx import AsyncClient

from MUZI.config import PLUGIN_CONFIG

size = PLUGIN_CONFIG["setu"]["size"]
proxy = PLUGIN_CONFIG["setu"]["proxy"]

async def get_setu(keyword="", r18=False):
    async with AsyncClient() as client:
        req_url = "https://api.lolicon.app/setu/v2"
        params = {
            "keyword": keyword,
            "r18": 1 if r18 else 0,
            "size": size,
            "proxy": proxy,
        }
        try:
            res = await client.get(req_url, params=params, timeout=120)
            setu_url = res.json()["data"][0]["urls"]["regular"]
            content = await _down_pic(setu_url)
            if content:
                base64_str = base64.b64encode(content).decode()
                return f"[CQ:image,file=base64://{base64_str}]"
        except:
            return False

async def _down_pic(url):
    async with AsyncClient(proxies=None) as client:
        headers = {
            "Referer": "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        }
        re = await client.get(url=url, headers=headers, timeout=120)
        if re.status_code == 200:
            return re.content