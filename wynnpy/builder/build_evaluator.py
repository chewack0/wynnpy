from typing import Optional

from wynnpy.data.datacontainer import ItemsContainer, MainDataContainer
from wynnpy.data.enums import EAttackSpeed, EItemType
from wynnpy.data.items import ItemIDs, Armor, Accessory, Weapon, Damage
from wynnpy.data.vrange import Range

class BuildEvaluator:

    atkSpd: Optional[EAttackSpeed]
    majorIDs: Optional[str]
    total_hp: float
    lvl: Range
    minimumReqIDs: ItemIDs
    damage: Damage
    powderSlotsWeapon: Optional[int]
    powderSlotsArmorTotal: Optional[int]

    helmet: Optional[Armor]
    chestplate: Optional[Armor]
    leggings: Optional[Armor]
    boots: Optional[Armor]
    ring1: Optional[Accessory]
    ring2: Optional[Accessory]
    bracelet: Optional[Accessory]
    necklace: Optional[Accessory]
    weapon: Optional[Weapon]

    #todo dont pass all data container, but just items, replace def createbuild
    def __init__(self, helmet = None, chestplate = None, leggings = None, boots = None,
                 ring1 = None, ring2 = None, bracelet = None, necklace = None, weapon = None):
        self.atkSpd = None
        self.majorIDs = None
        self.total_hp = 0.0
        self.lvl = Range(0, 0)
        self.minimumReqIDs = ItemIDs(0, 0, 0, 0, 0, 0)
        self.damage = Damage(
            nDam=Range(0, 0),
            eDam=Range(0, 0),
            tDam=Range(0, 0),
            wDam=Range(0, 0),
            fDam=Range(0, 0),
            aDam=Range(0, 0)
        )
        self.helmet = helmet
        self.chestplate = chestplate
        self.leggings = leggings
        self.boots = boots
        self.ring1 = ring1
        self.ring2 = ring2
        self.bracelet = bracelet
        self.necklace = necklace
        self.weapon = weapon

        #todo something with that, get screwed idiot
        self.powderSlotsWeapon = None
        self.powderSlotsArmorTotal = None

    #IDK which staticmethod should I use tbh
    @staticmethod
    def create_build(*items):
        rings = [item for item in items if isinstance(item, Accessory) and item.item == EItemType.RING]

        build = BuildEvaluator(
            helmet = next((item for item in items if isinstance(item, Armor) and item.item == EItemType.HELMET), None),
            chestplate = next((item for item in items if isinstance(item, Armor) and item.item == EItemType.CHESTPLATE), None),
            leggings = next((item for item in items if isinstance(item, Armor) and item.item == EItemType.LEGGINGS), None),
            boots = next((item for item in items if isinstance(item, Armor) and item.item == EItemType.BOOTS), None),
            ring1 = rings[0] if len(rings) > 0 else None,
            ring2 = rings[1] if len(rings) > 1 else None,
            bracelet = next((item for item in items if isinstance(item, Accessory) and item.item == EItemType.BRACELET), None),
            necklace = next((item for item in items if isinstance(item, Accessory) and item.item == EItemType.NECKLACE), None),
            weapon = next((item for item in items if isinstance(item, Weapon)), None),
        )
        return build

    @staticmethod
    def create_build_fancy(*items):
        build = BuildEvaluator()
        for item in items:
            if isinstance(item, Armor):
                build.assign_armor(item)
            elif isinstance(item, Accessory):
                build.assign_accessory(item)
            elif isinstance(item, Weapon):
                build.assign_weapon(item)
            else:
                raise ValueError(f"Unknown item type: {item.name}")
        return build

    def assign_armor(self, item):
        item_type = item.item

        if item_type == EItemType.HELMET:
            if not self.helmet:
                self.helmet = item
            else:
                raise ValueError(f"Too many: {EItemType.HELMET} , can't add item: {item.name}")

        elif item_type == EItemType.CHESTPLATE:
            if not self.chestplate:
                self.chestplate = item
            else:
                raise ValueError(f"Too many: {EItemType.CHESTPLATE}, can't add item: {item.name}")

        elif item_type == EItemType.LEGGINGS:
            if not self.leggings:
                self.leggings = item
            else:
                raise ValueError(f"Too many: {EItemType.LEGGINGS}, can't add item: {item.name}")

        elif item_type == EItemType.BOOTS:
            if not self.boots:
                self.boots = item
            else:
                raise ValueError(f"Too many: {EItemType.BOOTS}, can't add item: {item.name}")

        else:
            raise ValueError(f"Invalid item type: {item_type} in item: {item.name}")

    def assign_accessory(self, item):
        item_type = item.item

        if item_type == EItemType.RING:
            if not self.ring1:
                self.ring1 = item
            elif not self.ring2:
                self.ring2 = item
            else:
                raise ValueError(f"Too many: {EItemType.RING}, can't add item: {item.name}")

        elif item_type == EItemType.BRACELET:
            if not self.bracelet:
                self.bracelet = item
            else:
                raise ValueError(f"Too many: {EItemType.BRACELET}, can't add item: {item.name}")

        elif item_type == EItemType.NECKLACE:
            if not self.necklace:
                self.necklace = item
            else:
                raise ValueError(f"Too many: {EItemType.NECKLACE}, can't add item: {item.name}")

        else:
            raise ValueError(f"Invalid item type: {item_type} in item: {item.name}")

    def assign_weapon(self, item):
        if not self.weapon:
            self.weapon = item
        else:
            raise ValueError(f"Too many weapons, can't add item: {item.name}")

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