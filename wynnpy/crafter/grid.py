from wynnpy.data.ingreds import Ingredient, EID, Range, ItemIDs, PosMods, ECraftingSkill
from typing import Optional, List, Dict
import logging 



class Grid:
    
    skill: ECraftingSkill
    ids: Dict[EID, Range]
    itemIDs: ItemIDs

    def __init__(self, skill: ECraftingSkill, *ingreds: Optional[Ingredient]):
        
        self.skill = skill
        for ing in ingreds:
            if not ing.validate_skill(self.skill):
                logging.warning(f"Hey, something is wrong with crafting skill, you can't use {ing.name}({', '.join(str(skill.value) for skill in ing.skills)}) in this recipe ({self.skill.value})")

        if len(ingreds) == 6:
            self.ingredients = [[ingreds[0], ingreds[1]],
                                [ingreds[2], ingreds[3]],
                                [ingreds[4], ingreds[5]]]
        elif len(ingreds) == 15:
            self.ingredients = [[ingreds[i] for i in range(3)] for j in range(5)]
        else:
            raise ValueError("There is something wrong with ingreds quantity")
            
        self.posModsGrid = [[100 for i in range(len(self.ingredients[0]))] for j in range(len(self.ingredients))]
        self.ids = dict()

    def eval(self):
        return self.evalPosMods().evalIDs()
    
    def evalIDs(self):
        for i in range(len(self.ingredients)):
            for j in range(len(self.ingredients[i])):
                for id in self.ingredients[i][j].ids.items():
                    if id[0] in self.ids:
                        self.ids[id[0]] += (id[1] * (self.posModsGrid[i][j] / 100)).floor()
                    else:
                        self.ids[id[0]] = (id[1] * (self.posModsGrid[i][j] / 100)).floor()
        return self

    def evalPosMods(self):
        for i in range(len(self.ingredients)):
            for j in range(len(self.ingredients[0])):
                if self.ingredients[i][j] is not None:
                    self.posModsGrid = self.calculatePosMods(self.ingredients[i][j].posMods, [i, j], self.posModsGrid)
                else:
                    pass
        return self

    @staticmethod
    def calculatePosMods(posmods: PosMods, position: List[int], board: List[List]) -> List:
        y0, x0 = position
        values = board
        for y1 in range(len(board)):
            for x1 in range(len(board[0])):
                if x0 > x1 and y0 == y1:
                    values[y1][x1] += posmods.left
                if x0 < x1 and y0 == y1:
                    values[y1][x1] += posmods.right
                if x0 == x1 and y0 < y1:
                    values[y1][x1] += posmods.under
                if x0 == x1 and y0 > y1:
                    values[y1][x1] += posmods.above
                if (abs(x0 - x1) + abs(y0 - y1)) < 2 and (abs(x0 - x1) + abs(y0 - y1)) != 0:
                    values[y1][x1] += posmods.touching
                if (abs(x0 - x1) + abs(y0 - y1)) > 1 and (abs(x0 - x1) + abs(y0 - y1)) != 0: 
                    values[y1][x1] += posmods.notTouching 
                if y1 == y0 and x1 == position[1]:
                    pass
        return values
    
    def prettyIDs(self):
        for i in self.ids:
            print(f"{i.value.min} {i.stat} {i.value.max}")

    def pretty(self):
        for i in self.ingredients:
            print(*[j.name if j is not None else "-" for j in i])

    def prettyPosMods(self):
        for i in self.posModsGrid:
            print(*i)

#example = Grid(ingredient0, ingredient1,
#               ingredient2, ingredient3,
#               ingredient4, ingredient5)

if __name__ == "__main__":
    print("cool")