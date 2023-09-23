#include <ncurses.h>

#include "mines.h"

#define get_cursor_x(ui) ((ui)->anchor.x + (ui)->offset.x)
#define get_cursor_y(ui) ((ui)->anchor.y + (ui)->offset.y)

/**
 * Text user interface.
 */
struct text_ui
{
    Minesweeper *game;
    struct
    {
        long x, y;
    } anchor;
    struct
    {
        int x, y;
    } offset;
    int lives;
};

static char const TILE_CHAR[] = {
    [TILE_ZERO] = ' ',
    [TILE_ONE] = '1',
    [TILE_TWO] = '2',
    [TILE_THREE] = '3',
    [TILE_FOUR] = '4',
    [TILE_FIVE] = '5',
    [TILE_SIX] = '6',
    [TILE_SEVEN] = '7',
    [TILE_EIGHT] = '8',
    [TILE_PLAIN] = '-',
    [TILE_MINE] = '*',
    [TILE_DETONATED] = '@',
    [TILE_FLAG_RIGHT] = '#',
    [TILE_FLAG_WRONG] = 'X',
};
static struct color
{
    short fg;
    bool bold;
} TILE_COLORS[] = {
    [TILE_ZERO] = {COLOR_WHITE, false},
    [TILE_ONE] = {COLOR_BLUE, true},
    [TILE_TWO] = {COLOR_GREEN, false},
    [TILE_THREE] = {COLOR_RED, true},
    [TILE_FOUR] = {COLOR_BLUE, false},
    [TILE_FIVE] = {COLOR_RED, false},
    [TILE_SIX] = {COLOR_CYAN, false},
    [TILE_SEVEN] = {COLOR_WHITE, true},
    [TILE_EIGHT] = {COLOR_BLACK, true},
    [TILE_PLAIN] = {COLOR_BLACK, true},
    [TILE_MINE] = {COLOR_MAGENTA, false},
    [TILE_DETONATED] = {COLOR_YELLOW, true},
    [TILE_FLAG_RIGHT] = {COLOR_GREEN, true},
    [TILE_FLAG_WRONG] = {COLOR_MAGENTA, true},
};

static int color_attr(struct color color)
{
    short n = has_colors() ? color.fg + 1 : 0;

    return COLOR_PAIR(n) | (color.bold ? A_BOLD : A_NORMAL);
}

/**
 * Print status bar to screen.
 */
static void print_status_bar(struct text_ui *ui)
{
    int max_x = getmaxx(stdscr),
        max_y = getmaxy(stdscr),
        a, b, c;

    move(max_y - 1, 0);

    attrset(color_attr((struct color){COLOR_MAGENTA, false}) | A_REVERSE);
    printw(" %.1f%% %n", 0.69 * 100, &a);

    attrset(color_attr((struct color){COLOR_CYAN, false}) | A_REVERSE);
    printw(" Lives: %-4i Score: %-4i %nx: %-4li y: %-4li %n",
           4, 20, &b, get_cursor_x(ui), get_cursor_y(ui), &c);

    /* insert spaces to right-justify coordinate display */
    move(max_y - 1, a + b);
    for (int i = 0; i < max_x - (a + c); i++)
        insch(' ');
}

static void print_quit_confirm(void)
{
    int max_x = getmaxx(stdscr),
        max_y = getmaxy(stdscr);

    move(max_y - 1, 0);

    attrset(color_attr((struct color){COLOR_YELLOW, false}) | A_REVERSE);
    addstr(" Quit? [y/n]");

    for (int i = 0; i < max_x; i++)
        insch(' ');
}

/**
 * Print grid to screen.
 */
static void print_grid(struct text_ui *ui)
{
    int max_x = getmaxx(stdscr),
        max_y = getmaxy(stdscr);

    for (int y = 0; y < max_y - 1; y++)
    {
        for (int x = 0; x < max_x / 2; x++)
        {
            enum tile tile = get_tile(
                ui->game, ui->anchor.x + x, ui->anchor.y + y);

            if (ui->lives < 0) /* TODO */
            {
            }

            move(max_y - 2 - y, x * 2);
            attrset(color_attr(TILE_COLORS[tile]));
            addch(' ');
            addch(TILE_CHAR[tile]);
        }
    }
}

