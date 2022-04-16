
def load_json(path:...):...


class Ark:
    """明日方舟抽卡数据"""
    role_class: dict = {}
    """干员职业"""
    role_6: list = []
    """6星干员列表"""
    role_5: list = []
    """5星干员列表"""
    role_4: list = []
    """4星干员列表"""
    role_3: list = []
    """3星干员列表"""
    up_role_6: list = []
    """UP6星干员列表"""
    up_role_5: list = []
    """UP5星干员列表"""
    up_role_4: list = []
    """UP4星干员列表"""
    xd_role: list = []
    """限定干员列表"""
    cache: dict = {}
    """抽卡缓存数据"""
    @classmethod
    def reload(cls):
        cls.role_class: dict = {}
        cls.role_6: list = []
        cls.role_5: list = []
        cls.role_4: list = []
        cls.role_3: list = []
        cls.up_role_6: list = []
        cls.up_role_5: list = []
        cls.up_role_4: list = []
        cls.xd_role: list = []

class Gen:
    """原神抽卡数据"""
    p5: float = 0.006
    """5星概率"""
    p4: float = 0.051
    """4星概率"""
    p3: float = 0.943
    """3星概率"""

    b4: int = 10
    """4星保底次数"""
    b5: int = 90
    """5星保底次数"""
    bd: int = 180
    """up保底次数"""
    role_5: list = []
    role_4: list = []
    role_u: list = []

    item_5: list = []
    item_4: list = []
    item_3: list = []
    item_u: list = []

