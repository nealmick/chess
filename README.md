# Chess Engine

SunFish engine implemented using the Django and Chess libraries 


There are more unique chess game states, than atoms in the known universe(10^111).  The engine evaluates any position and finds the best move.  Evaluation is done by first generating a tree structure that contains every possible board state up to a certain depth (moves ahead).  The root of the tree is the current game state.  Each branch of the tree is a possible move.  Every level of depth in the tree the player flips (MiniMax).  Terminal state of each branch is reached at the max depth or can be cut early if the branch score drops below a certain value(alpha/beta pruning).  Each branch is evaluated based on a scoring system.  The scoring system works by assigning each piece a value and adding or subtracting that value to the current branch score if the piece is captured.  Positions are also evaluated based on where each piece is located on the board, a piece map where knights are best in the center, pawns are encouraged to move forward, etc… The best score is kept while traversing the tree and updated if a better branch score is found.  Once every move is evaluated the board is converted to a FEN string and sent back to the front end.  The engine is written in Python and is a fork of an engine called Sunfish.  All of the tree computation occurs on the server.  The server is a Django web application which receives and replies to requests from the front end.

#### Django apps:
1.  Mysite - Default django app.
2.  chessBot - Logic for receiving board states, move generation, and returning board state.

#### Install:

```bash
git clone https://github.com/nealmick/chess
cd chess
pip install -r requirements.txt
python3 manage.py runserver
```


<img src="https://i.imgur.com/5g4ZcGh.png" width="400" height="500" />



Think you can beat it?
# Live:
https://nealmick.com/chess/

# Sunfish:
https://github.com/thomasahle/sunfish

