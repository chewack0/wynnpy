import json
from typing import List, Dict, Optional
import logging 
from .items import Weapon, Accessory, Armor, Damage, ItemIDs, Item
from .ingreds import Ingredient
from .recipes import Recipe
from .enums import EItemCategory, EAttackSpeed, EItemTier, EID, EItemRestrict
from .vrange import Range


class ItemFactory:



    def __init__(self):
        pass
    
    
    @classmethod
    def parse(cls, obj: dict) -> Weapon | Armor | Accessory:
        item_factories = {EItemCategory.WEAPON: cls.parse_weapon,
                        EItemCategory.ARMOR: cls.parse_armor,
                        EItemCategory.ACCESSORY: cls.parse_accessory}
        
        #logging.info(obj)
        if obj["category"] in [item.value for item in EItemCategory]:
            return item_factories[EItemCategory(obj["category"])](obj)
        else:
            logging.warning(f"{obj["category"]} is not a valid category...")

    @classmethod
    def parse_weapon(cls, data: dict) -> Weapon:
        return Weapon(
            name = data["name"],
            category = EItemCategory.WEAPON,
            item = data["type"].upper(),
            damage = cls.parse_damage(data),
            itemIDs = cls.parse_itemids(data), 
            atkSpd = EAttackSpeed[data["atkSpd"].upper()],
            lvl = data["lvl"],
            ids = cls.parse_ids(data),
            tier = EItemTier[data["tier"].upper()],
            powderSlots = data.get("slots", 0),
            displayName = data["name"],
            restrict = cls.parse_restricts(data),
            majorIDs = data.get("majorIds", None),
            id = data["id"])

    @classmethod
    def parse_armor(cls, data: dict) -> Armor:
        return Armor(
            name = data["name"],
            category = EItemCategory.ARMOR,
            item = data["type"].upper(),
            itemIDs = cls.parse_itemids(data), 
            lvl = data["lvl"],
            hp = Range.fromint(data.get("hp", 0)),
            ids = cls.parse_ids(data),
            tier = EItemTier[data["tier"].upper()],
            powderSlots = data.get("slots", 0),
            displayName = data["name"],
            restrict = cls.parse_restricts(data),
            majorIDs = data.get("majorIds", None),
            id = data["id"]
        )
    
    @classmethod
    def parse_accessory(cls, data: dict) -> Accessory:
        return Accessory(
            name = data["name"],
            category = EItemCategory.ACCESSORY,
            item = data["type"].upper(),
            itemIDs = cls.parse_itemids(data), 
            lvl = data["lvl"],
            ids = cls.parse_ids(data),
            tier = EItemTier[data["tier"].upper()],
            displayName = data["name"],
            restrict = cls.parse_restricts(data),
            majorIDs = data.get("majorIds", None),
            id = data["id"]
        )

    @classmethod
    def parse_range(cls, value: str) -> Optional[Range]:
        if value == "0-0":
            return Range(0, 0)
        min_value, max_value = map(int, value.split("-"))
        return Range(min = min_value, max = max_value)

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
    def parse_restricts(cls, data: dict) -> List[EItemRestrict]:
        restricts = []
        if "restirct" in data and data["restirct"].lower() == "untredable":
            restricts.append(EItemRestrict.UNTRADABLE)
        if "quest" in data:
            restricts.append(EItemRestrict.QUESTITEM)
        if "allowCraftsman" in data and data["allowCraftsman"]:
            restricts.append(EItemRestrict.ALLOWCRAFTSMAN)
        return restricts


def parse_items(path: str) -> List[Item]:
    items = list()
    with open(path) as data:
        data = json.load(data)["items"]
        counter = 1
        for item in data:
            logging.info(f"[{counter}] Parsing item... {item["name"]} id: {item["id"]}")
            items.append(ItemFactory.parse(item))
            counter += 1
        #ingredients.append(Ingredient.empty())
    print(len(items))
    return items

def parse_ingredients(path: str) -> List[Ingredient]:
    ingredients = list()
    with open(path) as data:
        data = json.load(data)
        counter = 1
        for ing in data:
            logging.info(f"[{counter}] Parsing ingredient... {ing["name"]} id: {ing["id"]}")
            ingredients.append(Ingredient.parse_ing(ing))
            counter += 1
        ingredients.append(Ingredient.empty())
    return ingredients

def parse_recipes(path: str) -> List[Recipe]:
    recipes = list()
    with open(path) as data:
        data = json.load(data)
        counter = 1
        for recipe in data["recipes"]:
            logging.info(f"[{counter}] Parsing recipe... {recipe["name"]}  id: {recipe["id"]}")
            recipes.append(Recipe.parse_recipe(recipe))
            counter += 1
        return recipes
