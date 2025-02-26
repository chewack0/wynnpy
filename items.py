from dataclasses import dataclass
from typing import List, Optional, Dict
from enums import EID, EAttackSpeed, EItemTier, EItemRestrict, EItemType
from typing import Optional, Dict
from vrange import Range

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
    name: str
    item: EItemType
    damage: Optional[Damage]
    itemIDs: ItemIDs
    atkSpd: Optional[EAttackSpeed] 
    lvl: int
    ids: Dict[EID, Range] 
    tier: EItemTier 
    powderSlots: Optional[int]
    displayName: str
    restrict: List[EItemRestrict]
    majorIDs: Optional[str]
    id: int

    def __hash__(self):
        return hash((self.__class__.__name__, self.id))
    
    @classmethod
    def parse_range(cls, value: str) -> Optional[Range]:
        if value == "0-0":
            return None
        min_vlaue, max_value = map(int, value.split("-"))
        return Range(min = min_vlaue, max = max_value)

    @classmethod
    def parse_damage(cls, data: dict) -> Damage:
        return Damage(
            nDam = cls.parse_range(data.get("nDam", "0-0")),
            eDam = cls.parse_range(data.get("eDam", "0-0")),
            tDam = cls.parse_range(data.get("tDam", "0-0")),
            wDam = cls.parse_range(data.get("wDam", "0-0")),
            fDam = cls.parse_range(data.get("fDam", "0-0")),
            aDam = cls.parse_range(data.get("aDam", "0-0"))
        )

    @classmethod
    def parse_itemids(cls, data: dict) -> ItemIDs:
        return ItemIDs(
            durability = data.get("durability", 0),
            strReq = data.get("strReq", 0),
            dexReq = data.get("dexReq", 0),
            intReq = data.get("intReq", 0),
            defReq = data.get("defReq", 0),
            agiReq = data.get("agiReq", 0)
        )

    #...?
    @classmethod
    def parse_ids(cls, data: dict) -> Dict[EID, Range]:
        parsed_ids = {}
        fixed_keys = {"agi", "str", "dex", "int", "def"}
        reversed_keys = { "spPct1", "spPct2", "spPct3", "spPct4", "spRaw1", "spRaw2", "spRaw3", "spRaw4"}

        for key, value in data.items():
            for id_enum in EID:
                if id_enum.value == key:
                    if data.get("fixID"):
                        parsed_ids[id_enum] = Range(value, value)
                    elif key in fixed_keys:
                        parsed_ids[id_enum] = Range(value, value)
                    elif key in reversed_keys:
                        if value <= 0:
                            parsed_ids[id_enum] = Range(value*0.3, value*1.3).round()
                        else:
                            parsed_ids[id_enum] = Range(value*1.3, value*0.7).round()
                    else:
                        if value >= 0:
                            parsed_ids[id_enum] = Range(value*0.3, value*1.3).round()
                        else:
                            parsed_ids[id_enum] = Range(value*1.3, value*0.7).round()

        return parsed_ids 

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

#function transfer item from JSON to class Item
    @classmethod
    def parse_item(cls, data: dict) -> 'Item':
        restricts = []
        if "restirct" in data and data["restirct"].lower() == "untredable":
            restricts.append(EItemRestrict.UNTRADABLE)
        if "quest" in data:
            restricts.append(EItemRestrict.QUESTITEM)
        if "allowCraftsman" in data and data["allowCraftsman"]:
            restricts.append(EItemRestrict.ALLOWCRAFTSMAN)

        return Item(
            name = data["name"],
            item = data["type"].upper(),
            damage = cls.parse_damage(data),
            itemIDs = cls.parse_itemids(data), 
            atkSpd = EAttackSpeed[data["atkSpd"].upper()] if "atckSpd" in data else None,
            lvl = data["lvl"],
            ids = cls.parse_ids(data),
            tier = EItemTier[data["tier"].upper()],
            powderSlots = data.get("slots", 0),
            displayName = data["name"],
            restrict = restricts,
            majorIDs = data.get("majorIds", None),
            id = data["id"]
        )
    
            

if __name__ == "__main__":
    pass