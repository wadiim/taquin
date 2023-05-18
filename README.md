# Taquin

An N-puzzle solver written for a class project.

## Usage

```sh
python main.py <strategy> <parameter> <puzzle-file> <solution-file> <stats-file>
```
where:

* `<strategy>` — The algorithm that will be used to solve the puzzle. Can be one of the following: `bfs` (Breadth-first search), `dfs` (Depth-first search), `astr` (A*);
* `<parameter>` — The algorithm's parameter. In case of BFS and DFS, it is the search order specified by a string that is permutation of the following four upper case letters: L (left), R (right), U (up), and D (down). In case of A*, it is a heuristic that can be one of the following: `hamm` (Hamming distance), or `manh` (Manhattan distance);
* `<puzzle-file>` — The path to the file containing the puzzle to solve. The format of this file is specified later in this document (see section [Puzzle file](###-Puzzle-file));
* `<solution-file>` — The path to the file that the solution will be written to. The format of this file is specified later in this document (see section [Solution file](###-Solution-file));
* `<stats-file>` — The path to the file that the additional information about the calculation process will be written to. The format of this file is specified later in this document (see section [Stats file](###-Stats-file));

### Puzzle file

The program reads the initial state of the puzzle from a file in which the first line should contain two integers `r` and `c` separated by space that determine the vertical (number of rows) and horizontal (number of columns) dimensions of the puzzle, respectively. Each of the remaining `r` lines contains `c` space-separated integers that describe the location of the individual pieces of the puzzle, with a value of `0` indicating an empty space.

Example:
```
4 4
1 2 3 4
5 6 7 8
10 13 11 12
9 14 0 15
```

### Solution file

The program generates a solution file that contains two lines. The first line contains an integer `n` that specifies the length of the found solution (i.e., the length of the sequence of moves corresponding to the shifts of the free field that will lead the puzzle from the given initial state to the goal state). The second line contains a sequence of `n` upper case letters corresponding to the individual movements of the empty field within the found solution. If the program has not found a solution for the puzzle, then the solution file consists of only a single line, which contains the number `-1`.

Example:
```
7
LULDRRR
```

### Stats file

The program generates a file containing additional information about the calculation process. It consists of 5 lines, each of which contains a number representing respectively:

* 1st line (integer): the length of the solution found - with the same value as in the file with the solution (where the program did not find a solution, this value is -1);
* 2nd line (integer): number of states visited;
* 3rd line (integer): number of processed states;
* 4th line (integer): maximum recursion depth reached;
* 5th line (real number accurate to 3 decimal places): duration of the calculation process in milliseconds.

Example:
```
7
29
14
7
0.502
```

## Benchmarking

There is a `benchmark.py` script that can be used to measure the execution time of different parts of the program. Run it as follows:

```sh
python benchmark.py
```

## Research

The task was to examine all the possible initial states of the 15-puzzle at distances 1-7 from the solved state (a total of 413 states). For the BFS and DFS strategies, all of the following search orders had to be used:

* right-down-up-left
* right-down-left-up
* down-right-up-left
* down-right-left-up
* left-up-down-right
* left-up-right-down
* up-left-down-right
* up-left-right-down

All the result were combined into a single CSV file (where space rather than comma was used as a separator). Next, the script `plotter.py` was used to generate bar diagrams showing the average solution length, average number of visited states, average number of processed states, and average recursion depth for each algorithm and parameter combination.

### Results

<p align="center">
	<img src="https://github.com/wadiim/taquin/assets/33803413/ddce547d-c7ca-4a05-9322-d500abae95b4" width="49%" />
	<img src="https://github.com/wadiim/taquin/assets/33803413/fd7862a0-6042-415e-a9d5-7c014bc8a426" width="49%" />
	<img src="https://github.com/wadiim/taquin/assets/33803413/1ee3114d-b07a-4c36-8a14-79455056a4ae" width="49%" />
	<img src="https://github.com/wadiim/taquin/assets/33803413/e054a80d-3ae6-484b-aa56-db1e99dc6407" width="49%" />
</p>

<p align="center">
	<img src="https://github.com/wadiim/taquin/assets/33803413/22baf03b-0374-45d3-bc45-97cdf095b8f8" width="49%" />
	<img src="https://github.com/wadiim/taquin/assets/33803413/09941c0e-f940-435c-8314-aba5e87a5b9c" width="49%" />
	<img src="https://github.com/wadiim/taquin/assets/33803413/d9694cd6-fddc-4548-8e71-672913776508" width="49%" />
	<img src="https://github.com/wadiim/taquin/assets/33803413/13a5c589-296a-46e4-8054-10e6f81d933e" width="49%" />
</p>

<p align="center">
	<img src="https://github.com/wadiim/taquin/assets/33803413/1f97ab6d-16a3-411c-a16e-008af74d7a7d" width="49%" />
	<img src="https://github.com/wadiim/taquin/assets/33803413/f3ab252d-7d15-49d8-9bc9-d7865929eda2" width="49%" />
	<img src="https://github.com/wadiim/taquin/assets/33803413/4623a3d1-30f2-4d69-b325-123c11d87558" width="49%" />
	<img src="https://github.com/wadiim/taquin/assets/33803413/fb944c66-97c0-429a-b555-9b86a983d949" width="49%" />
</p>

<p align="center">
	<img src="https://github.com/wadiim/taquin/assets/33803413/e0f8d1cd-7f6a-4074-80d8-d36f01e2a0e6" width="49%" />
	<img src="https://github.com/wadiim/taquin/assets/33803413/b226b2db-bce2-458b-9a42-9e6064f72bcf" width="49%" />
	<img src="https://github.com/wadiim/taquin/assets/33803413/d53af5c7-40a7-4209-a3d6-64571ccd043d" width="49%" />
	<img src="https://github.com/wadiim/taquin/assets/33803413/8c67e0ec-b7d6-454f-a263-0732decadba9" width="49%" />
</p>

<p align="center">
	<img src="https://github.com/wadiim/taquin/assets/33803413/3c2d5297-de98-485a-b61a-d94d4ff10401" width="49%" />
	<img src="https://github.com/wadiim/taquin/assets/33803413/1ca1eba2-dad0-4f1a-8f01-206cf652bc95" width="49%" />
	<img src="https://github.com/wadiim/taquin/assets/33803413/ef615948-710d-4e27-af5b-243e2e3ea5cb" width="49%" />
	<img src="https://github.com/wadiim/taquin/assets/33803413/3d2384d4-9e9f-4343-85b1-15e3cb8f08e7" width="49%" />
</p>

## License

[MIT](https://github.com/wadiim/taquin/blob/master/LICENSE)
