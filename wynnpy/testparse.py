import json

with open("./data/json/recipes.json") as file:
    data = json.load(file)["recipes"]
    print(data[0])
