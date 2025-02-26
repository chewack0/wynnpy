from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
from enums import ID, CraftingSkill 
from vrange import Range
from items import ItemIDs
import json
import math

@dataclass
class ConsumableIDs:
    durability: int
    charges: int

@dataclass
class PosMods:
    left: int
    right: int
    above: int
    under: int
    touching: int
    notTouching: int

@dataclass
class Ingredient:
    name: str
    #type: str
    lvl: int
    skills: List[CraftingSkill]
    #icon: None
    ids: Dict[ID, Range] #TODO rewrite as dict 
    tier: int
    consumableIDs: ConsumableIDs
    posMods: PosMods
    itemIDs: ItemIDs
    displayName: str
    id: int
    
    @classmethod
    def parse_ing(cls, obj: dict) -> 'Ingredient':
        
        name = obj["name"]
        lvl = obj["lvl"]
        skills = cls.parse_skills(obj["skills"])
        ids = cls.parse_ids(obj["ids"])
        consumableIDs = cls.parse_consumableIDs(obj["consumableIDs"])
        tier = obj["tier"] 
        posMods = cls.parse_posMods(obj["posMods"])
        itemIDs = cls.parse_itemIDs(obj["itemIDs"])
        displayName = obj["displayName"]
        id = obj["id"]

        return Ingredient(name=name, 
                        lvl=lvl, 
                        skills=skills, 
                        ids=ids, 
                        consumableIDs = consumableIDs,
                        tier = tier,
                        posMods = posMods, 
                        itemIDs= itemIDs, 
                        displayName = displayName, 
                        id = id)
            
    @classmethod
    def parse_range(cls, srange: dict) -> Range:
        return Range(min = srange["minimum"], max = srange["maximum"])

    @classmethod
    def parse_skills(cls, skills: List[str]) -> List[CraftingSkill]:
        return [CraftingSkill(skill) for skill in skills]

    @classmethod
    def parse_ids(cls, ids: dict) -> Dict[ID, Range]:
        return {ID(id): cls.parse_range(ids[id]) for id in ids}

    @classmethod
    def parse_consumableIDs(cls, consumableIDs: dict) -> ConsumableIDs:
        return ConsumableIDs(durability = consumableIDs["dura"], 
                            charges = consumableIDs["charges"])

    @classmethod
    def parse_posMods(cls, posmods: dict) -> PosMods:
        return PosMods(left = posmods["left"],
                    right = posmods["right"],
                    above = posmods["above"],
                    under = posmods["under"],
                    touching = posmods["touching"],
                    notTouching = posmods["notTouching"])

    @classmethod
    def parse_itemIDs(cls, itemIDs: dict) -> ItemIDs:
        return ItemIDs(durability = itemIDs["dura"],
                    strReq = itemIDs["strReq"],
                    dexReq = itemIDs["dexReq"],
                    intReq = itemIDs["intReq"],
                    defReq = itemIDs["defReq"],
                    agiReq = itemIDs["agiReq"])



if __name__ == "__main__":
    pass
