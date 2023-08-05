from enum import Enum, auto

import tcod
from tcod import Color

from .fov import distance
from .game_messages import join_list
from .game_states import GameStates
from .menu import inventory_menu


class RenderOrder(Enum):
    PLAYER = auto()
    ENEMY = auto()
    ITEM = auto()
    CORPSE = auto()


def render_bar(
    panel, x, y, total_width, name, value, maximum, bar_color, back_color
):
    bar_width = int(float(value) / maximum * total_width)

    tcod.console_set_default_background(panel, back_color)
    tcod.console_rect(panel, x, y, total_width, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        tcod.console_rect(panel, x, y, bar_width, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_foreground(panel, tcod.white)
    tcod.console_print_ex(
        panel,
        int(x + total_width / 2),
        y,
        tcod.BKGND_NONE,
        tcod.CENTER,
        f"{name}: {value}/{maximum}",
    )


def render_all(
    console,
    panel,
    bar_width,
    message_log,
    game_map,
    player,
    fov_map,
    memory,
    color_scheme,
    game_state,
    mouse,
    menu_selection=0,
    key_cursor=None,
    inventory_options=None,
    viewing_map=False,
):
    # Screen dimensions
    screen_width = tcod.console_get_width(console)
    screen_height = tcod.console_get_height(console)

    # The center coordinates of the screen
    center_x = int(screen_width / 2)
    center_y = int(screen_height / 2)

    if key_cursor:
        camera_x = key_cursor[0]
        camera_y = key_cursor[1]
    else:
        camera_x = player.x
        camera_y = player.y

    # The map coordinates of the top left character displayed on the screen
    top_left_x = camera_x - center_x
    top_left_y = camera_y - center_y

    if game_state is GameStates.VICTORY:
        tcod.console_clear(console)
        tcod.console_print_ex(
            console,
            center_x,
            center_y,
            tcod.BKGND_DEFAULT,
            tcod.CENTER,
            "You Win!",
        )
        tcod.console_blit(console, 0, 0, screen_width, screen_height, 0, 0, 0)
        return

    # Draw all visible and remembered tiles
    for x in range(screen_width):
        for y in range(screen_height):
            tile_x = x + top_left_x
            tile_y = y + top_left_y
            if game_map.contains(tile_x, tile_y) and (
                viewing_map or memory[tile_x][tile_y]
            ):
                tile = game_map.get_tile(tile_x, tile_y, value=False)
                foreground = color_scheme.foreground.get(tile)
                background = color_scheme.background.get(tile)

                if viewing_map or tcod.map_is_in_fov(fov_map, tile_x, tile_y):
                    if color_scheme.allow_fade and not viewing_map:
                        foreground = apply_fov_gradient(
                            foreground,
                            distance(player.x, player.y, tile_x, tile_y),
                            player.sight.fov_radius,
                        )
                        background = apply_fov_gradient(
                            background,
                            distance(player.x, player.y, tile_x, tile_y),
                            player.sight.fov_radius,
                        )
                else:
                    foreground = color_scheme.get_memory_color(foreground)
                    background = color_scheme.get_memory_color(background)

                tcod.console_set_default_foreground(console, foreground)
                tcod.console_put_char(console, x, y, tile.value.character)
                tcod.console_set_char_background(
                    console, x, y, background, tcod.BKGND_SET
                )
            else:
                tcod.console_set_default_foreground(
                    console, color_scheme.foreground[None]
                )
                tcod.console_put_char(console, x, y, " ")
                tcod.console_set_char_background(
                    console,
                    x,
                    y,
                    color_scheme.background[None],
                    tcod.BKGND_SET,
                )

    # Sort entities by their render order
    ordered_entities = sorted(
        game_map.entities, key=lambda i: i.render_order.value, reverse=True
    )

    # Draw all visible entities
    for entity in ordered_entities:
        if viewing_map or tcod.map_is_in_fov(fov_map, entity.x, entity.y):
            tcod.console_set_default_foreground(console, entity.color)
            tcod.console_put_char(
                console,
                entity.x - top_left_x,
                entity.y - top_left_y,
                entity.char,
                tcod.BKGND_NONE,
            )

    if key_cursor:
        tcod.console_set_default_foreground(console, tcod.white)
        tcod.console_put_char(
            console, center_x, center_y, "X", tcod.BKGND_NONE
        )

    tcod.console_blit(console, 0, 0, screen_width, screen_height, 0, 0, 0)

    if viewing_map:
        return

    # Panel dimensions
    panel_width = tcod.console_get_width(panel)
    panel_height = tcod.console_get_height(panel)
    panel_y = screen_height - panel_height

    tcod.console_set_default_background(panel, tcod.black)
    tcod.console_clear(panel)

    cursor_x = mouse.cx + top_left_x
    cursor_y = mouse.cy + top_left_y

    if tcod.map_is_in_fov(fov_map, cursor_x, cursor_y):
        entities_at_cursor = game_map.get_entities_at_tile(cursor_x, cursor_y)
        if entities_at_cursor:
            names = join_list(
                [entity.indefinite_name for entity in entities_at_cursor]
            )
            if len(names) > screen_width - 2:
                names = (
                    str(len(entities_at_cursor))
                    + " entities (right-click to list all)"
                )

            tcod.console_set_default_foreground(panel, tcod.light_gray)
            tcod.console_print_ex(
                panel, 1, 0, tcod.BKGND_NONE, tcod.LEFT, names
            )

    # Print the game messages, one line at a time
    message_y = 1
    for i in range(
        max(0, len(message_log.messages) - panel_height + 1),
        max(0, len(message_log.messages)),
    ):
        message = message_log.messages[i]
        tcod.console_set_default_foreground(panel, message.color)
        tcod.console_print_ex(
            panel,
            message_log.x,
            message_y,
            tcod.BKGND_NONE,
            tcod.LEFT,
            message.text,
        )
        message_y += 1

    render_bar(
        panel,
        1,
        1,
        bar_width,
        "HP",
        player.fighter.hp,
        player.fighter.max_hp,
        tcod.red,
        tcod.darker_red,
    )
    tcod.console_print_ex(
        panel,
        1,
        2,
        tcod.BKGND_NONE,
        tcod.LEFT,
        f"Attack:  {player.fighter.attack}",
    )
    tcod.console_print_ex(
        panel,
        1,
        3,
        tcod.BKGND_NONE,
        tcod.LEFT,
        f"Defense: {player.fighter.defense}",
    )
    tcod.console_print_ex(
        panel,
        1,
        4,
        tcod.BKGND_NONE,
        tcod.LEFT,
        f"Damage:  {player.fighter.damage}",
    )
    tcod.console_set_default_foreground(panel, tcod.yellow)
    tcod.console_print_ex(
        panel,
        1,
        5,
        tcod.BKGND_NONE,
        tcod.LEFT,
        f"Dungeon Level: {game_map.dungeon_level}",
    )

    tcod.console_blit(panel, 0, 0, panel_width, panel_height, 0, 0, panel_y)

    if game_state == GameStates.INVENTORY:
        item_count = len(player.container.items)
        capacity = player.container.capacity
        inventory_menu(
            console,
            f"Inventory ({item_count}/{capacity})\n",
            player,
            50,
            screen_width,
            screen_height,
            menu_selection,
            inventory_options,
        )


def clear_all(console, entities, player):
    screen_width = tcod.console_get_width(console)
    screen_height = tcod.console_get_height(console)

    for entity in entities:
        tcod.console_put_char(
            console,
            entity.x - player.x + int(screen_width / 2),
            entity.y - player.y + int(screen_height / 2),
            " ",
            tcod.BKGND_NONE,
        )


# Used to brighten tiles near the player and darken ones further away
def apply_fov_gradient(
    tile_color,
    tile_distance,
    fov_radius,
    brightness_range=32,
    max_brightness=16,
):
    color_mod = (
        int(brightness_range * (tile_distance / fov_radius)) - max_brightness
    )

    # If the color modifier is above zero, the tile is darkened, otherwise it
    # is lightened
    if color_mod >= 0:
        return tile_color.__sub__(Color(color_mod, color_mod, color_mod))
    color_mod = -color_mod
    return tile_color.__add__(Color(color_mod, color_mod, color_mod))