/**
 * Move cursor by given offset, scrolling the window to keep the cursor in
 * bounds.
 */
static void move_cursor(struct text_ui *ui, int dx, int dy)
{
    int max_x = getmaxx(stdscr) / 2,
        max_y = getmaxy(stdscr) - 1,
        x, y;

    x = (ui->offset.x += dx);
    y = (ui->offset.y += dy);

    if (x < 0)
    {
        ui->anchor.x += x;
        ui->offset.x = 0;
    }
    else if (x >= max_x)
    {
        ui->anchor.x += x - max_x + 1;
        ui->offset.x = max_x - 1;
    }

    if (y < 0)
    {
        ui->anchor.y += y;
        ui->offset.y = 0;
    }
    else if (y >= max_y)
    {
        ui->anchor.y += y - max_y + 1;
        ui->offset.y = max_y - 1;
    }
}

static void center_cursor(struct text_ui *ui)
{
    int max_x, max_y, dx, dy;

    getmaxyx(stdscr, max_y, max_x);
    max_x /= 2;
    max_y -= 1;

    dx = max_x / 2 - ui->offset.x;
    dy = max_y / 2 - ui->offset.y;

    ui->offset.x += dx;
    ui->offset.y += dy;
    ui->anchor.x -= dx;
    ui->anchor.y -= dy;
}

static void scroll_to(struct text_ui *ui, long x, long y)
{
    ui->anchor.x += x - get_cursor_x(ui);
    ui->anchor.y += y - get_cursor_y(ui);
}

static void game_loop(struct text_ui *ui)
{
    enum
    {
        PLAY,
        QUIT_CONFIRM,
        QUIT
    } state = PLAY;

    center_cursor(ui);

    while (state != QUIT)
    {
        int max_y = getmaxy(stdscr);
        long x = get_cursor_x(ui),
             y = get_cursor_y(ui);

        print_grid(ui);
        curs_set(2);

        switch (state)
        {
        case PLAY:
            print_status_bar(ui);
            move(max_y - 2 - ui->offset.y, ui->offset.x * 2 + 1);

            switch (getch())
            {
            case KEY_UP:
                move_cursor(ui, 0, +1);
                break;
            case KEY_DOWN:
                move_cursor(ui, 0, -1);
                break;
            case KEY_LEFT:
                move_cursor(ui, -1, 0);
                break;
            case KEY_RIGHT:
                move_cursor(ui, +1, 0);
                break;
            case KEY_ENTER:
            case '\r':
            case '\n':
                uncover(ui->game, x, y);
                break;
            case ' ':
                if (!flag(ui->game, x, y))
                    auto_chord(ui->game, x, y);
                break;
            case 'w':
                ui->anchor.y++;
                break;
            case 's':
                ui->anchor.y--;
                break;
            case 'a':
                ui->anchor.x--;
                break;
            case 'd':
                ui->anchor.x++;
                break;
            case 'W':
                ui->anchor.y += 5;
                break;
            case 'S':
                ui->anchor.y -= 5;
                break;
            case 'A':
                ui->anchor.x -= 5;
                break;
            case 'D':
                ui->anchor.x += 5;
                break;
            case '0':
                scroll_to(ui, 0, 0);
                break;
            case 'c':
                center_cursor(ui);
                break;
            case 'q':
                state = QUIT_CONFIRM;
                break;
            default:
                break;
            }
            break;
        case QUIT_CONFIRM:
            print_quit_confirm();
            curs_set(0);

            switch (getch())
            {
            case 'y':
            case 'Y':
                state = QUIT;
                break;
            case 'n':
            case 'N':
                state = PLAY;
                break;
            default:
                break;
            }
            break;
        default:
            break;
        }
    }
}

void textui_run(Minesweeper *game)
{
    struct text_ui ui = {
        .game = game,
        .anchor = {.x = 0, .y = 0},
        .offset = {.x = 0, .y = 0}};

    initscr();
    start_color();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);

    /* initialize color pairs for 8 basic colors */
    if (has_colors())
    {
        start_color();
        short background = use_default_colors() == OK ? -1 : 0;

        for (short color = 0; color < 8; color++)
            init_pair(color + 1, color, background);
    }

    game_loop(&ui);

    nocbreak();
    echo();
    keypad(stdscr, FALSE);
    endwin();
}
