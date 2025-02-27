from typing import List, Union
from ingreds import Ingredient
from items import Item
from recipes import Recipe
from abc import ABC, abstractmethod
import logging

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

    def byID(self, id: int) -> Item:
        return [item for item in self.objects if item.id == id]

    def byName(self, name):
        pass
    
    def search(self):
        pass
    
class IngredientsContainer(DataContainer):
    def __init__(self, ingredients: List[Ingredient]):
        super().__init__(ingredients)

    def byID(self, id: int) -> Ingredient:
        return [ingredient for ingredient in self.objects if ingredient.id == id]

    def byName(self, name):
        pass
    
    def search(self):
        pass

class RecipeContainer(DataContainer):
    def __init__(self, recipes: List[Recipe]):
        super().__init__(recipes)

    def byID(self, id: int) -> Recipe:
        return [recipe for recipe in self.objects if recipe.id == id]

    def byName(self, name):
        pass

    def search(self):
        pass

class MainDataContainer:
    def __init__(self, ingredients: IngredientsContainer, items: ItemsContainer, recipes: RecipeContainer):
        self.items = items
        self.ingredients = ingredients
        self.recipes = recipes

    