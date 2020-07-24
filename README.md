# mines

Set-based implementation of minesweeper in Python

## Overview

Typically, minesweeper is implemented using a 2D array of cells. The following table shows an example grid of all possible cells. The two missing combinations reflect the fact that `dug` and `flag` properties are mutually exclusive.

| row  | col  |  dug  | flag  | mine  |
| :--- | :--- | :---: | :---: | :---: |
| 0    | 0    |       |       |       |
| 0    | 1    |       |       |   X   |
| 0    | 2    |       |   X   |       |
| 1    | 0    |       |   X   |   X   |
| 1    | 1    |   X   |       |       |
| 1    | 2    |   X   |       |   X   |

The printout of the grid would look like this:

```txt
- * X
^ 3 @
```

Now, the above table translated into three sets:

```py
dug = {(1, 1), (1, 2)}
flag = {(0, 2), (1, 0)}
mine = {(0, 1), (1, 0), (1, 2)}
```

The end result of this simple data transformation is a program that is less efficient, but far more elegant in terms of mathematical reasoning and code style. It also retains the same time/space complexities, as will be explained below.

*Note:* For simplicity, the number of mines is assumed to be proportional to the number of cells. Therefore, `n` will be used to describe both quantities simultaneously.

----

WIP
