# A basic version of Minecraft in Python as a text adventure
version = "0.3.1"

# Import the random module
import random

# Define some constants
BLOCKS = ["air", "dirt", "stone", "wood", "leaves", "coal", "iron", "gold", "diamond"]
TOOLS = [
    "hand",
    "wooden pickaxe",
    "stone pickaxe",
    "iron pickaxe",
    "gold pickaxe",
    "diamond pickaxe",
]
DURABILITY = {
    "hand": -1,
    "wooden pickaxe": 60,
    "stone pickaxe": 132,
    "iron pickaxe": 251,
    "gold pickaxe": 33,
    "diamond pickaxe": 1562,
}
HARVEST_LEVEL = {
    "hand": 0,
    "wooden pickaxe": 1,
    "stone pickaxe": 2,
    "iron pickaxe": 3,
    "gold pickaxe": 1,
    "diamond pickaxe": 4,
}
BREAK_TIME = {
    "air": 0,
    "dirt": 0.75,
    "stone": 1.5,
    "wood": 2,
    "leaves": 0.3,
    "coal": 3,
    "iron": 4.5,
    "gold": 4.5,
    "diamond": 7.5,
}
HARDNESS = {
    "air": 0,
    "dirt": 0.5,
    "stone": 1.5,
    "wood": 2,
    "leaves": 0.2,
    "coal": 3,
    "iron": 5,
    "gold": 3,
    "diamond": 5,
}
REQUIREMENT = {
    "air": -1,
    "dirt": -1,
    "stone": -1,
    "wood": -1,
    "leaves": -1,
    "coal": -1,
    "iron": -1,
    "gold": -1,
    "diamond": -1,
}
CRAFTING = {
    "wooden pickaxe": {"wood": 3, "stick": 2},
    "stone pickaxe": {"stone": 3, "stick": 2},
    "iron pickaxe": {"iron ingot": 3, "stick": 2},
    "gold pickaxe": {"gold ingot": 3, "stick": 2},
    "diamond pickaxe": {"diamond": 3, "stick": 2},
}
SMELTING = {
    "iron ingot": {"iron ore": 1},
    "gold ingot": {"gold ore": 1},
}
FUEL = {
    "coal": 8,
}

# Define some global variables
inventory = {}
selected_tool = TOOLS[0]
world = []
world_size = (16, 16)
player_pos = (0, 0)
player_icon = "🙂"

# Define the commands and their effects
commands = {
    "north": lambda: move_player("w"),
    "south": lambda: move_player("s"),
    "east": lambda: move_player("d"),
    "west": lambda: move_player("a"),
    "dig": lambda: break_block(),
    "place": lambda: place_block(),
    "craft": lambda: craft_tool(),
    "map": lambda: print_world(),
    "icon": lambda: change_icon(),
    "save": lambda: save_world(),
    "load": lambda: load_world(),
    "help": lambda: show_help(),
}


def show_help():
    global commands
    # List the available commands and their descriptions
    print("You can use these commands:")
    for command in commands:
        print(f"- {command}")


# Define some helper functions
def generate_world():
    # Generate a random world with blocks
    global world
    global world_size
    world = []

    for x in range(world_size[0]):
        column = []
        for y in range(world_size[1]):
            block = random.choice(BLOCKS)
            column.append(block)
        world.append(column)


def print_world():
    # Print the world as a grid of symbols
    global world
    global world_size
    global player_pos
    symbols = {
        "air": "  ",
        "dirt": "🟫",
        "stone": "🪨",
        "wood": "🪵",
        "leaves": "🍃",
        "coal": "⚫",
        "iron": "⬜",
        "gold": "🪙",
        "diamond": "💎",
    }

    for y in range(world_size[1] - 1, -1, -1):
        row = ""
        for x in range(world_size[0]):
            if (x, y) == player_pos:
                row += player_icon
            else:
                block = world[x][y]
                symbol = symbols[block]
                row += symbol
        print(row)


def save_world():
    import os
    import pickle

    # Create a saves folder if it doesn't exist
    if not os.path.exists("saves"):
        os.makedirs("saves")

    global inventory
    global selected_tool
    global world
    global world_size
    global player_pos
    global player_icon

    # Save the data to a file
    world_data = [inventory, selected_tool, world, world_size, player_pos, player_icon]
    world_name = input("Please name your world: ").lower()
    world_save = open("saves/%s.txt" % (world_name), "wb")
    pickle.dump(world_data, world_save)
    world_save.close()
    print("Your world has been saved to /saves/%s.txt" % (world_name))


def load_world():
    from os.path import exists
    import pickle

    global inventory
    global selected_tool
    global world
    global world_size
    global player_pos
    global player_icon

    # Get name of world and check if it exists in the saves folder
    world_name = input(
        "Please enter the name of the world you'd like to load: "
    ).lower()
    if not exists("saves/%s.txt" % (world_name)):
        print(
            "That world doesn't seem to exist! Make sure it's in the saves directory."
        )
        return

    # Load the data from the file
    world_save = open("saves/%s.txt" % (world_name), "rb")
    world_data = pickle.load(world_save)
    inventory = world_data[0]
    selected_tool = world_data[1]
    world = world_data[2]
    world_size = world_data[3]
    player_pos = world_data[4]
    player_icon = world_data[5]
    world_save.close()
    print("%s loaded!" % (world_name))
    print_world()


