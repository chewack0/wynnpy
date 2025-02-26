from ingreds import Ingredient
from items import Item
from recipes import Recipe
import parse

ingredients = list()
items = list()
recipes = list()

def init():
    global recipes
    global items
    global ingredients
    
    ingredients = parse.parse_ingredients('./data/ingreds.json')
    items = parse.parse_items('./data/items.json')
    recipes = parse.parse_recipes('./data/recipes.json')

if __name__ == "__main__":
    init()