import yaml
from pathlib import Path
from nonebot.log import logger

def load_yml(file: Path, encoding="utf-8") -> dict:
    with open(file, "r", encoding=encoding) as f:
        data = yaml.safe_load(f)
    return data

def dump_yml(file: Path, **data) -> None:
    with file.open('w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)


DATA_DIR = Path("./data").absolute()
CONFIG_PATH = Path("./config.yml").absolute()
PLUGIN_SETTING_PATH = DATA_DIR / "plugin_setting.yml"
PLUGIN_USAGE_PATH = DATA_DIR / "plugin_usage.yml"


START_CONFIG = {
    "host": "127.0.0.1",
    "port": 8080,
    "debug": False,
    "superusers": ["123456789","987654321"],
    "nickname": ["awsomebot","bot"],
    "command_start": ["","/"],
    "command_sep": [";","&"],
    "session_expire_timeout": 60,
    "api_timeout": 30
}
PLUGIN_CONFIG = {
    "setu":{
        "proxy": "i.pixiv.re",
    },
    "report":{
        "bindgroup":['20000000','10000000']
    }
}
PLUGIN_CONFIG

if not DATA_DIR.exists():
    DATA_DIR.mkdir()
if not CONFIG_PATH.is_file(): 
    dump_yml(CONFIG_PATH, **{"StartConfig": START_CONFIG, "PluginConfig": PLUGIN_CONFIG})
    logger.warning("配置文件config.yml不存在 已自动生成")
    logger.success("已使用默认配置启动")
if not PLUGIN_SETTING_PATH.is_file():
    dump_yml(PLUGIN_SETTING_PATH, **{})
    logger.warning("配置文件plugin_setting.yml不存在 已自动生成")
if not PLUGIN_USAGE_PATH.is_file():
    dump_yml(PLUGIN_USAGE_PATH, **{"default":{}, "optional":{}})



CONFIG = load_yml(CONFIG_PATH)
PLUGIN_SETTING = load_yml(PLUGIN_SETTING_PATH)
PLUGIN_USAGE = load_yml(PLUGIN_USAGE_PATH)
START_CONFIG.update(CONFIG["StartConfig"])
PLUGIN_CONFIG.update(CONFIG["PluginConfig"])
    
_DEF_PLUGINS = PLUGIN_USAGE["default"] if PLUGIN_USAGE["default"] else {}
_OPT_PLUGINS = PLUGIN_USAGE["optional"] if PLUGIN_USAGE["optional"] else {}
PLUGIN_DESCRIBE = dict(_DEF_PLUGINS,**_OPT_PLUGINS)


class BotInfo:
    name: str = START_CONFIG["nickname"][0]
    nickname: str = START_CONFIG["nickname"]
    superuser: list = START_CONFIG["superusers"]
    bindgroup: list = PLUGIN_CONFIG["report"].get("bindgroup",[])
    
    default_plugin: list = list(_DEF_PLUGINS.keys())
    optional_plugin: list = list(_OPT_PLUGINS.keys())
    plugin_describe: dict = PLUGIN_DESCRIBE
    plugins_setting: dict = PLUGIN_SETTING if PLUGIN_SETTING else {}
    plugins: list = default_plugin + optional_plugin

    @classmethod
    def update_plugin_setting(cls, **data):
        """更新 plugin_setting"""
        cls.plugins_setting.update(data)
        dump_yml(PLUGIN_SETTING_PATH, **data)

if len(BotInfo.plugins_setting) != len(BotInfo.optional_plugin):
    data = {}
    for p in BotInfo.optional_plugin:
        data[p] = BotInfo.plugins_setting.get(p,[])
    BotInfo.update_plugin_setting(**data)