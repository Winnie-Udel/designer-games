from dataclasses import dataclass
from designer import *
from random import randint

set_window_color("lightblue")
FISH_SPEED = 5

@dataclass
class World:
    fish: DesignerObject
    fish_speed: int
    shrimps: list[DesignerObject]

def create_world() -> World:
    """Create the world."""
    return World(create_fish(), FISH_SPEED, [])

def create_fish() -> DesignerObject:
    """Create the fish."""
    fish = emoji("fish")
    fish.y = get_height() * (1/3)
    fish.flip_x = True
    return fish

def move_fish(world:World):
    """The fish constantly moves."""
    world.fish.x += world.fish_speed

def head_left(world: World):
    """The fish moves left."""
    world.fish_speed = -FISH_SPEED
    world.fish.flip_x = False

def head_right(world: World):
    """The fish moves right."""
    world.fish_speed = FISH_SPEED
    world.fish.flip_x = True

def head_up(world: World):
    """The fish moves up."""
    world.fish.y += -30

def head_down(world: World):
    """The fish moves down."""
    world.fish.y += 30

def wrap_fish(world: World):
    """
    When the fish collides with the end of the screen,
    fish warps to the opposite side of the screen.
    """
    if world.fish.x > get_width():
        world.fish.x = 0
    elif world.fish.x < 0:
        world.fish.x = get_width()
    elif world.fish.y > get_height():
        world.fish.y = 0
    elif world.fish.y < 0:
        world.fish.y = get_height()

def control_fish(world: World, key: str):
    """
    The fish moves left, right, up or down,
    depending on the key the user presses.
    """
    if key == "left":
        head_left(world)
    elif key == "right":
        head_right(world)
    elif key == "up":
        head_up(world)
    elif key == "down":
        head_down(world)

def create_shrimp() -> DesignerObject:
    """Creates the shrimp, food for the fish."""
    shrimp = emoji("shrimp")
    shrimp.scale_x = 0.5
    shrimp.scale_y = 0.5
    shrimp.x = randint(0, get_width())
    shrimp.y = randint(0, get_height())
    return shrimp

def make_shrimp(world: World):
    """
    The shrimps spawns randomly.
    A max of five shrimp can be spawned.
    """
    not_too_many_shrimps = len(world.shrimps) < 5
    random_chance = randint(1, 50) == 25
    if not_too_many_shrimps and random_chance:
        world.shrimps.append(create_shrimp())

def eating_shrimp(world: World):
    eaten_shrimps = []
    for shrimp in world.shrimps:
        if colliding(shrimp, world.fish):
            eaten_shrimps.append(shrimp)
    world.shrimps = remove_shrimp(world.shrimps, eaten_shrimps)

def remove_shrimp(shrimps: list[DesignerObject], eaten_shrimps: list[DesignerObject]) -> list[DesignerObject]:
    #Remove eaten shrimps
    uneaten_shrimps = []
    for shrimp in shrimps:
        if shrimp in eaten_shrimps:
            destroy(shrimp)
        else:
            uneaten_shrimps.append(shrimp)
    return uneaten_shrimps

when("starting", create_world)
when("updating", move_fish)
when("updating", wrap_fish)
when("typing", control_fish)
when("updating", make_shrimp)
when("updating", eating_shrimp)
start()

