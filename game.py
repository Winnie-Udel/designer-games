from dataclasses import dataclass
from designer import *
from random import randint

set_window_color("lightblue")
FISH_SPEED = 5
SHARK_SPEED = 2
START_TIME = 45
SHARK_NUMBER = 3

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
class GameOverScreen:
    background: DesignerObject
    header: DesignerObject
    final_score: DesignerObject
    remaining_hearts: DesignerObject
    bonus_point: DesignerObject
    home_button: Button

@dataclass
class World:
    fish: DesignerObject
    fish_speed: int
    shrimps: list[DesignerObject]
    sharks: list[DesignerObject]
    shark_speed: int
    score: int
    score_counter: DesignerObject
    hearts: list[DesignerObject]
    frame: int
    second: int
    timer: DesignerObject
    shark_number: int
    power_ups: list[DesignerObject]
    marine_snows: list[DesignerObject]

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
    When the buttons of the title screen are clicked, it redirects the user to either the game scene or permits the
    user to quit the game.

    Args:
	    world (TitleScreen): Composed of a background image, header, and two buttons.
    """
    if colliding_with_mouse(world.start_button.background):
        change_scene("game")
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
                 SHARK_NUMBER, [], [])

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

def aligned_hearts(hearts: list[DesignerObject]) -> list[DesignerObject]:
    """
    Displayed the hearts side by side.

    Args:
        hearts (list[DesignerObject]): List of desired amount of hearts.

    Returns:
        list[DesignerObject]: List of hearts that's displayed side by side.
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
    if world.frame % 600 == 0: # 30 frames * 20 = 600
        world.shark_number += 1
        world.shark_speed += 1

def create_power_up() -> DesignerObject:
    """
    Creates a timer power-up.

    Returns:
        DesignerObject: An image of a timer power-up.
    """
    power_up = image("images/timer.png")
    power_up.scale_x = 0.3
    power_up.scale_y = 0.3
    power_up.x = randint(0, get_width())
    power_up.y = 0
    return power_up

def spawn_power_up(world: World):
    """
    Power-ups randomly spawns.

    Args:
        world (World): The World's instance.
    """
    not_too_many_power_ups = len(world.power_ups) < 2
    random_chance = randint(1, 150) == 100
    if not_too_many_power_ups and random_chance:
        world.power_ups.append(create_power_up())

def move_power_up(world: World):
    """
    The power ups descends from above. The power ups is destroyed when moved offscreen.

    Args:
        world (World): The World's instance.
    """
    kept = []
    for power_up in world.power_ups:
        power_up.y += 1
        if power_up.y < get_height():
            kept.append(power_up)
        else:
            destroy(power_up)
    world.power_ups = kept

def more_time(world: World):
    """
    When fish collide with time power-ups, 15 seconds is added to the timer.

    Args:
        world (World): The World's instance.
    """
    fish = world.fish
    collided_power_ups = []
    for power_up in world.power_ups:
        if colliding(fish, power_up):
            collided_power_ups.append(power_up)
            world.second += 15
    world.power_ups = filter_from(world.power_ups, collided_power_ups)

def create_marine_snow() -> DesignerObject:
    """
    Create marine snow.

    Returns:
         DesignerObject: Image of a marine snow.
    """
    marine_snow = image("images/snow.png")
    marine_snow.scale_x = 0.2
    marine_snow.scale_y = 0.2
    marine_snow.x = randint(0, get_width())
    marine_snow.y = 0
    return marine_snow

def spawn_marine_snow(world: World):
    """
    Marine snow randomly spawns.

    Args:
        world (World): The World's instance.
    """
    not_too_many_marine_snow = len(world.marine_snows) < 4
    random_chance = randint(1, 100) == 50
    if not_too_many_marine_snow and random_chance:
        world.marine_snows.append(create_marine_snow())

def move_marine_snow(world: World):
    """
    The marine snow descends from above. The snow is destroyed when moved offscreen.

    Args:
        world (World): The World's instance.
    """
    kept = []
    for marine_snow in world.marine_snows:
        marine_snow.y += 2
        if marine_snow.y < get_height():
            kept.append(marine_snow)
        else:
            destroy(marine_snow)
    world.marine_snows = kept

def shrink_fish(world: World):
    """
    When fish collide with marine_snow, the fish shrinks.

    Args:
        world (World): The World's instance.
    """
    fish = world.fish
    collided_marine_snows = []
    for marine_snow in world.marine_snows:
        if colliding(fish, marine_snow):
            collided_marine_snows.append(marine_snow)
            fish.scale_x -= 0.05
            fish.scale_y -= 0.05
    world.marine_snows = filter_from(world.marine_snows, collided_marine_snows)

def game_over(world: World):
    """
    Transition to the end scene, or the game over screen, when either the time runs out or when there is no more
    hearts left.

    Args:
        world (World): The World's instance.
    """
    time_runs_out = world.second == 0
    no_more_hearts = len(world.hearts) == 0
    if time_runs_out or no_more_hearts:
        push_scene("end", score=world.score, remaining_hearts=len(world.hearts))

def create_game_over_screen(score: int, remaining_hearts: int) -> GameOverScreen:
    """
    Creates the game over screen.

    Args:
        score (int): Player's score.
        remaining_hearts (int): Number of player's remaining hearts.

    Returns:
        GameOverScreen: Composed of a background image, header, game statistics, and a home button.
    """
    bonus_points = remaining_hearts * 15
    final_score = score + bonus_points
    return GameOverScreen(image("images/game_over_background.png"),
                          text("navy", "Game Over!", 60, get_width()/2, 180, font_name = 'DejaVu Sans Mono'),
                          text("navy", "Final Score: " + str(final_score), 35, get_width()/2, 245,
                               font_name = 'DejaVu Sans Mono'),
                          text("navy", "Remaining Hearts: " + str(remaining_hearts), 20, get_width() / 2, 280,
                               font_name='DejaVu Sans Mono'),
                          text("navy", "Bonus Points: +" + str(bonus_points), 20, get_width() / 2, 305,
                               font_name='DejaVu Sans Mono'),
                          make_button("Home", get_width()/2, 380))

def handle_game_over_button(world: GameOverScreen):
    """
    When the home button of the end scene is clicked, it redirects the user to the title scene.

    Args:
    	world (GameOverScreen): Composed of a background image, header, game statistics, and a home button.
    """
    if colliding_with_mouse(world.home_button.background):
        change_scene("title")

when("starting: title", create_title_screen)
when("clicking: title", handle_title_buttons)
when("starting: game", create_world)
when("updating: game", move_fish)
when("updating: game", wrap_fish)
when("typing: game", control_fish)
when("updating: game", spawn_shrimp)
when("updating: game", eating_shrimp)
when("updating: game", update_score)
when("updating: game", spawn_shark)
when("updating: game", move_shark)
when("updating: game", eating_fish)
when("updating: game", last_heart_warning)
when("updating: game", update_timer)
when("updating: game", spawn_more_shark)
when("updating: game", spawn_power_up)
when("updating: game", move_power_up)
when("updating: game", more_time)
when("updating: game", spawn_marine_snow)
when("updating: game", move_marine_snow)
when("updating: game", shrink_fish)
when("updating: game", game_over)
when("starting: end", create_game_over_screen)
when("clicking: end", handle_game_over_button)
start()