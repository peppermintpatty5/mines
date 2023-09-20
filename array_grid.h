#ifndef ARRAY_GRID_H_
#define ARRAY_GRID_H_

#include <stdbool.h>

typedef struct array_grid ArrayGrid;

extern ArrayGrid *
array_grid_new(long x_min, long x_max, long y_min, long y_max);

extern bool array_grid_is_mine(ArrayGrid *grid, long x, long y);

extern bool array_grid_is_uncovered(ArrayGrid *grid, long x, long y);

extern bool array_grid_is_flagged(ArrayGrid *grid, long x, long y);

extern void array_grid_set_mine(ArrayGrid *grid, long x, long y, bool val);

extern void array_grid_set_uncovered(ArrayGrid *grid, long x, long y, bool val);

extern void array_grid_set_flagged(ArrayGrid *grid, long x, long y, bool val);

#endif
