""" A command-line controlled coffee maker. """

import sys
import load_recipes

# Implement the coffee maker's commands. Interact with the user via stdin and print to stdout.
#
# Requirements:
#     - use functions
#     - use __main__ code block
#     - access and modify dicts and/or lists
#     - use at least once some string formatting (e.g. functions such as strip(), lower(),
#     format()) and types of printing (e.g. "%s %s" % tuple(["a", "b"]) prints "a b"
#     - BONUS: read the coffee recipes from a file, put the file-handling code in another module
#     and import it (see the recipes/ folder)
#
# There's a section in the lab with syntax and examples for each requirement.
#
# Feel free to define more commands, other coffee types, more resources if you'd like and have time.

# Tips:
# *  Start by showing a message to the user to enter a command, remove our initial messages
# *  Keep types of available coffees in a data structure such as a list or dict
# e.g. a dict with coffee name as a key and another dict with resource mappings (resource:percent)
# as value

# Commands
EXIT = "exit"
LIST_COFFEES = "list"
MAKE_COFFEE = "make"  # !!! when making coffee you must first check that you have enough resources!
HELP = "help"
REFILL = "refill"
RESOURCE_STATUS = "status"
COMMANDS = [EXIT, LIST_COFFEES, MAKE_COFFEE, REFILL, RESOURCE_STATUS, HELP]

# Coffee examples
ESPRESSO = "espresso"
AMERICANO = "americano"
CAPPUCCINO = "cappuccino"
COFFEES = (ESPRESSO, AMERICANO, CAPPUCCINO)

# Resources examples
WATER = "water"
COFFEE = "coffee"
MILK = "milk"

# Coffee maker's resources - the values represent the fill percents
RESOURCES = {WATER: 100, COFFEE: 100, MILK: 100}

# INGREDIENTS = {AMERICANO: {WATER: 10, COFFEE: 10, MILK: 0},
# CAPPUCCINO: {WATER: 5, COFFEE: 10, MILK: 10},
# ESPRESSO: {WATER: 5, COFFEE: 10, MILK: 0}}
INGREDIENTS = {}

# Example result/interactions:
#
# I'm a smart coffee maker
# Enter command:
# list
# americano, cappuccino, espresso
# Enter command:
# status
# water: 100%
# coffee: 100%
# milk: 100%
# Enter command:
# make
# Which coffee?
# espresso
# Here's your espresso!
# Enter command:
# refill
# Which resource? Type 'all' for refilling everything
# water
# water: 100%
# coffee: 90%
# milk: 100%
# Enter command:
# exit

# print("I'm a simple coffee maker")
# print("Press enter")
# sys.stdin.readline()
# print("Teach me how to make coffee...please...")


def list_coffees():
    """List all coffee types available"""
    for coffee in COFFEES:
        print(coffee, end=" ")
    print("")
    print("")


def make_coffee():
    """Make coffee"""
    print("Which coffee?")
    order = sys.stdin.readline().strip("\n")
    if order in COFFEES:
        for ingr in INGREDIENTS[order]:
            if RESOURCES[ingr] < INGREDIENTS[order][ingr]:
                print("Sorry, we need to refill; not enough " + ingr)
                return
        for ingr in INGREDIENTS[order]:
            RESOURCES[ingr] -= INGREDIENTS[order][ingr]
        print("Here is your " + order + "!")
    else:
        print("Not available")
    print("")


def help_coffee():
    """List available commands"""
    print("Commands:")
    print("exit")
    print("list")
    print("make")
    print("help")
    print("refill")
    print("status")
    print("")


def resource_status():
    """Show resources status"""
    for ingr in RESOURCES:
        print("%s: %d%%" % (ingr, RESOURCES[ingr]))
    print("")


def refill():
    """Refill resources"""
    print("Which resource? Type 'all' for refilling everything")
    details = sys.stdin.readline().strip("\n")
    if details == "all":
        RESOURCES[WATER] = 100
        RESOURCES[COFFEE] = 100
        RESOURCES[MILK] = 100
    elif details == "water":
        RESOURCES[WATER] = 100
    elif details == "coffee":
        RESOURCES[COFFEE] = 100
    elif details == "milk":
        RESOURCES[MILK] = 100
    else:
        print("No such thing")
    resource_status()


COMM_NAME = {EXIT: exit,
             LIST_COFFEES: list_coffees,
             MAKE_COFFEE: make_coffee,
             HELP: help_coffee,
             REFILL: refill,
             RESOURCE_STATUS: resource_status}


def main():
    """Simulate a coffee maker"""
    print("I'm a smart coffee maker\n")
    load_recipes.read_recipe(COFFEES, INGREDIENTS)
    while True:
        print("Enter command:")
        command = sys.stdin.readline().strip("\n")
        if command in COMMANDS:
            (COMM_NAME[command])()
        else:
            print("Try again")


if __name__ == "__main__":
    main()