def change_icon():
    global player_icon
    player_icon = input("What would you like your icon to be? ").lower()[0]


def move_player(direction):
    # Move the player in the given direction
    global player_pos
    global world_size
    x, y = player_pos

    if direction == "w":
        # Move up
        y += 1
    elif direction == "a":
        # Move left
        x -= 1
    elif direction == "s":
        # Move down
        y -= 1
    elif direction == "d":
        # Move right
        x += 1
    else:
        # Invalid direction
        print("Invalid direction")
        return

    # Check if the new position is valid
    if x < 0 or x >= world_size[0] or y < 0 or y >= world_size[1]:
        print("You cannot move out of the world")
        return

    # Update the player position
    player_pos = (x, y)
    print("You moved to", player_pos)


def break_block():
    # Break the block in front of the player
    global world
    global player_pos
    global inventory
    global selected_tool
    x, y = player_pos

    # Check if there is a block in front of the player
    if y == world_size[1] - 1:
        print("There is no block in front of you")
        return

    # Get the block type and its properties
    block = world[x][y + 1]
    hardness = HARDNESS[block]
    requirement = REQUIREMENT[block]
    break_time = BREAK_TIME[block]

    if block == "air":
        print("You cannot break air")
        return

    # Get the tool type and its properties
    tool = selected_tool
    durability = DURABILITY[tool]
    harvest_level = HARVEST_LEVEL[tool]

    # Check if the tool can break the block
    if harvest_level < requirement:
        print("You cannot break", block, "with", tool)
        return

    # Calculate the actual break time based on the tool and the block
    actual_break_time = break_time / (harvest_level + 1)

    # Print a message and wait for the break time
    print("Breaking", block, "with", tool, "...")
    import time

    time.sleep(actual_break_time)

    # Break the block and update the world and the inventory
    print("You broke", block)
    world[x][y + 1] = "air"
    inventory[block] = inventory.get(block, 0) + 1

    # Reduce the tool durability if it is not infinite
    if durability > 0:
        durability -= 1
        DURABILITY[tool] = durability
        print(tool, "durability:", durability)

        # If the tool breaks, switch to hand
        if durability == 0:
            print(tool, "broke")
            selected_tool = TOOLS[0]


def place_block():
    # Place a block in front of the player
    global world
    global player_pos
    global inventory
    x, y = player_pos

    # Check if there is an empty space in front of the player
    if y == world_size[1] - 1 or world[x][y + 1] != "air":
        print("You cannot place a block here")
        return

    # Ask the player what block they want to place
    print("What block do you want to place?")
    print("Your inventory:", inventory)
    block = input("> ")

    # Check if the player has that block in their inventory
    if not block in inventory or inventory[block] == 0:
        print("You don't have any", block)
        return

    # Place the block and update the world and the inventory
    print("You placed", block)
    world[x][y + 1] = block
    inventory[block] -= 1


def craft_tool():
    # Craft a tool from the available materials
    global inventory
    global selected_tool

    # Ask the player what tool they want to craft
    print("What tool do you want to craft?")
    print("Your inventory:", inventory)
    tool = input("> ")

    # Check if the tool is valid
    if not tool in TOOLS:
        print("Invalid tool")
        return

    # Check if the player has enough materials to craft the tool
    recipe = CRAFTING.get(tool, {})
    for material, amount in recipe.items():
        if not material in inventory or inventory[material] < amount:
            print("You don't have enough", material)
            return

    # Craft the tool and update the inventory
    print("You crafted", tool)
    for material, amount in recipe.items():
        inventory[material] -= amount

    # Select the new tool
    selected_tool = tool


# def smelt_item():
#      # Smelt an item from a raw material
#      global inventory

#      # Ask the player what item they want to smelt
#      print("What item do you want to smelt?")
#      print("Your inventory:", inventory)
#      item = input("> ")

#      # Check if the item is valid
#      if not item in SMELTING:
#          print("Invalid item")
#          return

#      # Check if the player has enough raw materials to smelt the item
#      recipe = SMELTING[item]
#      for material, amount in recipe.items():
#          if not material in inventory or inventory[material] < amount:
#              print("You don't have enough", material)
#              return

#       # Check if the player has enough fuel to smelt the item
#       fuel_needed = 1
#       fuel_available = 0
#       for fuel, value in FUEL.items():

# Start the game
print("Welcome to the text-based minecraft game!")
generate_world()
print_world()
show_help()

# Main game loop
playing = True
while playing:
    # Get the user input
    command = input("What do you want to do? ").lower()

    # Check if the command is valid
    if command in commands:
        commands[command]()
    else:
        # The command is invalid
        print("Invalid command.")
