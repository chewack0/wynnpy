from typing import List
import logging

class Filter:
    '''
        A class to parse logical?? expressions and compare it against some list of dictionaries\n
        Supported operators > < = !attr attr
    '''

    tokens: List['Expression']

    def __init__(self, filteringString: str, objects: List):
        if isinstance(objects, dict):
            self.objects = [objects]
        elif isinstance(objects, list):
            for i in objects:
                if not isinstance(i, dict):
                    raise TypeError("Bruv get me some dictionaries")
            self.objects = objects
        else:
            raise TypeError("Me want list of dicts, or at least just a dict")

        self.filteringString = filteringString
        self.expressions = []
        for expression in self.parseFilteringString():
            self.expressions += self.parseExpression(expression)
        #self.expressions = [self.parseExpression(expression) for expression in self.parseFilteringString()]
    
    def __repr__(self):
        return self.filteringString

    def parseFilteringString(self):
        tokens = []
        for i in [i.strip() for i in self.filteringString.split(",")]:
            tokens.append(i)
        return tokens
    
    def parseExpression(self, token: str) -> List['Expression']:
        #TODO OR XOR

        parts = [token.strip()]
        
        expressions = []
        for part in parts:
             
            if part.startswith("!"):
                attr = part[1::]
                expressions.append(self.Expression(attr=attr, operator="!"))
            elif '>' in part:
                attr, value = part.split(">", 1)
                expressions.append(self.Expression(attr=attr, operator=">", value=value))
            elif '<' in part:
                attr, value = part.split("<", 1)
                expressions.append(self.Expression(attr=attr, operator="<", value=value))
            elif '=' in part:
                attr, value = part.split("=", 1)
                expressions.append(self.Expression(attr=attr, operator="=", value=value))
            else:
                expressions.append(self.Expression(part.strip()))
        return expressions

    def test(self):
        result = []
        for object in self.objects:
            #if not any(expression.test(object) for expression in self.expressions):
            flag = True
            for expression in self.expressions:
                if not expression.test(object):
                    flag = False
            if flag:
                result.append(object)
    
        return result
    
    class Expression:

        def __init__(self, attr: str, operator: str = None, value: str = None):
            self.attr = attr.strip()
            self.operator = operator.strip()
            self.value = str(value).strip()

        def __repr__(self):
            return f"{self.attr} {self.operator} {self.value}"
        
        def test(self, object) -> bool:
            if self.operator is None:
                return bool(object.get(self.attr, 0))     
            if self.operator == "!":
                return not bool(object.get(self.attr, 0))
            if self.operator == "=":
                return bool(str(object.get(self.attr, 0)) == str(self.value))
            if self.operator == "<":
                try:
                    return object.get(self.attr, 0) < int(self.value)
                except (ValueError, TypeError):
                    return False
            if self.operator == ">":
                try:
                    return object.get(self.attr, 0) > int(self.value)
                except (ValueError, TypeError):
                    return False
        # =)

if __name__ == "__main__":
    a = [{"name": 0, "c": 10, "b": 5, "d": 0},{"name": 1, "c": 5, "b": 5, "d": 0},{"name": 2, "c": 10, "b": 10, "d": 0}]
    s = "c > 6, b < 10, d = 0"
    c = Filter(s, a).test()
