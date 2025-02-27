import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from data.datacontainer import ItemsContainer, IngredientsContainer, RecipeContainer, MainDataContainer
from data import parse
from crafter import grid
import logger
import logging




log = logger.init_logger(loglevel=logging.INFO)

ingredients = list()
items = list()
recipes = list()

if __name__ == "__main__":

    data = MainDataContainer(ingredients = IngredientsContainer(parse.parse_ingredients('./data/json/ingreds.json')),
                            items = ItemsContainer(parse.parse_items('./data/json/items.json')),
                            recipes = RecipeContainer(parse.parse_recipes('./data/json/recipes.json')))
    
    