import json
from typing import List
import logging 
from items import Item
from ingreds import Ingredient
from recipes import Recipe

def parse_items(path: str) -> List[Item]:
    items = list()
    with open(path) as data:
        data = json.load(data)["items"]
        counter = 1
        for item in data:
            logging.info(f"[{counter}] Parsing item... {item["name"]}  id: {item["id"]}")
            items.append(Item.parse_item(item))
            counter += 1
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
