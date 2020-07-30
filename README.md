# mines

Set-based implementation of minesweeper in Python

## Overview

Typically, minesweeper is implemented using a 2D array of cells. The following table shows an example grid containing all possible cells. The two missing combinations reflect the fact that `dug` and `flag` properties are mutually exclusive (cannot both be true).

```txt
+-----+-----+------+------+------+
| row | col | dug  | flag | mine |
+-----+-----+------+------+------+
|   0 |   0 |    0 |    0 |    0 |
|   0 |   1 |    0 |    0 |    1 |
|   0 |   2 |    0 |    1 |    0 |
|   1 |   0 |    0 |    1 |    1 |
|   1 |   1 |    1 |    0 |    0 |
|   1 |   2 |    1 |    0 |    1 |
+-----+-----+------+------+------+
```

The printout of the grid would look like this:

```txt
- * X
^ 3 @
```

Now, the above table translated into three sets. Like before, the `dug` and `flag` sets are disjoint (intersection is the empty set).

```py
dug = {(1, 1), (1, 2)}
flag = {(0, 2), (1, 0)}
mine = {(0, 1), (1, 0), (1, 2)}
```

The result of this alteration is a program that is less efficient, but far more elegant in terms of mathematical reasoning and code style. It also retains the same time/space complexities, as will be explained below.

## Mathematical background

The following set properties translate directly into Python code optimizations:
<!-- One day, GitHub will bestow upon us built-in LaTeX rendering. -->
![x \in A \cup B \equiv x \in A \vee x \in B](https://latex.codecogs.com/svg.latex?x%20%5Cin%20A%20%5Ccup%20B%20%5Cequiv%20x%20%5Cin%20A%20%5Cvee%20x%20%5Cin%20B)

![x \in A \cap B \equiv x \in A \wedge x \in B](https://latex.codecogs.com/svg.latex?x%20%5Cin%20A%20%5Ccap%20B%20%5Cequiv%20x%20%5Cin%20A%20%5Cwedge%20x%20%5Cin%20B)

![x \in A - B \equiv x \in A \wedge x \notin B](https://latex.codecogs.com/svg.latex?x%20%5Cin%20A%20-%20B%20%5Cequiv%20x%20%5Cin%20A%20%5Cwedge%20x%20%5Cnotin%20B)

```py
(x in A | B) is (x in A or x in B)
(x in A & B) is (x in A and x in B)
(x in A - B) is (x in A and x not in B)
```

In cases where `A` is of constant size, `&` and `-` are `O(1)`.

| Operation |  Average case  |
| :-------- | :------------: |
| `A \| B`  |   `O(a + b)`   |
| `A & B`   | `O(min(a, b))` |
| `A - B`   |     `O(a)`     |

## Algorithm descriptions

*Note:* For simplicity, the number of mines is assumed to be proportional to the number of cells. Therefore, `n` will be used to describe both quantities simultaneously.

* **dig** `O(1)` - Uncovers a cell by adding it to `dug`
* **flag** `O(1)` - Toggles a cell's flag on/off by adding/removing it to/from `dug`
* **chord** `O(1)` - Checks if the number of adjacent flags equals the number of adjacent mines, then adds the adjacent non-flag cells to `dug`
