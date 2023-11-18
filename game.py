from dataclasses import dataclass
from designer import *
from random import randint

set_window_color("lightblue")
FISH_SPEED = 5
SHARK_SPEED = 2

@dataclass
class World:
    fish: DesignerObject
    fish_speed: int
    shrimps: list[DesignerObject]
    sharks: list[DesignerObject]
    shark_speed: int
    score: int
    counter: list[DesignerObject]
    lives: list[DesignerObject]


def create_world() -> World:
    """Create the world."""
    return World(create_fish(), FISH_SPEED, [], [], SHARK_SPEED, 0,
                 text("black", "", 25, get_width()/2, 30, font_name = 'Roboto'),
                 display_heart([create_heart(), create_heart(), create_heart()]))

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
    fish = world.fish
    for shrimp in world.shrimps:
        if colliding(shrimp, world.fish):
            eaten_shrimps.append(shrimp)
            # Fish grows bigger
            fish.scale_x += 0.05
            fish.scale_y += 0.05
            # Scores
            world.score += 1
    world.shrimps = filter_from(world.shrimps, eaten_shrimps)

def update_score(world: World):
    """ Update the score """
    world.counter.text = "Score: " + str(world.score)

def create_shark() -> DesignerObject:
    shark = emoji("shark")
    shark.scale_x = 2
    shark.scale_y = 2
    shark.x = get_width()
    shark.y = randint(0, get_height())
    return shark

def make_sharks(world: World):
    too_many_sharks = len(world.sharks) < 4
    rand_chance = randint(1, 50) == 10
    if too_many_sharks and rand_chance:
        world.sharks.append(create_shark())

def move_shark(world:World):
    """The shark constantly moves. Shark is destroyed when moves offscreen"""
    kept = []
    for shark in world.sharks:
        shark.x -= world.shark_speed
        if shark.x > 0:
            kept.append(shark)
        else:
            destroy(shark)
    world.sharks = kept

def eating_fish(world: World):
    fish = world.fish
    collided_sharks = []
    remove_hearts = []
    for shark in world.sharks:
        if colliding(fish, shark):
            collided_sharks.append(shark)
            remove_hearts.append(world.lives[-1])
    world.sharks = filter_from(world.sharks, collided_sharks)
    world.lives = filter_from(world.lives, remove_hearts)

def filter_from(old_objects: list[DesignerObject], destroyed_objects: list[DesignerObject]) -> list[DesignerObject]:
    # Removed destroyed objects
    objects = []
    for object in old_objects:
        if object in destroyed_objects:
            destroy(object)
        else:
            objects.append(object)
    return objects

def create_heart() -> DesignerObject:
    heart = emoji("❤")
    heart.scale_x = 0.5
    heart.scale_y = 0.5
    heart.x = get_width()/2 - 20
    heart.y = 55
    return heart

def display_heart(lives: list[DesignerObject]):
    hearts = []
    offset = 0
    for index, heart in enumerate(lives):
        heart.x += offset
        offset += 20
        hearts.append(heart)
    return hearts

def fish_hurt(world: World):
    "Fish flashes when it has one life left"
    if len(world.lives) < 2:
        set_visible(world.fish, not world.fish.visible)
        print(world.fish.visible)

when("starting", create_world)
when("updating", move_fish)
when("updating", wrap_fish)
when("typing", control_fish)
when("updating", make_shrimp)
when("updating", eating_shrimp)
when("updating", update_score)
when("updating", make_sharks)
when("updating", move_shark)
when("updating", eating_fish)
when("updating", fish_hurt)
start()

