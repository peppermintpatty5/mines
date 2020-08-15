# mines

Set-based implementation of minesweeper in Python

## Data structures

A minesweeper grid is defined by three sets of integer pairs. These sets denote the indices of revealed cells, flagged cells, and cells that are mines respectively:

$$ R, F, M \subset \mathbb Z ^ 2 $$

Since a cell cannot be both revealed and flagged, the following sets must always be disjoint:

$$ R \cap F = \emptyset $$

*Disclaimer:* An infinite minesweeper grid would be silly, so restrictions must be made according to the number of rows and columns.

## Algorithms

Let `A` be the set of cells adjacent to `x = (r, c)`:

$$ A = \left ( \left \{ r - 1, r, r + 1 \right \} \times \left \{ c - 1, c, c + 1 \right \} \right ) \setminus \left \{ \left ( r, c \right ) \right \} $$

### Reveal

**Condition** - `x` is not flagged:

$$ x \notin F $$

**Action** - Adds `x` to `R`:

$$ R \cup \left \{ x \right \} $$

### Flag

**Condition** - `x` has not been revealed:
$$ x \notin R $$

**Action** - If `x` is flagged, then it will be un-flagged and vice versa. This is done rather neatly by updating `F` via symmetric difference:

$$ F \triangle \left \{ x \right \} $$

### Chord

**Condition** - `x` has been revealed and is not a mine and the number of adjacent flags plus the number of adjacent revealed mines equals the number of adjacent mines:

$$ x \in R \wedge x \notin M \wedge \left | A \cap F \right | + \left | A \cap R \cap M \right | = \left | A \cap M \right | $$

**Action** - Adds adjacent non-flagged cells to `R`:

$$ R \cup \left ( A \setminus F \right ) $$
