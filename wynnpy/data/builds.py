from typing import Optional

from wynnpy.data.datacontainer import ItemsContainer, MainDataContainer
from wynnpy.data.enums import EAttackSpeed
from wynnpy.data.items import ItemIDs, Armor, Accessory, Weapon, Damage
from wynnpy.data.vrange import Range

class Build:

    atkSpd: Optional[EAttackSpeed]
    majorIDs: Optional[str]
    total_hp: float
    lvl: Range
    minimumReqIDs: ItemIDs
    item_list: list
    damage: Damage
    powderSlotsWeapon: Optional[int]
    powderSlotsArmorTotal: Optional[int]

    #todo dont pass all data container, but just items, replace def createbuild
    def __init__(self, items):
        self.atkSpd = None
        self.majorIDs = None
        self.total_hp = 0.0
        self.lvl = Range(0, 0)
        self.minimumReqIDs = ItemIDs(0, 0, 0, 0, 0, 0)
        self.item_list = []
        self.damage = Damage(
            nDam=Range(0, 0),
            eDam=Range(0, 0),
            tDam=Range(0, 0),
            wDam=Range(0, 0),
            fDam=Range(0, 0),
            aDam=Range(0, 0)
        )

        #todo something with that, get screwed idiot
        self.powderSlotsWeapon = None
        self.powderSlotsArmorTotal = None

        if isinstance(items, ItemsContainer):
            self.items = items
        elif isinstance(items, MainDataContainer):
            self.items = items.items
        else:
            raise ValueError("items: Invalid container type")

    def validatebuild(self) -> bool:
        max_items_by_type = {
            "WAND" : 1,
            "DAGGER": 1,
            "RELIK": 1,
            "BOW": 1,
            "SPEAR": 1,
            "HELMET": 1,
            "CHESTPLATE": 1,
            "LEGGINGS": 1,
            "BOOTS": 1,
            "RING": 2,
            "BRACELET": 1,
            "NECKLACE": 1
        }

        items_by_type = {key: 0 for key in max_items_by_type}
        weapon_types = set()
        weapon_count = 0

        for item in self.item_list:
            item_type = item.item.strip().upper()
            if item_type in items_by_type:
                items_by_type[item_type] += 1
                if items_by_type[item_type] > max_items_by_type[item_type]:
                    print(f"Too many - {item_type} !")
                    return False
            if item_type in ["WAND", "DAGGER", "RELIK", "BOW", "SPEAR"]:
                weapon_types.add(item_type)
                weapon_count += 1

        if len(weapon_types) > 1:
            print("More then 1 type of weapon in build!")
            return False
        if weapon_count > 1:
            print("Too many weapons in the build!")
            return False

        return True

    #todo remove it
    def createbuild(self, ids: list[int]):

        for item in ids:
            self.item_list.append(self.items.byID(item))

    def calculatebuild(self):

        #todo move validate
        if not self.validatebuild():
            return None

        min_lvl, max_lvl = 0, 0

        #todo make __add__ __iadd__ in damage class or maybe not

        for item in self.item_list:
            min_lvl = min(min_lvl, item.lvl)
            max_lvl = max(max_lvl, item.lvl)
            self.majorIDs = item.majorIDs
            if isinstance(item, Armor):
                #print(f"Item is an Armor: {vars(item)}")
                #print(f"type of obj: {type(item)}")
                self.minimumReqIDs += item.itemIDs
                self.total_hp += item.hp.min
                print(f"Armor {item.id} ({item.name}) IDs: {item.ids}")
            elif isinstance(item, Weapon):
                print(f"Weapon {item.id} ({item.name}) IDs: {item.ids}")
            elif isinstance(item, Accessory):
                print(f"Accessory {item.id} ({item.name}) IDs: {item.ids}")
                self.total_hp += item.hp.min
            else:
                raise ValueError(f"Invalid item type: {item.item}")

        self.lvl = Range(min_lvl, max_lvl)

    def typebuild(self):
        print(" Build:")
        print(f"Stat required: Strength: {self.minimumReqIDs.strReq}, Dexterity: {self.minimumReqIDs.dexReq}, "
              f"Intelligence: {self.minimumReqIDs.intReq}, Defense: {self.minimumReqIDs.defReq}, "
              f"Agility: {self.minimumReqIDs.agiReq}")
        print(f"Total hp: {self.total_hp}")
        print(f"lvl range: {self.lvl.min} - {self.lvl.max}")
        print(f"Majors: {self.majorIDs}")
        build_items = [f"{item.name} ({item.item} {item.id})" for item in self.item_list]
        print(f"Items: {', '.join(build_items)}")