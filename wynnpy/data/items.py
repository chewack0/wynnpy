from dataclasses import dataclass
from typing import List, Optional, Dict
from .enums import EID, EAttackSpeed, EItemTier, EItemRestrict, EItemType, EItemCategory
from typing import Optional, Dict
from .vrange import Range

@dataclass
class ItemIDs:
    durability: int
    strReq: int
    dexReq: int
    intReq: int
    defReq: int
    agiReq: int

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
    lvl: int
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
    hp: int
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