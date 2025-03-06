import warnings
from typing import Optional

from wynnpy.data.enums import EAttackSpeed, EItemType
from wynnpy.data.items import ItemIDs, Armor, Accessory, Weapon, Damage
from wynnpy.data.vrange import Range

def validate_build(*items) -> bool:
    armor_types = [EItemType.HELMET, EItemType.CHESTPLATE, EItemType.LEGGINGS, EItemType.BOOTS]
    accessory_types = [EItemType.BRACELET, EItemType.NECKLACE]

    for armor_type in armor_types:
        armors_of_type = [item for item in items if isinstance(item, Armor) and item.item == armor_type.value]
        if len(armors_of_type) > 1:
            warnings.warn(f"Too many {armor_type.value} ! Only the first one added: "
                          f"{next(item for item in items if isinstance(item, Armor) and item.item == armor_type.value).name}", UserWarning)
            return False

    for accessory_type in accessory_types:
        accessories_of_type = [item for item in items if isinstance(item, Accessory) and item.item == accessory_type.value]
        if len(accessories_of_type) > 1:
            warnings.warn(f"Too many {accessory_type.value} ! Only the first one added:"
                          f"{next(item for item in items if isinstance(item, Accessory) and item.item == accessory_type.value).name}", UserWarning)
            return False

    rings = [item for item in items if isinstance(item, Accessory) and item.item == EItemType.RING.value]
    if len(rings) > 2:
        warnings.warn(f"Too many Rings ! Only the first two added: {rings[0].name} , {rings[1].name}", UserWarning)
        return False

    weapons = [item for item in items if isinstance(item, Weapon)]
    if len(weapons) > 1:
        warnings.warn(f"Too many Weapon ! Only the first one added: {next(item for item in items if isinstance(item, Weapon)).name}", UserWarning)
        return False

    return True

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
        rings = [item for item in items if isinstance(item, Accessory) and item.item == EItemType.RING.value]
        build = BuildEvaluator(
            helmet = next((item for item in items if isinstance(item, Armor) and item.item == EItemType.HELMET.value), None),
            chestplate = next((item for item in items if isinstance(item, Armor) and item.item == EItemType.CHESTPLATE.value), None),
            leggings = next((item for item in items if isinstance(item, Armor) and item.item == EItemType.LEGGINGS.value), None),
            boots = next((item for item in items if isinstance(item, Armor) and item.item == EItemType.BOOTS.value), None),
            ring1 = rings[0] if len(rings) > 0 else None,
            ring2 = rings[1] if len(rings) > 1 else None,
            bracelet = next((item for item in items if isinstance(item, Accessory) and item.item == EItemType.BRACELET.value), None),
            necklace = next((item for item in items if isinstance(item, Accessory) and item.item == EItemType.NECKLACE.value), None),
            weapon = next((item for item in items if isinstance(item, Weapon)), None),
        )

        validate_build(*items)

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
                warnings.warn(f"Unknown item type: {item.name}")
        return build

    def assign_armor(self, item):
        item_type = item.item

        if item_type == EItemType.HELMET.value:
            if not self.helmet:
                self.helmet = item
            else:
                warnings.warn(f"Too many: {EItemType.HELMET.value} ! Can't add item: {item.name}", UserWarning)

        elif item_type == EItemType.CHESTPLATE.value:
            if not self.chestplate:
                self.chestplate = item
            else:
                warnings.warn(f"Too many: {EItemType.CHESTPLATE.value} ! Can't add item: {item.name}", UserWarning)

        elif item_type == EItemType.LEGGINGS.value:
            if not self.leggings:
                self.leggings = item
            else:
                warnings.warn(f"Too many: {EItemType.LEGGINGS.value} ! Can't add item: {item.name}", UserWarning)

        elif item_type == EItemType.BOOTS.value:
            if not self.boots:
                self.boots = item
            else:
                warnings.warn(f"Too many: {EItemType.BOOTS.value} ! Can't add item: {item.name}", UserWarning)

        else:
            warnings.warn(f"Invalid item type: {item_type} , in item: {item.name}", UserWarning)

    def assign_accessory(self, item):
        item_type = item.item

        if item_type == EItemType.RING.value:
            if not self.ring1:
                self.ring1 = item
            elif not self.ring2:
                self.ring2 = item
            else:
                warnings.warn(f"Too many: {EItemType.RING.value} ! Can't add item: {item.name}", UserWarning)

        elif item_type == EItemType.BRACELET.value:
            if not self.bracelet:
                self.bracelet = item
            else:
                warnings.warn(f"Too many: {EItemType.BRACELET.value} ! Can't add item: {item.name}", UserWarning)

        elif item_type == EItemType.NECKLACE.value:
            if not self.necklace:
                self.necklace = item
            else:
                warnings.warn(f"Too many: {EItemType.NECKLACE.value} ! Can't add item: {item.name}", UserWarning)

        else:
            warnings.warn(f"Invalid item type: {item_type} , in item: {item.name}", UserWarning)

    def assign_weapon(self, item):
        if not self.weapon:
            self.weapon = item
        else:
            warnings.warn(f"Too many weapons ! Can't add item: {item.name}", UserWarning)

    def calculatebuild(self):
        min_lvl, max_lvl = 0, 0

        #todo make __add__ __iadd__ in damage class or maybe not
        #remake calculate for new fields style
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