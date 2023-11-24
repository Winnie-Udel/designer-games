from dataclasses import dataclass
from designer import *
from random import randint

set_window_color("lightblue")
FISH_SPEED = 5
SHARK_SPEED = 2
START_TIME = 45

@dataclass
class Button:
    background: DesignerObject
    border: DesignerObject
    label: DesignerObject

@dataclass
class TitleScreen:
    background: DesignerObject
    header: DesignerObject
    start_button: Button
    quit_button: Button

@dataclass
class World:
    fish: DesignerObject
    fish_speed: int
    shrimps: list[DesignerObject]
    sharks: list[DesignerObject]
    shark_speed: int
    score: int
    score_counter: list[DesignerObject]
    hearts: list[DesignerObject]
    frame: int
    second: int
    timer: list[DesignerObject]
    shark_number: int

def make_button(message: str, x: int, y: int) -> Button:
    """
    Creates a button.

    Args:
        message (str): Message on the button.
        x (int): The x position of the button.
        y (int): The y position of the button.

    Returns:
        Button: A collection of designer objects that forms a button.
    """
    horizontal_padding = 12
    vertical_padding = 8
    label = text("navy", message, 20, x, y, layer = 'top', font_name = 'DejaVu Sans Mono')
    return Button(rectangle("lightblue", label.width + horizontal_padding, label.height + vertical_padding, x, y),
                  rectangle("navy", label.width + horizontal_padding, label.height + vertical_padding, x, y, 1),
                  label)

def create_title_screen() -> TitleScreen:
    """
    Creates the title screen.

    Returns:
       TitleScreen: Composed of a background image, header, and two buttons.
    """
    return TitleScreen(background_image("images/title_background.png"),
                    text("navy", "Shark Invasion", 50, get_width()/2, 250, font_name = 'DejaVu Sans Mono'),
                    make_button("Play", get_width() / 2, 325),
                    make_button("Quit", get_width() / 2, 375))

def handle_title_buttons(world: TitleScreen):
    """
    When the buttons of the title screen are clicked, it redirects the user to either the start screen or permits the
    user to quit the game.

    Args:
	    world (TitleScreen): Composed of a background image, header, and two buttons.
    """
    if colliding_with_mouse(world.start_button.background):
        change_scene("start")
    if colliding_with_mouse(world.quit_button.background):
        quit()

def create_world() -> World:
    """
    Creates the world.

    Returns:
        World: The World's instance.
    """
    return World(create_fish(), FISH_SPEED, [], [], SHARK_SPEED, 0,
                 text("navy", "", 20, get_width()/2, 30, layer = 'top', font_name = 'DejaVu Sans Mono'),
                 aligned_hearts([create_heart(), create_heart(), create_heart()])
                 , 0, START_TIME,
                 text("navy", "", 20, get_width()/2, 80, layer = 'top', font_name = 'DejaVu Sans Mono'),
                 3)

def create_fish() -> DesignerObject:
    """
    Creates the fish.

    Returns:
        DesignerObject: Image of fish.
    """
    fish = image("images/fish.png")
    fish.scale_x = 0.4
    fish.scale_y = 0.4
    fish.y = get_height() * (1/3)
    fish.flip_x = True
    return fish

def move_fish(world: World):
    """
    The fish constantly moves without any user input.

    Args:
        world (World): The World's instance.
    """
    world.fish.x += world.fish_speed

def head_left(world: World):
    """
    The fish moves left.

    Args:
        world (World): The World's instance.
    """
    world.fish_speed = -FISH_SPEED
    world.fish.flip_x = False

def head_right(world: World):
    """
    The fish moves right.

    Args:
        world (World): The World's instance.
    """
    world.fish_speed = FISH_SPEED
    world.fish.flip_x = True

def wrap_fish(world: World):
    """
    When the fish collides with the end of the screen, fish warps to the opposite side of the screen.

    Args:
        world (World): The World's instance.
    """
    fish = world.fish
    if fish.x > get_width():
        fish.x = 0
    elif fish.x < 0:
        fish.x = get_width()
    elif fish.y > get_height():
        fish.y = 0
    elif fish.y < 0:
        fish.y = get_height()

def control_fish(world: World, key: str):
    """
    The fish moves left, right, up or down, depending on the key the user presses.

    Args:
        world (World): The World's instance.
        key (str): The key the user presses.
    """
    fish = world.fish
    if key == "left":
        head_left(world)
    elif key == "right":
        head_right(world)
    elif key == "up":
        fish.y += -30
    elif key == "down":
        fish.y += 30

def create_shrimp() -> DesignerObject:
    """
    Creates the shrimp.

    Returns:
        DesignerObject: A shrimp emoji.
    """
    shrimp = emoji("shrimp")
    shrimp.scale_x = 0.6
    shrimp.scale_y = 0.6
    shrimp.x = randint(0, get_width())
    shrimp.y = randint(0, get_height())
    return shrimp

