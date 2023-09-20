#include <stdlib.h>

#include "array_grid.h"
#include "mines.h"

#define X_MIN -128
#define X_MAX 127
#define Y_MIN -128
#define Y_MAX 127

typedef bool(predicate_t)(Minesweeper *, long, long);
typedef void(action_t)(Minesweeper *, long, long);

struct minesweeper
{
    ArrayGrid *grid;
    double density;
    long uncovered_count;
    long detonated_count;
};

/**
 * Return true if the predicate is true for all cells adjacent to the given
 * coordinate, false otherwise.
 */
static bool
all_adjacent(Minesweeper *game, long x, long y, predicate_t *predicate)
{
    long u, v;

    for (u = x - 1; u <= x + 1; u++)
        for (v = y - 1; v <= y + 1; v++)
            if (u != x || v != y)
                if (!predicate(game, u, v))
                    return false;
    return true;
}

/**
 * Count the number of cells adjacent to the given coordinate which satisfy the
 * predicate.
 */
static int
count_adjacent(Minesweeper *game, long x, long y, predicate_t *predicate)
{
    int n = 0;
    long u, v;

    for (u = x - 1; u <= x + 1; u++)
        for (v = y - 1; v <= y + 1; v++)
            if (u != x || v != y)
                if (predicate(game, u, v))
                    n++;
    return n;
}

/**
 * Perform the action for all cells adjacent to the given coordinate which
 * satisfy the optional predicate.
 */
static void
foreach_adjacent(Minesweeper *game, long x, long y,
                 predicate_t *predicate,
                 action_t *action)
{
    long u, v;

    for (u = x - 1; u <= x + 1; u++)
        for (v = y - 1; v <= y + 1; v++)
            if (u != x || v != y)
                if (predicate == NULL || predicate(game, u, v))
                    action(game, u, v);
}

static bool is_mine(Minesweeper *game, long x, long y)
{
    return array_grid_is_mine(game->grid, x, y);
}

static bool is_uncovered(Minesweeper *game, long x, long y)
{
    return array_grid_is_uncovered(game->grid, x, y);
}

static bool is_flagged(Minesweeper *game, long x, long y)
{
    return array_grid_is_flagged(game->grid, x, y);
}

static bool not_uncovered(Minesweeper *game, long x, long y)
{
    return !is_uncovered(game, x, y);
}

static bool is_detonated(Minesweeper *game, long x, long y)
{
    return is_uncovered(game, x, y) && is_mine(game, x, y);
}

static void uncover_action(Minesweeper *game, long x, long y)
{
    uncover(game, x, y);
}

#define is_mine(x, y) is_mine(game, x, y)
#define is_uncovered(x, y) is_uncovered(game, x, y)
#define is_flagged(x, y) is_flagged(game, x, y)
#define set_mine(x, y, val) \
    array_grid_set_mine(game->grid, x, y, val)
#define set_uncovered(x, y, val) \
    array_grid_set_uncovered(game->grid, x, y, val)
#define set_flagged(x, y, val) \
    array_grid_set_flagged(game->grid, x, y, val)
#define count_adj(x, y, predicate) \
    count_adjacent(game, x, y, predicate)

Minesweeper *minesweeper_new(double density)
{
    Minesweeper *game = malloc(sizeof(Minesweeper));

    if (game != NULL)
    {
        game->grid = array_grid_new(X_MIN, X_MAX, Y_MIN, Y_MAX);
        game->density = density;
        game->uncovered_count = 0;
        game->detonated_count = 0;
    }

    return game;
}

/**
 * Randomly generate a mine at the given coordinate if the cell is not adjacent
 * to any uncovered cells.
 */
static void generate_mine(Minesweeper *game, long x, long y)
{
    if (all_adjacent(game, x, y, not_uncovered))
    {
        double r = (double)rand() / (double)((unsigned)RAND_MAX + 1);

        if (r < game->density)
            set_mine(x, y, true);
    }
}

bool uncover(Minesweeper *game, long x, long y)
{
    if (!is_uncovered(x, y) && !is_flagged(x, y))
    {
        /* the first cell uncovered should never be a mine */
        if (game->uncovered_count > 0)
            generate_mine(game, x, y);

        /* generate mines in adjacent cells */
        foreach_adjacent(game, x, y, not_uncovered, generate_mine);

        /* uncover the cell */
        set_uncovered(x, y, true);
        game->uncovered_count++;
        if (is_mine(x, y))
            game->detonated_count++;

        return true;
    }
    return false;
}

bool flag(Minesweeper *game, long x, long y)
{
    if (!is_uncovered(x, y))
    {
        set_flagged(x, y, !is_flagged(x, y));

        return true;
    }
    return false;
}

bool chord(Minesweeper *game, long x, long y)
{
    if (is_uncovered(x, y) && !is_mine(x, y) &&
        count_adj(x, y, is_flagged) + count_adj(x, y, is_detonated) ==
            count_adj(x, y, is_mine))
    {
        foreach_adjacent(game, x, y, NULL, uncover_action);

        return true;
    }
    return false;
}

enum tile get_tile(Minesweeper *game, long x, long y)
{
    return is_mine(x, y)
               ? (is_uncovered(x, y)
                      ? TILE_DETONATED
                      : (is_flagged(x, y) ? TILE_FLAG_RIGHT : TILE_MINE))
               : (is_uncovered(x, y)
                      ? count_adj(x, y, is_mine)
                      : (is_flagged(x, y) ? TILE_FLAG_WRONG : TILE_PLAIN));
}
