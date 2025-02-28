import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from wynnpy.data.datacontainer import ItemsContainer, IngredientsContainer, RecipeContainer, MainDataContainer
from wynnpy.data import parse
from wynnpy.crafter import grid
from wynnpy import logger
import logging




log = logger.init_logger(loglevel=logging.INFO)

if __name__ == "__main__":

    data = MainDataContainer(ingredients = IngredientsContainer(parse.parse_ingredients('./data/json/ingreds.json')),
                            items = ItemsContainer(parse.parse_items('./data/json/items.json')),
                            recipes = RecipeContainer(parse.parse_recipes('./data/json/recipes.json')))
    
    
    