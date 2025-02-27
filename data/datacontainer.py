from typing import List, Union
from data.ingreds import Ingredient
from data.items import Item
from data.recipes import Recipe
from abc import ABC, abstractmethod
import logging
from utils.fuzzy import fuzzy_match

class DataContainer(ABC):

    def __init__(self, arr: List): 
        self.objects = set()
        self.itemsType = type(arr[0])
        for object in arr:
            self.add(object)


    def add(self, object):
        if type(object) != self.itemsType:
            logging.warning(f"The object ({type(object)}) is not of type {self.itemsType}")
        else:
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

    