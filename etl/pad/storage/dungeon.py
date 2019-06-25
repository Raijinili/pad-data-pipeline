from typing import List

from pad.db.sql_item import SimpleSqlItem
from pad.raw_processor.crossed_data import CrossServerDungeon


class Dungeon(SimpleSqlItem):
    """Dungeon top-level item."""
    TABLE = 'dungeons'
    KEY_COL = 'dungeon_id'

    @staticmethod
    def from_csd(o: CrossServerDungeon) -> 'Dungeon':
        return Dungeon(
            dungeon_id=o.dungeon_id,
            name_jp=o.jp_dungeon.clean_name,
            name_na=o.na_dungeon.clean_name,
            name_kr=o.kr_dungeon.clean_name,
            dungeon_type=o.jp_dungeon.full_dungeon_type.value,
            visible=True)

    def __init__(self,
                 dungeon_id: int = None,
                 name_jp: str = None,
                 name_na: str = None,
                 name_kr: str = None,
                 dungeon_type: int = None,
                 visible: bool = None,
                 tstamp: int = None):
        self.dungeon_id = dungeon_id
        self.name_jp = name_jp
        self.name_na = name_na
        self.name_kr = name_kr
        self.dungeon_type = dungeon_type
        self.visible = visible
        self.tstamp = tstamp


def _non_auto_update_cols(self):
    return ['visible']


class SubDungeon(SimpleSqlItem):
    """Per-difficulty dungeon section."""
    TABLE = 'sub_dungeons'
    KEY_COL = 'sub_dungeon_id'

    @staticmethod
    def from_csd(o: CrossServerDungeon) -> List['SubDungeon']:
        results = []
        for sd in o.sub_dungeons:
            results.append(SubDungeon(
                sub_dungeon_id=sd.sub_dungeon_id,
                dungeon_id=o.dungeon_id,
                name_jp=sd.jp_sub_dungeon.clean_name,
                name_na=sd.na_sub_dungeon.clean_name,
                name_kr=sd.kr_sub_dungeon.clean_name,
                floors=sd.jp_sub_dungeon.floors,
                stamina=sd.jp_sub_dungeon.stamina,
                hp_mult=sd.jp_sub_dungeon.hp_mult,
                atk_mult=sd.jp_sub_dungeon.atk_mult,
                def_mult=sd.jp_sub_dungeon.def_mult,
                s_rank=sd.jp_sub_dungeon.score))
        return results

    def __init__(self,
                 sub_dungeon_id: int = None,
                 dungeon_id: int = None,
                 name_jp: str = None,
                 name_na: str = None,
                 name_kr: str = None,
                 floors: int = None,
                 stamina: int = None,
                 hp_mult: float = None,
                 atk_mult: float = None,
                 def_mult: float = None,
                 s_rank: int = None,
                 tstamp: int = None):
        self.sub_dungeon_id = sub_dungeon_id
        self.dungeon_id = dungeon_id
        self.name_jp = name_jp
        self.name_na = name_na
        self.name_kr = name_kr
        self.floors = floors
        self.stamina = stamina
        self.hp_mult = hp_mult
        self.atk_mult = atk_mult
        self.def_mult = def_mult
        self.s_rank = s_rank
        self.tstamp = tstamp
