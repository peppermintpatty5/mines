#ifndef MINES_H_
#define MINES_H_

#include <stdbool.h>

/**
 * A tile uniquely describes a cell. Numeric tiles have corresponding numeric
 * values.
 */
enum tile
{
    TILE_ZERO,
    TILE_ONE,
    TILE_TWO,
    TILE_THREE,
    TILE_FOUR,
    TILE_FIVE,
    TILE_SIX,
    TILE_SEVEN,
    TILE_EIGHT,
    TILE_PLAIN,
    TILE_MINE,
    TILE_DETONATED,
    TILE_FLAG_RIGHT,
    TILE_FLAG_WRONG
};

/**
 * An infinite game of minesweeper.
 */
typedef struct minesweeper Minesweeper;

/**
 * The density parameter determines what proportion of cells are mines and shall
 * be in the range [0, 1].
 */
extern Minesweeper *minesweeper_new(double density);

/**
 * Uncover the cell at the given coordinate. Return true if the move is legal,
 * false otherwise.
 */
extern bool uncover(Minesweeper *game, long x, long y);

/**
 * Set/unset a flag at the given coordinate. A flag precludes a cell from being
 * uncovered. Return true if the move is legal, false otherwise.
 */
extern bool flag(Minesweeper *game, long x, long y);

/**
 * Perform a "chord" move at the given coordinate. Return true if the move is
 * legal, false otherwise.
 */
extern bool chord(Minesweeper *game, long x, long y);

/**
 * Get the tile associated with the cell at the given coordinate.
 */
extern enum tile get_tile(Minesweeper *game, long x, long y);

#endif
