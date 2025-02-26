import json
from typing import List

from items import Item
from ingreds import Ingredient
from recipes import Recipe

def parse_items(path: str) -> List[Item]:
    items = list()
    with open(path) as data:
        data = json.load(data)["items"]
        for item in data:
            items.append(Item.parse_item(item))
    return items

def parse_ingredients(path: str) -> List[Ingredient]:
    ingredients = list()
    with open(path) as data:
        data = json.load(data)
        counter = 1
        for ing in data:
            print(f"[{counter}]Parsing... {ing["name"]}")
            ingredients.append(Ingredient.parse_ing(ing))
            counter += 1
    return ingredients

def parse_recipes(path: str) -> List[Recipe]:
    recipes = list()
    with open(path) as data:
        data = json.load(data)
        counter = 1
        for recipe in data["recipes"]:
            print(f"[{counter}]Parsing... {recipe["name"]}")
            recipes.append(Recipe.parse_recipe(recipe))
            counter += 1
        return recipes
