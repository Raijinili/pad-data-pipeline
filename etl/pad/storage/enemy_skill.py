from dadguide_proto.enemy_skills_pb2 import MonsterBehavior
from pad.db.sql_item import SimpleSqlItem
from pad.raw_processor.crossed_data import CrossServerESInstance
from pad.raw.skills.jp.enemy_skill_text import JpESTextConverter
from pad.raw.skills.en.enemy_skill_text import EnESTextConverter
#from pad.raw.skills.kr.enemy_skill_text import KrESTextConverter

class EnemySkill(SimpleSqlItem):
    """Enemy skill data."""
    TABLE = 'enemy_skills'
    KEY_COL = 'enemy_skill_id'

    @staticmethod
    def from_json(o):
        return EnemySkill(enemy_skill_id=o['enemy_skill_id'],
                          name_ja=o['name_ja'],
                          name_en=o['name_en'],
                          name_ko=o['name_ko'],
                          desc_ja=o['desc_ja'],
                          desc_en=o['desc_en'],
                          desc_ko=o['desc_ko'],
                          min_hits=o['min_hits'],
                          max_hits=o['max_hits'],
                          atk_mult=o['atk_mult'])

    @staticmethod
    def from_cseb(o: CrossServerESInstance) -> 'EnemySkill':
        exemplar = o.jp_skill.behavior

        has_attack = hasattr(exemplar, 'attack') and exemplar.attack
        min_hits = exemplar.attack.min_hits if has_attack else 0
        max_hits = exemplar.attack.max_hits if has_attack else 0
        atk_mult = exemplar.attack.atk_multiplier if has_attack else 0

        ja_desc = exemplar.full_description(JpESTextConverter())
        en_desc = exemplar.full_description(EnESTextConverter())
       #ko_desc = exemplar.full_description(KrESTextConverter())
        
        return EnemySkill(
            enemy_skill_id=o.enemy_skill_id,
            name_ja=o.jp_skill.name,
            name_en=o.na_skill.name,
            name_ko=o.kr_skill.name,
            desc_ja=ja_desc,
            desc_en=en_desc,
            desc_ko=en_desc,
            min_hits=min_hits,
            max_hits=max_hits,
            atk_mult=atk_mult)

    def __init__(self,
                 enemy_skill_id: int = None,
                 name_ja: str = None,
                 name_en: str = None,
                 name_ko: str = None,
                 desc_ja: str = None,
                 desc_en: str = None,
                 desc_ko: str = None,
                 min_hits: int = None,
                 max_hits: int = None,
                 atk_mult: int = None,
                 tstamp: int = None):
        self.enemy_skill_id = enemy_skill_id
        self.name_ja = name_ja
        self.name_en = name_en
        self.name_ko = name_ko
        self.desc_ja = desc_ja
        self.desc_en = desc_en
        self.desc_ko = desc_ko
        self.min_hits = min_hits
        self.max_hits = max_hits
        self.atk_mult = atk_mult
        self.tstamp = tstamp

    def __str__(self):
        return 'EnemySkill({}): {} - {}'.format(self.key_value(), self.name_en, self.desc_en)


class EnemyData(SimpleSqlItem):
    """Enemy skill data."""
    TABLE = 'enemy_data'
    KEY_COL = 'enemy_id'

    @staticmethod
    def from_mb(o: MonsterBehavior, status: int) -> 'EnemyData':
        return EnemyData(
            enemy_id=o.monster_id,
            status=status,
            behavior=o.SerializeToString())

    def __init__(self,
                 enemy_id: int = None,
                 status: int = None,
                 behavior: str = None,
                 tstamp: int = None):
        self.enemy_id = enemy_id
        self.status = status
        self.behavior = behavior
        self.tstamp = tstamp

    def __str__(self):
        return 'EnemyData({}): {}'.format(self.key_value(), len(self.behavior))