def spawn_shrimp(world: World):
    """
    Shrimps are spawned randomly. A max of five shrimp can be spawned. 
    
    Args:
        world (World): The World's instance. 
    """
    not_too_many_shrimps = len(world.shrimps) < 5
    random_chance = randint(1, 75) == 25
    if not_too_many_shrimps and random_chance:
        world.shrimps.append(create_shrimp())

def eating_shrimp(world: World):
    """
    When fish and shrimp collide, the score increases by one and the fish grows bigger.

    Args:
         world (World): The World's instance.
    """
    eaten_shrimps = []
    fish = world.fish
    for shrimp in world.shrimps:
        if colliding(shrimp, fish):
            eaten_shrimps.append(shrimp)
            # Fish grows bigger
            fish.scale_x += 0.05
            fish.scale_y += 0.05
            # Scores increased by one
            world.score += 1
    world.shrimps = filter_from(world.shrimps, eaten_shrimps)

def update_score(world: World):
    """
    Update the score.

    Args:
        world (World): The World's instance.
    """
    world.score_counter.text = "Score: " + str(world.score)

def create_shark() -> DesignerObject:
    """
    Creates the shark.

    Returns:
        DesignerObject: A shark image.
    """
    shark = image("images/shark.png")
    shark.x = get_width()
    shark.y = randint(0, get_height())
    return shark

def spawn_shark(world: World):
    """
    Sharks randomly spawns.

    Args:
        world (World): The World's instance.
    """
    not_too_many_sharks = len(world.sharks) < world.shark_number
    random_chance = randint(1, 50) == 10
    if not_too_many_sharks and random_chance:
        world.sharks.append(create_shark())

def move_shark(world: World):
    """
    The shark moves from right to left. The shark is destroyed when moved offscreen.

    Args:
         world (World): The World's instance.
    """
    kept = []
    for shark in world.sharks:
        shark.x -= world.shark_speed
        if shark.x > 0:
            kept.append(shark)
        else:
            destroy(shark)
    world.sharks = kept

def eating_fish(world: World):
    """
    When fish collide with sharks, the player loses a heart.

    Args:
        world (World): The World's instance.
    """
    fish = world.fish
    collided_sharks = []
    lost_hearts = []
    for shark in world.sharks:
        if colliding(fish, shark):
            collided_sharks.append(shark)
            lost_hearts.append(world.hearts[-1])
    world.sharks = filter_from(world.sharks, collided_sharks)
    world.hearts = filter_from(world.hearts, lost_hearts)

def filter_from(old_objects: list[DesignerObject], destroyed_objects: list[DesignerObject]) -> list[DesignerObject]:
    """
    Removed destroyed objects.

    Args:
        old_objects (list[DesignerObject]): Original list of objects.
        destroyed_objects (list[DesignerObject]): Desired list of objects wanting to be removed.

    Returns:
        list[DesignerObject]: New list of objects after unwanted objects are removed.
    """
    objects = []
    for object in old_objects:
        if object in destroyed_objects:
            destroy(object)
        else:
            objects.append(object)
    return objects

def create_heart() -> DesignerObject:
    """
    Creates a heart.

    Returns:
        DesignerObject: A heart image.
    """
    heart = image("images/heart.png")
    heart.scale_x = 0.8
    heart.scale_y = 0.8
    heart.x = get_width()/2 - 20
    heart.y = 55
    return heart

def aligned_hearts(hearts: list[DesignerObject]):
    """
    Displayed the hearts side by side.

    Args:
        hearts (list[DesignerObject]): List of desired amount of hearts.
    """
    new_hearts = []
    offset = 0
    for index, heart in enumerate(hearts):
        heart.x += offset
        offset += 25
        new_hearts.append(heart)
    return new_hearts

def last_heart_warning(world: World):
    """
    Fish flashes when it has one heart left.

    Args:
        world (World): The World's instance.
    """
    if len(world.hearts) < 2:
        set_visible(world.fish, not world.fish.visible)

def update_timer(world: World):
    """
    Update the timer. When the game updates, for every 30 frames, a second passed by.

    Args:
        world (World): The World's instance.
    """
    world.frame += 1
    if world.frame % 30 == 0:
        world.second -= 1
    world.timer.text = "Timer: " + str(world.second)

def spawn_more_shark(world: World):
    """
    An extra shark is spawned every 20 seconds passed. The shark is also faster.

    Args:
        world (World): The World's instance.
    """
    if world.frame % 600 == 0:
        world.shark_number += 1
        world.shark_speed += 1

when("starting: title", create_title_screen)
when("clicking: title", handle_title_buttons)
when("starting: start", create_world)
when("updating: start", move_fish)
when("updating: start", wrap_fish)
when("typing: start", control_fish)
when("updating: start", spawn_shrimp)
when("updating: start", eating_shrimp)
when("updating: start", update_score)
when("updating: start", spawn_shark)
when("updating: start", move_shark)
when("updating: start", eating_fish)
when("updating: start", last_heart_warning)
when("updating: start", update_timer)
when("updating: start", spawn_more_shark)
start()