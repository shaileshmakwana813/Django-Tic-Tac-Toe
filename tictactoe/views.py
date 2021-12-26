from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
from . import util

# Create your views here.

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def game_status(request):
    if request.method == "POST":
        matrix = json.loads(request.body).get('matrix')
        matrix = util.get_matrix(matrix)
        if util.terminal(matrix):
            return JsonResponse({"end": True, "winner": util.winner(matrix)})
        else:
            return JsonResponse({"end": False, "winner": None})

@csrf_exempt
def next_move(request):
    if request.method == "POST":
        matrix = json.loads(request.body).get('matrix')
        matrix = util.get_matrix(matrix)
        move = util.minimax(matrix)
        return JsonResponse({"row": move[0], "col": move[1]})