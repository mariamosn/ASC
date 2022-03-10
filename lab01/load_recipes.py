"""Bonus task"""

# Bonus task: load all the available coffee recipes from the folder 'recipes/'
# File format:
# 	first line: coffee name
# 	next lines: resource=percentage
#
# info and examples for handling files:
# 	http://cs.curs.pub.ro/wiki/asc/asc:lab1:index#operatii_cu_fisiere
# 	https://docs.python.org/3/library/io.html
# 	https://docs.python.org/3/library/os.path.html

RECIPES_FOLDER = "recipes"


def read_recipe(coffees, ingredients):
    """Parse the recipe for each type of coffee"""
    for coffee in coffees:
        crt_recipe = {}
        file_name = "./recipes/" + coffee + '.txt'
        file = open(file_name, 'r')
        for line in file:
            if line.strip("\n") != coffee:
                crt_recipe[line.split("=")[0]] = int(line.split("=")[1].strip("\n"))
        ingredients[coffee] = crt_recipe
    return ingredients
