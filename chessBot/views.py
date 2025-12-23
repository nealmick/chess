from django.shortcuts import render
import pickle
import os
import json
# Create your views here.
from django.http import HttpResponse, JsonResponse
from . import sunfish

from . import tools

# File to store the move history
MOVES_FILE = os.path.join(os.path.dirname(__file__), 'moves_history.json')

# Starting position FEN
START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

def parse_fen_to_board(fen):
    """Parse FEN string into 8x8 list."""
    board = []
    position = fen.split(' ')[0]
    rows = position.split('/')
    for row in rows:
        board_row = []
        for char in row:
            if char.isdigit():
                board_row.extend(['.'] * int(char))
            else:
                board_row.append(char)
        board.append(board_row)
    return board

def find_moves_from_boards(old_board, new_board, color):
    """Compare two board arrays and return list of moves (handles castling)."""
    froms = []  # squares where pieces left
    tos = []    # squares where pieces arrived

    for y in range(8):
        for x in range(8):
            old_piece = old_board[y][x]
            new_piece = new_board[y][x]

            if old_piece == new_piece:
                continue

            # Piece left this square
            if old_piece != '.' and new_piece == '.':
                froms.append((x, 7 - y, old_piece))
            # Piece arrived (or replaced another)
            elif new_piece != '.' and old_piece != new_piece:
                captured = old_piece if old_piece != '.' else None
                tos.append((x, 7 - y, new_piece, captured))

    moves = []
    # Match each "to" with its corresponding "from" by piece type
    for to_x, to_y, piece, captured in tos:
        for i, (fx, fy, fp) in enumerate(froms):
            if fp == piece:
                moves.append({
                    'from': [fx, fy],
                    'to': [to_x, to_y],
                    'capture': captured,
                    'color': color
                })
                froms.pop(i)
                break

    return moves

def load_moves():
    try:
        with open(MOVES_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'last_fen': START_FEN, 'moves': []}

def save_moves(data):
    with open(MOVES_FILE, 'w') as f:
        json.dump(data, f)

def index(request):
    return render(request,'chessBot/index.html')


def getState(request):
    """Return the list of moves with from/to/capture info."""
    data = load_moves()
    return JsonResponse({'moves': data['moves'], 'count': len(data['moves'])})


def resetGame(request):
    """Reset the game history."""
    save_moves({'last_fen': START_FEN, 'moves': []})
    return JsonResponse({'status': 'reset', 'moves': []})




def nextMoveSunFish(request):
    context = {}
    
    print('sunfish move!')
       
    url = request.build_absolute_uri()
    print(url)

    surl = url.split('?king=')
    king = surl[1].split('&queen=')[0]

    surl = surl[1].split('&queen=')[1]
    
    queen = surl.split('&rook=')[0]
    surl = url.split('&rook=')[1]
    rook = surl.split('&bishop=')[0]

    surl = url.split('&bishop=')[1]
    bishop = surl.split('&knight=')[0]

    surl = url.split('&knight=')[1]
    knight = surl.split('&pawn=')[0]


    surl = url.split('&pawn=')[1]
    pawn = surl.split('&from=')[0]




    print(king)
    print(queen)
    print(rook)
    print(bishop)
    print(knight)
    print(pawn)

    surl = url.split('&from=')
    _from = surl[1][0]+surl[1][1]
    surl = url.split('&to=')
    _to = surl[1][0]+surl[1][1]
    

    sub = url.split('&fen=')
    subS = sub[1]
    fen = subS.split("%2F")
    finalFen = ""
    for f in fen:
        finalFen+=f+"/"
        
    finalFen = finalFen.rstrip(finalFen[-1])
    ff=finalFen
    ff +=' w KQkq - 0 1'
    fff=finalFen
    fff +=' b KQkq - 0 1'



    print('from:',_from)
    print('to:',_to)
    print('fen ===========', finalFen)

    p = { 'P': int(pawn), 'N': int(knight), 'B': int(bishop), 'R': int(rook), 'Q': int(queen), 'K': int(king) }


    
    pos = tools.parseFEN(ff)
    
    sunfish.print_pos(pos)
    
    f = sunfish.getMove(pos[0],_from,_to,p)

    # Load current state
    data = load_moves()

    # Parse the board to check for captures
    board_before = parse_fen_to_board(finalFen)

    # Convert chess notation (e2, e4) to x,y coordinates
    from_x = ord(_from[0]) - ord('a')
    from_y = int(_from[1]) - 1
    to_x = ord(_to[0]) - ord('a')
    to_y = int(_to[1]) - 1

    # Check if player captured a piece (was there a piece at destination?)
    dest_row = 7 - to_y  # flip for board array indexing
    player_captured = board_before[dest_row][to_x]
    if player_captured == '.':
        player_captured = None

    # Record player's move (white)
    player_move = {
        'from': [from_x, from_y],
        'to': [to_x, to_y],
        'capture': player_captured,
        'color': 'white'
    }
    data['moves'].append(player_move)

    # Check for player castling (king moved 2 squares)
    piece_moved = board_before[7 - from_y][from_x]
    if piece_moved == 'K' and abs(to_x - from_x) == 2:
        # Castling! Add rook move
        if to_x > from_x:  # Kingside
            rook_move = {'from': [7, 0], 'to': [5, 0], 'capture': None, 'color': 'white'}
        else:  # Queenside
            rook_move = {'from': [0, 0], 'to': [3, 0], 'capture': None, 'color': 'white'}
        data['moves'].append(rook_move)

    # Build intermediate board (after player move, before AI)
    board_after_player = [row[:] for row in board_before]  # copy
    board_after_player[7 - from_y][from_x] = '.'
    board_after_player[7 - to_y][to_x] = piece_moved

    # Handle castling rook in intermediate board
    if piece_moved == 'K' and abs(to_x - from_x) == 2:
        if to_x > from_x:  # Kingside
            board_after_player[7][7] = '.'
            board_after_player[7][5] = 'R'
        else:  # Queenside
            board_after_player[7][0] = '.'
            board_after_player[7][3] = 'R'

    # Now find AI's move(s) by comparing intermediate to final (black)
    ai_moves = find_moves_from_boards(board_after_player, parse_fen_to_board(f), 'black')
    for ai_move in ai_moves:
        data['moves'].append(ai_move)

    save_moves(data)

    return JsonResponse({'asdf': f})
 























