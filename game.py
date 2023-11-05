from dataclasses import dataclass
from designer import *

FISH_SPEED = 5

@dataclass
class World:
    fish: DesignerObject
    fish_speed: int

def create_world() -> World:
    """Create the world"""
    return World(create_fish(), FISH_SPEED)

def create_fish() -> DesignerObject:
    """Create the fish"""
    fish = emoji("fish")
    fish.y = get_height() * (1/3)
    fish.flip_x = True
    return fish

def move_fish(world:World):
    world.fish.x += world.fish_speed

def head_left(world: World):
    world.fish_speed = -FISH_SPEED
    world.fish.flip_x = False

def head_right(world: World):
    world.fish_speed = FISH_SPEED
    world.fish.flip_x = True

def head_up(world: World):
    world.fish.y += -30

def head_down(world:World):
    world.fish.y += 30

def wrap_fish(world: World):
    if world.fish.x > get_width():
        world.fish.x = 0
    elif world.fish.x < 0:
        world.fish.x = get_width()
    elif world.fish.y > get_height():
        world.fish.y = 0
    elif world.fish.y < 0:
        world.fish.y = get_height()

def control_fish(world: World, key: str):
    if key == "left":
        head_left(world)
    elif key == "right":
        head_right(world)
    elif key == "up":
        head_up(world)
    elif key == "down":
        head_down(world)

when("starting", create_world)
when("updating", move_fish)
when("updating", wrap_fish)
when("typing", control_fish)
start()

