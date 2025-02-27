from dataclasses import dataclass
from typing import List, Optional
from data.enums import ECraftingSkill, EMaterial, EItemType
from data.vrange import Range

@dataclass
class Material():
    item: EMaterial
    amount: int

@dataclass
class Recipe:
    item: EItemType
    skill: ECraftingSkill
    materials: List[Material]
    healthOrDamage: Range
    durability: Optional[Range]
    duration: Optional[Range]
    basicDuration: Optional[Range] 
    lvl: Range
    name: str
    id: int

    def __hash__(self):
        return hash((self.__class__.__name__, self.id))

    @classmethod
    def parse_recipe(cls, obj: dict) -> 'Recipe':
        item = obj["type"]
        skill = obj["skill"]
        materials = cls.parse_materials(obj["materials"])
        healthOrDamage = cls.parse_range(obj["healthOrDamage"])
        if "durability" in obj:
            durability = cls.parse_range(obj["durability"])
            duration = None
            basicDuration = None
        else:
            durability = None
            duration = cls.parse_range(obj["duration"])
            basicDuration = cls.parse_range(obj["basicDuration"])
        lvl = cls.parse_range(obj["lvl"])
        name = obj["name"]
        id = obj["id"]

        return Recipe(item = item,
                    skill = skill,
                    materials = materials,
                    healthOrDamage = healthOrDamage,
                    durability = durability,
                    duration = duration,
                    basicDuration = basicDuration,
                    lvl = lvl,
                    name = name,
                    id = id)

    @classmethod
    def parse_range(cls, srange: dict) -> Range:
        return Range(min = srange["minimum"], max = srange["maximum"])

    @classmethod
    def parse_materials(cls, materials: dict) -> List[Material]:
        return [Material(item = i["item"], amount = i["amount"]) for i in materials]



if __name__ == "__main__":
    pass
