from django.shortcuts import render
import pickle
import os
# Create your views here.
from django.http import HttpResponse, JsonResponse
from . import sunfish

from . import tools

# File to store the latest FEN
FEN_STATE_FILE = os.path.join(os.path.dirname(__file__), 'latest_fen.txt')

def index(request):
    return render(request,'chessBot/index.html')


def getState(request):
    """Return the latest FEN string from the last game move."""
    try:
        with open(FEN_STATE_FILE, 'r') as f:
            fen = f.read().strip()
        return JsonResponse({'fen': fen})
    except FileNotFoundError:
        return JsonResponse({'fen': None, 'error': 'No game state yet'})




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

    # Save the latest FEN state
    with open(FEN_STATE_FILE, 'w') as file:
        file.write(f)

    return JsonResponse({'asdf': f})
 























