#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "mines.h"
#include "textui.h"

int main(void)
{
    Minesweeper *game = minesweeper_new(0.10);

    srand(time(NULL));
    textui_run(game);

    return EXIT_SUCCESS;
}
