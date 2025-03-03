from typing import List, Union
from .ingreds import Ingredient
from .items import Item
from .recipes import Recipe
from abc import ABC, abstractmethod
import logging
from wynnpy.utils.fuzzy import fuzzy_match
from wynnpy.utils.filtering import Filter
from wynnpy.data.vrange import Range

class DataContainer(ABC):

    def __init__(self, arr: List): 
        self.objects = set()
        self.itemsType = type(arr[0])
        for object in arr:
            self.add(object)


    def add(self, object):
        try:
            hash(object)
            self.objects.add(object)
        except TypeError:
            logging.warning(f"The object of type {type(object)} is not hashable")
            

    def remove(self, object):
        self.objects.discard(object)

    # . . . ? Maybe we don't even need this abstract methods here
    @abstractmethod
    def byName(self, name: str):
        pass
    
    @abstractmethod
    def byID(self, id: int):
        pass
    
    @abstractmethod
    def search(self):
        pass

class ItemsContainer(DataContainer):
    def __init__(self, items: List[Item]):
        super().__init__(items)

    def byID(self, id: int) -> Item | None:
        return next((item for item in self.objects if item.id == id), None)

    def byName(self, name) -> Item | None:
        return next((item for item in self.objects if item.name == name), None)
    
    # filter(quantity, "expression0, expression1, expression2 . . .")
    # expression ~ "attr" / "!attr" / "attr0 ><= attr1" / TODO:"attr0 or attr1 or attr2 ..." / "attr0 xor attr1 ..." 
    def filter(self, filteringString: str) -> List[Item]:
        filterable_stats = [{'id':item.id, 
                             "total_hp_min": item.__dict__.get('hp', Range(0, 0)).min + item.ids.get("hpBonus", Range(0, 0)).min, 
                             "total_hp_avg": item.__dict__.get('hp', Range(0, 0)).mean() + item.ids.get("hpBonus", Range(0, 0)).mean(), 
                             "total_hp_max": item.__dict__.get('hp', Range(0, 0)).max + item.ids.get("hpBonus", Range(0, 0)).max}|
                            {i.value+"_min":item.ids.get(i, 0).min for i in item.ids.keys()}|
                            {i.value+"_avg":item.ids.get(i, 0).mean() for i in item.ids.keys()}|
                            {i.value+"_max":item.ids.get(i, 0).max for i in item.ids.keys()} for item in self.objects]
        #filterable_stats = [{'id':item.id, 'total_hp': item.__dict__.get("hp", 0) + item.ids.get("hp_bonus", 0), **item.ids} for item in self.objects]
        return [self.byID(item["id"]) for item in Filter(filteringString=filteringString, objects=filterable_stats).test()]

    #TODO implement threshold
    def search(self, name: str) -> Item:
        #Fuzzy search by name
        val = 127
        result = None
        for i in [item.name for item in self.objects]:
            curr_value = fuzzy_match(name.lower(), i.lower())
            if curr_value < val:
                val = curr_value
                result = i

        return self.byName(result)
        
    
class IngredientsContainer(DataContainer):
    def __init__(self, ingredients: List[Ingredient]):
        super().__init__(ingredients)

    def byID(self, id: int) -> Ingredient | None:
        return next((ingredient for ingredient in self.objects if ingredient.id == id), None)
    
    def byName(self, name) -> Ingredient | None:
        return next((ingredient for ingredient in self.objects if ingredient.name == name), None)
    
    def search(self, name: str) -> Ingredient:
        #Fuzzy search by name
        val = 127
        result = None
        for i in [item.name for item in self.objects]:
            curr_value = fuzzy_match(name.lower(), i.lower())
            if curr_value < val:
                val = curr_value
                result = i

        return self.byName(result)

class RecipeContainer(DataContainer):
    def __init__(self, recipes: List[Recipe]):
        super().__init__(recipes)

    def byID(self, id: int) -> Recipe | None:
        return next((recipe for recipe in self.objects if recipe.id == id), None)

    def byName(self, name) -> Recipe | None:
        return next((recipe for recipe in self.objects if recipe.name == name), None)

    def search(self, name: str) -> Recipe:
        #Fuzzy search by name
        val = 127
        result = None
        for i in [item.name for item in self.objects]:
            curr_value = fuzzy_match(name.lower(), i.lower())
            if curr_value < val:
                val = curr_value
                result = i

        return self.byName(result)

class MainDataContainer:
    def __init__(self, ingredients: IngredientsContainer, items: ItemsContainer, recipes: RecipeContainer):
        self.items = items
        self.ingredients = ingredients
        self.recipes = recipes

    