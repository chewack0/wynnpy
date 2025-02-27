from data.datacontainer import ItemsContainer, IngredientsContainer, RecipeContainer, MainDataContainer
from data import parse
import logger
import logging

log = logger.init_logger(loglevel=logging.INFO)

ingredients = list()
items = list()
recipes = list()

if __name__ == "__main__":

    data = MainDataContainer(ingredients = IngredientsContainer(parse.parse_ingredients('./data/ingreds.json')),
                            items = ItemsContainer(parse.parse_items('./data/items.json')),
                            recipes = RecipeContainer(parse.parse_recipes('./data/recipes.json')))
    