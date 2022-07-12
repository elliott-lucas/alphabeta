# Alpha-Beta Pruning Program

An program for playing arbitrary two-player adversarial games using the [Alpha-Beta Pruning](https://en.wikipedia.org/wiki/Alpha-beta_pruning) algorithm. 

Various examples of games are included (Hex, Tic Tac Toe, 21, etc.).

## Defining a Game

Games are created as a subclass of the Game class and must define its abstract functions:

- `getPossibleMoves` - How to get all current possible moves for the current player.
- `getEvaluation` - How to get a numerical evaluation of the current game state.
- `playMove` - How to play a given move.

Additionally, definitions can be added for `getInput` and `drawGame` to allow for human players and graphics.
