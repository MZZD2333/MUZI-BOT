import json
from pathlib import Path
from typing import Dict, List

from MUZI.config import DATA_DIR


def dump_json(path: Path,**data):
    with open(path,'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



class Config:
    games: list = ['Arknights']
    gamedraw_dir: Path = DATA_DIR / 'gamedraw'
    role_path: Dict[str, Path] = {
    'Arknights' : Path(gamedraw_dir) / 'Arknights.json',
    }
    image_path: Dict[str, Path] = {
    'Arknights' : Path(gamedraw_dir) / 'Arknights'
    }
    extra_data_path: Dict[str, Path] = {
    'Arknights' : Path(gamedraw_dir) / 'Arknights' / 'Extra',
    }


if not Config.gamedraw_dir.exists():
    Config.gamedraw_dir.mkdir()


for path in Config.role_path.values():
    if not path.exists():
        dump_json(path,**{})  
for path in Config.image_path.values():
    if not path.exists():
        path.mkdir() 
for path in Config.extra_data_path.values():
    if not path.exists():
        path.mkdir() 



