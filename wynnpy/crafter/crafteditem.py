from typing import Optional, Dict, List
from wynnpy.data.recipes import Recipe
from wynnpy.data.enums import EID, EAttackSpeed, EItemRestrict, EItemType, EItemCategory, ECraftingSkill, EItemTier
from wynnpy.data.vrange import Range
from wynnpy.data.items import Damage, ItemIDs
from wynnpy.data.items import Weapon, Armor, Accessory
from .grid import Grid
from abc import ABC
import logging


class CraftedItem(ABC):
    grid: Grid
    recipe: Recipe
    materialTier: List[int]

#TODO hashing
class CraftedWeapon(Weapon, CraftedItem):
    pass

class CraftedArmor(Armor, CraftedItem):
    pass

class CraftedAccessory(Accessory, CraftedItem):
    pass

class CraftedItemFactory:
    
    @classmethod
    def craft(cls, recipe: Recipe, materialTier: List[int], grid: Grid) -> CraftedItem:
        
        craft_factories = {ECraftingSkill.TAILORING: cls.craft_armor,
                           ECraftingSkill.ARMOURING: cls.craft_armor,
                           ECraftingSkill.WOODWORKING: cls.craft_weapon,
                           ECraftingSkill.WEAPONSMITHING: cls.craft_weapon,
                           ECraftingSkill.JEWELING: cls.craft_accessory,}
        
        if recipe.skill == grid.skill:
            if recipe.skill in craft_factories.keys():
                grid.eval()
                return craft_factories[recipe.skill](recipe, materialTier, grid)
            else:
                logging.warning(f"There is no factory for a {recipe.skill.value} yet...")
        else:
            logging.warning(f"Item and ingredients crafting skill mismatch ({recipe.skill.value} vs {grid.skill.value})")

    #TODO atkSpd as Range
    #TODO id
    @classmethod
    def craft_weapon(cls, recipe: Recipe, materialTier: List[int], grid: Grid) -> CraftedWeapon:
        return CraftedWeapon(category=EItemCategory.WEAPON,
                             name = recipe.name,
                             item=recipe.item,
                             lvl=recipe.lvl,
                             itemIDs=grid.itemIDs,
                             ids=grid.ids,
                             tier=EItemTier.CRAFTED,
                             displayName=recipe.name,
                             restrict=[EItemRestrict.ALLOWCRAFTSMAN],
                             majorIDs=None,
                             damage=recipe.healthOrDamage,
                             atkSpd=EAttackSpeed.NORMAL,
                             powderSlots=cls.calculate_powderSlots(recipe),
                             id=-4) # Proper id will be asigned later...

    @classmethod
    def craft_armor(cls) -> CraftedArmor:
        pass
    
    @classmethod
    def craft_accessory(cls) -> CraftedAccessory:
        pass

    @classmethod
    def calculate_powderSlots(cls, recipe: Recipe) -> int:
        return 0
