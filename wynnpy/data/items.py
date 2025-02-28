from dataclasses import dataclass
from typing import List, Optional, Dict
from .enums import EID, EAttackSpeed, EItemTier, EItemRestrict, EItemType, EItemCategory
from typing import Optional, Dict
from .vrange import Range
import math

@dataclass
class ItemIDs:
    durability: int
    strReq: int
    dexReq: int
    intReq: int
    defReq: int
    agiReq: int

    def __add__(self, other: 'ItemIDs'):
        if isinstance(other, ItemIDs):
            return ItemIDs(self.durability + other.durability,
                        self.strReq + other.strReq,
                        self.dexReq + other.dexReq,
                        self.intReq + other.intReq,
                        self.defReq + other.defReq,
                        self.agiReq + other.agiReq)
        else:
            raise ValueError("Types no good for +")

    def __iadd__(self, other: 'ItemIDs'):
        self.durability += other.durability,
        self.strReq += other.strReq,
        self.dexReq += other.dexReq,
        self.intReq += other.intReq,
        self.defReq += other.defReq,
        self.agiReq += other.agiReq
        return self

    def __mul__(self, number: int | float) -> 'ItemIDs':

        if isinstance(number, int) or isinstance(number, float):
            return ItemIDs(self.durability, 
                           self.strReq * number,
                           self.dexReq * number,
                           self.intReq * number,
                           self.defReq * number,
                           self.agiReq * number)
        else:
            raise ValueError("Types no good for *")
    
    def __imul__(self, number: int | float):
        if isinstance(number, int) or isinstance(number, float):
            self.durability,
            self.strReq *= number,
            self.dexReq *= number,
            self.intReq *= number,
            self.defReq *= number,
            self.agiReq *= number
            return self
        else:
            raise ValueError("Types no good for *")

    def floor(self):           
        return ItemIDs(math.floor(self.durability), 
                       math.floor(self.strReq),
                       math.floor(self.dexReq),
                       math.floor(self.intReq),
                       math.floor(self.defReq),
                       math.floor(self.agiReq))
    
    def round(self):
        return ItemIDs(round(self.durability), 
                       round(self.strReq),
                       round(self.dexReq),
                       round(self.intReq),
                       round(self.defReq),
                       round(self.agiReq))

@dataclass
class Damage:
    nDam: Range
    eDam: Range
    tDam: Range
    wDam: Range
    fDam: Range
    aDam: Range

@dataclass
class Item:
    category: EItemCategory
    name: str
    item: EItemType
    itemIDs: ItemIDs
    lvl: Range
    ids: Dict[EID, Range] 
    tier: EItemTier 
    displayName: str
    restrict: List[EItemRestrict]
    majorIDs: Optional[str]
    id: int

    def __hash__(self):
        return hash((self.__class__.__name__, self.id))
    
    def __eq__(self, other):
        return self.__class__.__name__ == other.__class__.__name__ and self.id == other.id
    
    #Move this to utils 
    @classmethod
    def fing_missing_keys(cls, data: dict):
        existing_keys = {id_enum.value for id_enum in EID}
        exclude_keys = {"icon", "lvl", "armourMaterial", "name", "id", "slots", "atkSpd", "tier", "lore", "drop", "majorIds", "nDam", "fDam", "displayName", "restrict", "quest",
                        "allowCraftsman", "agiReq", "aDam", "tDam", "wDam", "dexReq", "eDam", "intReq", "strReq", "type", "classReq", "averageDps", "armourColor", "category",
                        "defReq", "dropInfo", "fixID"}
        missing_keys = set()

        for item in data["items"]:
            for key in item.keys():
                if key not in existing_keys and key not in exclude_keys:
                    missing_keys.add(key)
        
        return missing_keys

@dataclass    
class Weapon(Item):
    damage: Damage
    atkSpd: EAttackSpeed
    powderSlots: Optional[int]

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        return super().__eq__()

@dataclass
class Armor(Item):
    hp: Range
    powderSlots: Optional[int]
    
    def __hash__(self):
        return super().__hash__()
    
    def __eq__(self, other):
        return super().__eq__()

@dataclass
class Accessory(Item):
    
    def __hash__(self):
        return super().__hash__()
    
    def __eq__(self, other):
        return super().__eq__()

if __name__ == "__main__":
    pass