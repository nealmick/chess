# Chess Engine

This project is built using the django library.  The front end game was built using the chess and chessboard javascript libraries.  This engine is a fork of the SunFish engine.  Upon a move being made a FEN string is generated representing the board and is sent to the server via jquery.  The django server then creates a board and updates its status to the FEN representation.  The engine calculates the position and outputs a move.  The engine works by first generating all legal moves up to a certain depth.  Each position is then evaluated by a scoring system.  The scoring system works by assigning each piece a value and a piece bonus map is then added making certain pieces more valuable on certain squares.  Once every piece has been added up the move is then outputted, and the board is converted back to a FEN string and sent to the front end. 

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

Think you can beat it?
# Live:
https://nealmick.com/chess/

