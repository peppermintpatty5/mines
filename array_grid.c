#include <stdlib.h>

#include "array_grid.h"

struct array_grid
{
    struct cell
    {
        bool is_mine : 1;
        bool is_uncovered : 1;
        bool is_flagged : 1;
    } *cells;
    long x_min, x_max, y_min, y_max;
};

ArrayGrid *array_grid_new(long x_min, long x_max, long y_min, long y_max)
{
    ArrayGrid *grid = malloc(sizeof(ArrayGrid));

    if (grid != NULL)
    {
        unsigned long cols = x_max - x_min,
                      rows = y_max - y_min,
                      r, c;
        struct cell *cell;

        grid->cells = malloc(sizeof(struct cell) * rows * cols);
        grid->x_min = x_min;
        grid->x_max = x_max;
        grid->y_min = y_min;
        grid->y_max = y_max;

        cell = grid->cells;
        for (r = 0; r < rows; r++)
        {
            for (c = 0; c < cols; c++)
            {
                cell->is_mine = false;
                cell->is_uncovered = false;
                cell->is_flagged = false;
                cell++;
            }
        }
    }

    return grid;
}

static struct cell *get_cell(ArrayGrid *grid, long x, long y)
{
    if (grid->x_min <= x && x < grid->x_max &&
        grid->y_min <= y && y < grid->y_max)
    {
        unsigned long cols = grid->x_max - grid->x_min,
                      r = x - grid->x_min,
                      c = y - grid->y_min;

        return &grid->cells[r * cols + c];
    }
    else
    {
        return NULL;
    }
}

bool array_grid_is_mine(ArrayGrid *grid, long x, long y)
{
    struct cell *cell = get_cell(grid, x, y);
    return cell != NULL && cell->is_mine;
}

bool array_grid_is_uncovered(ArrayGrid *grid, long x, long y)
{
    struct cell *cell = get_cell(grid, x, y);
    return cell != NULL && cell->is_uncovered;
}

bool array_grid_is_flagged(ArrayGrid *grid, long x, long y)
{
    struct cell *cell = get_cell(grid, x, y);
    return cell != NULL && cell->is_flagged;
}

void array_grid_set_mine(ArrayGrid *grid, long x, long y, bool val)
{
    struct cell *cell = get_cell(grid, x, y);
    if (cell != NULL)
        cell->is_mine = val;
}

void array_grid_set_uncovered(ArrayGrid *grid, long x, long y, bool val)
{
    struct cell *cell = get_cell(grid, x, y);
    if (cell != NULL)
        cell->is_uncovered = val;
}

void array_grid_set_flagged(ArrayGrid *grid, long x, long y, bool val)
{
    struct cell *cell = get_cell(grid, x, y);
    if (cell != NULL)
        cell->is_flagged = val;
}
