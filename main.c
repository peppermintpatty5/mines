#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "mines.h"

int main(void)
{
    long x, y;
    char const *legend = " 12345678-*@#X";
    Minesweeper *game = minesweeper_new(0.17);

    srand(time(NULL));

    for (y = 0; y < 16; y++)
        for (x = 0; x < 30; x++)
            uncover(game, x, y);

    for (y = 0; y < 16; y++)
    {
        for (x = 0; x < 30; x++)
        {
            putchar(' ');
            putchar(legend[get_tile(game, x, y)]);
        }

        putchar('\n');
    }

    return EXIT_SUCCESS;
}
