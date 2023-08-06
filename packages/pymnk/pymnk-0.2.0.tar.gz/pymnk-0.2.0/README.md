# pymnk: library for k-in-a-row games
## Introduction
Pymnk is a Python library for k-in-a-row family of games, including:
- (m,n,k)-game
- Pente
- Connect6
- Ultimate tic-tac-toe
- Some tic-tac-toe variants

## Features
- Most of the games support N players, n-by-m board including ∞-by-∞ with k-in-a-row to win.
- Legal move generation, checking wins and draws
- Tracking board history and reverting moves
- Creating and parsing FEN
- Engine evaluation

## Installing
Install the latest release using pip
```
pip install pymnk
```

## Usage

Initializing game instances
```python
>>> from pymnk import *
>>> ttt = TicTacToe(m=3, n=3, k=3, infinite=False, players=2)
>>> pente = Pente(m=19, n=19, k=5, infinite=False, players=2)
>>> connect6 = Connect6(m=19, n=19, k=6, p=2, q=1, infinite=False)
>>> ult = UltimateTicTacToe(m=3, n=3, k=3, which_local_board=(0,0), players=2)
```

Making moves
```python
>>> ttt.move(0,1)
>>> ttt.move(1,1)
>>> ttt.move(0,2)
>>> ttt.move(2,2)
>>> ttt.move(0,0)
```

Some games have their own methods for moves:
```python
>>> connect6.move_sequence([(0,1)])
>>> connect6.move_sequence([(2,2), (3,2)])
```

Checking wins and draws
```python
>>> ttt.result()
<Result.WIN: 1>

>>> ttt.get_winner()
<Piece.X: 1>
```

Getting board history and reverting moves
```python
>>> ttt.pop()
>>> ttt.move_history
[(0, 1), (1, 1), (0, 2), (2, 2)]
```

Creating and parsing FEN
```python
>>> ttt.fen
'1XX/1O1/2O X 3'
```

```python
>>> print(Pente.from_fen('XX1/O1O/3 X 3'))
XX.
O.O
...
```

Showing a simple ASCII board
```python
>>> print(ttt)
.XX
.O.
..O
```

Getting legal moves
```python
>>> print(list(ttt.legal_moves()))
[(0, 0), (1, 0), (1, 2), (2, 0), (2, 1)]
```

Showing a fancy Unicode board
```python
>>> print(ttt.unicode())
🟩⬜⬜
🟩⬛🟩
🟩🟩⬛
```

Resetting a board
```python
>>> ttt.reset()
>>> ttt
TicTacToe.from_fen('3/3/3 X 1')
```

## License

Pymnk is available under the MIT license. For the full text, check out `LICENSE`.