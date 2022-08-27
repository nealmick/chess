from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from . import sunfish
from . import tools

def index(request):
    return render(request,'chessBot/index.html')




def nextMoveSunFish(request):
    context = {}
    print('sunfish move!')
       
    url = request.build_absolute_uri()
    print(url)
    
    surl = url.split('?from=')
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


    pos = tools.parseFEN(ff)
    sunfish.print_pos(pos)
    f = sunfish.getMove(pos[0],_from,_to)
 

    return JsonResponse({'asdf': f})
 

