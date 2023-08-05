from enum import Enum

from .dungeon_generator import (
    EMPTY,
    ROOM_FLOOR,
    CORRIDOR_FLOOR,
    DOOR,
    DEADEND,
    ROOM_WALL,
    CORRIDOR_WALL,
    CAVE_WALL,
    CAVE_FLOOR,
    STAIRS,
)


class Tile:
    """
    A map tile which may or may not be blocked, and may or may not block sight.
    """

    def __init__(self, blocks, blocks_sight=None, character=None):
        self.blocks = blocks

        # By default, if a tile is blocked, it also blocks sight
        if blocks_sight is None:
            self.blocks_sight = blocks
        else:
            self.blocks_sight = blocks_sight

        if character is None:
            character = "#" if blocks else "."

        self.character = character


class Tiles(Enum):
    ROOM_FLOOR = Tile(False)
    ROOM_WALL = Tile(True)
    CORRIDOR_FLOOR = Tile(False)
    CORRIDOR_WALL = Tile(True)
    CAVE_FLOOR = Tile(False)
    CAVE_WALL = Tile(True)
    DOOR = Tile(False, True, "+")
    ROOM_STAIRS = Tile(True, False, ">")
    CAVE_STAIRS = Tile(True, False, ">")


int_to_tile_map = {
    EMPTY: Tiles.CAVE_WALL,
    ROOM_FLOOR: Tiles.ROOM_FLOOR,
    CORRIDOR_FLOOR: Tiles.CORRIDOR_FLOOR,
    DOOR: Tiles.DOOR,
    DEADEND: Tiles.CORRIDOR_FLOOR,
    ROOM_WALL: Tiles.ROOM_WALL,
    CORRIDOR_WALL: Tiles.CORRIDOR_WALL,
    CAVE_WALL: Tiles.CAVE_WALL,
    CAVE_FLOOR: Tiles.CAVE_FLOOR,
    STAIRS: Tiles.ROOM_STAIRS,
}
