from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status

from Userapp.models import User,Games
from Userapp.serializers import *
import jwt
import datetime
from datetime import timedelta
# Create your views here.

SECRET_KEY = "b'|\xe7\xbfU3`\xc4\xec\xa7\xa9zf:}\xb5\xc7\xb9\x139^3@Dv'"
from rest_framework_simplejwt.tokens import RefreshToken

def create_token(username):
    payload = {
        'exp': timezone.now() +timedelta(days=4),
        'iat': timezone.now(),
        'sub': username
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )

def extract_auth_token(authenticated_request):
    auth_header = authenticated_request.headers.get('Authorization')
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return None


def decode_token_user(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        username = payload['sub']
        user = User.objects.get(username=username)
        return user
    except (jwt.exceptions.DecodeError, User.DoesNotExist):
        return None

def decode_token_team(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        username = payload['sub']
        team = Teams.objects.get(TeamManagerUserName=username)
        return team
    except (jwt.exceptions.DecodeError, User.DoesNotExist):
        return None


def authenticate_user(request):
    token = extract_auth_token(request)
    if not token:
        return None, "You are not authenticated"
    user = decode_token_user(token) or decode_token_team(token)
    if not user:
        return None, "You are not authenticated"
    return user, None


@api_view(['POST'])
@csrf_exempt
def login(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.get(username = username)
        if user.password != password:
            return Response({'error': 'Wrong Password'})
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'})

    token = create_token(username)
    return Response({'access_token': token})


@api_view(['POST'])
@csrf_exempt
def login_team(request):
    try:
        username = request.data.get('TeamManagerusername')
        password = request.data.get('TeamManagerpassword')
        team = Teams.objects.get(TeamManagerUserName=username)
        if team.TeamManagerPassword != password:
            return Response({'error': 'Wrong Password'})
    except Teams.DoesNotExist:
        return Response({'error': 'Invalid team credentials'}, status=400)

    token = create_token(username)
    return Response({'access_token': token})


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@csrf_exempt
def UserApi(request, username = 0):
    if request.method == 'GET':
        users = User.objects.all()
        users_serializer= UserSerializer(users,many = True)
        return JsonResponse(users_serializer.data,safe = False)
    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        users_serializer = UserSerializer(data =user_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse(users_serializer.data, status=201)
        return JsonResponse(users_serializer.errors, status=400)
    elif request.method == 'PUT':
        user, error = authenticate_user(request)
        if error:
            return Response(error, 400)
        user_data = JSONParser().parse(request)
        user = User.objects.get(username = user_data['username'])
        users_serializer = UserSerializer(user,data =user_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse("Updated Successfully", safe = False,)
        return JsonResponse("Failed to Update", safe = False)
    elif request.method == 'DELETE':
        user = User.objects.get(username=username)
        if user.AccountBalance <0 :
            return JsonResponse("Player has an outstanding balance, cannot delete", 403)
        user.delete()
        return JsonResponse("Deleted Successfully", safe = False)


@api_view(['DELETE'])
@csrf_exempt
def delete_player(request,username):
    user = User.objects.get(username=username)
    if user.AccountBalance < 0:
        return JsonResponse("Player has an outstanding balance, cannot delete", 403)
    user.delete()
    return JsonResponse("Deleted Successfully", safe=False)



@api_view(['PUT'])
@csrf_exempt
def pay_user(request):
    user, error = authenticate_user(request)
    if error:
        return Response("Bad Request", 400)
    funds = request.data.get("AddFunds")
    if user.AccountBalance is not None:
        user.AccountBalance = user.AccountBalance + funds
    else:
        user.AccountBalance = funds
    user_data = {'AccountBalance': user.AccountBalance}
    user_serializer = UserSerializer(user, data = user_data, partial = True)
    print(user)
    if user_serializer.is_valid():
        user_serializer.save()
        return JsonResponse("Funds added Successfully", safe=False)
    return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)




@api_view(['PUT'])
@csrf_exempt
def coach_pay(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response("Player does not exist", status = 404)
    payment_amount = request.data.get("PaymentAmount")
    if user.AccountBalance is not None:
        user.AccountBalance = user.AccountBalance - payment_amount
    else:
        user.AccountBalance = -payment_amount
    user_data = {'AccountBalance': user.AccountBalance}
    user_serializer = UserSerializer(user, data=user_data, partial=True)
    if user_serializer.is_valid():
        user_serializer.save()
        return Response("Funds have been withdrawn")
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)








@api_view(['GET','DELETE'])
@csrf_exempt
def get_user_by_username_or_delete(request, username):
    if request.method == 'GET':
        print("Getting user by username:", username)
        user = get_object_or_404(User, username=username)
        user_serializer = UserSerializer(user)
        return JsonResponse(user_serializer.data)
    elif request.method == 'DELETE':
        user = User.objects.get(username=username)
        if user.AccountBalance < 0:
            return JsonResponse("Player has an outstanding balance, cannot delete", status =403, safe = False)
        user.delete()
        return JsonResponse("Deleted Successfully", safe=False)


@api_view(['GET'])
@csrf_exempt
def get_players_usernames(request):
    users = User.objects.all()
    usernames = [user.username for user in users]
    return Response(usernames, status=200)



@api_view(['GET'])
def get_my_user(request):
    user, error = authenticate_user(request)
    if error:
        return Response("Bad Request",400)
    user_serialized = UserSerializer(user)
    return Response(user_serialized.data,200)

@api_view(['GET'])
def get_user_team(request):
    user, error = authenticate_user(request)
    if error:
        return Response("Bad Request (Credentials)",400)
    try:
        team = Teams.objects.get(TeamName = user.Team)
    except Teams.DoesNotExist:
        return Response("Team not found", status=status.HTTP_404_NOT_FOUND)
    team_serialized = TeamsSerializer(team)
    data = {
    'TeamName': team_serialized.data['TeamName'],
    'Country': team_serialized.data['Country'],
    'GamesWon': team_serialized.data['GamesWon'],
    'GamesLost': team_serialized.data['GamesLost']
    }
    return Response(data, status =200)


@api_view(['GET'])
def get_teammates_usernames(request):
    user, error = authenticate_user(request)
    if error:
        return Response("Invalid Credentials", 400)
    try:
        users = User.objects.filter(Team = user.Team)
    except User.DoesNotExist:
        return Response("No Teammates found", status = 404)
    usernames = [user.username for user in users]
    return Response(usernames, status = 200)


@api_view(['GET'])
def get_teammates_usernames_team(request):
    team, error = authenticate_user(request)
    if error:
        return Response("Invalid Team Credentials", 400)
    try:
        users = User.objects.filter(Team = team.TeamName)
    except User.DoesNotExist:
        return Response("No Teammates found", status = 404)
    usernames = [user.username for user in users]
    return Response(usernames, status = 200)


@api_view(['GET'])
def get_my_team(request):
    user, error = authenticate_user(request)
    if error:
        return Response("Bad Request",400)
    user_serialized = TeamsSerializer(user)
    return Response(user_serialized.data,200)


@csrf_exempt
def GameApi(request, id =0):
    if request.method == 'GET':
        games = Games.objects.all()
        game_ids = [game.id for game in games]
        return JsonResponse(game_ids,status= 200, safe = False)

    elif request.method == 'POST':
        games_data = JSONParser().parse(request)
        games_serializer = GamesSerializer(data =games_data)
        if games_serializer.is_valid():
            games_serializer.save()
            return JsonResponse(games_serializer.data, status=201)
        return JsonResponse(games_serializer.errors, status=400)

    elif request.method == 'DELETE':
        games = Games.objects.get(id=id)
        games.delete()
        return JsonResponse("Deleted Successfully", safe = False)


@csrf_exempt
@csrf_exempt
def TeamApi(request, TeamName=0):
    if request.method == 'GET':
        teams = Teams.objects.all()
        teams_serializer = TeamsSerializer(teams, many=True)
        return JsonResponse(teams_serializer.data, safe=False)
    elif request.method == 'POST':
        teams_data = JSONParser().parse(request)
        teams_serializer = TeamsSerializer(data=teams_data)
        if teams_serializer.is_valid():
            teams_serializer.save()
            return JsonResponse(teams_serializer.data, status=201)
        return JsonResponse(teams_serializer.errors, status=400)

    elif request.method == 'DELETE':
        user, error = authenticate_user(request)
        if error:
            return Response("Invalid Authentication", 400)
        teams = Teams.objects.get(TeamName=TeamName)
        teams.delete()
        return JsonResponse("Deleted Successfully", safe = False)


@api_view(['PUT'])
@csrf_exempt
def UpdateTeam(request, team_name):
   # user, error = authenticate_user(request)
   # if error:
   #     return Response("Invalid Authentication", status=status.HTTP_400_BAD_REQUEST)
    try:
        team = Teams.objects.get(TeamName= team_name)
    except Teams.DoesNotExist:
        return Response("Team not found", status=status.HTTP_404_NOT_FOUND)
    teams_serializer = TeamsSerializer(team, data=request.data, partial=True)
    if teams_serializer.is_valid():
        teams_serializer.save()
        return JsonResponse("Updated Successfully", safe=False)
    return JsonResponse(teams_serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(['GET'])
def get_team_by_team_name(request, team_name):
    print("Getting user by username:", team_name)
    team = get_object_or_404(Teams, TeamName=team_name)
    team_serializer = TeamsSerializer(team)
    return JsonResponse(team_serializer.data)



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@csrf_exempt
def EventApi(request, EventName = 0):
    if request.method == 'GET':
        events = Event.objects.all()
        events_serializer= EventSerializer(events,many = True)
        return JsonResponse(events_serializer.data,safe = False)
    elif request.method == 'POST':
        event_data = JSONParser().parse(request)
        events_serializer = EventSerializer(data =event_data)
        if events_serializer.is_valid():
            events_serializer.save()
            return JsonResponse(events_serializer.data, status=201)
        return JsonResponse(events_serializer.errors, status=400)


@api_view(['DELETE'])
def delete_event(request, EventID):
    user, error = authenticate_user(request)
    if error:
        return Response("Invalid Credentials", status = 403)
    try:
        event = Event.objects.get(id = EventID)
    except Event.DoesNotExist:
        return Response("This event does not exist", status = 404)
    event.delete()
    return Response("Event deleted successfully", status = 200)


@api_view(['GET'])
def get_team_event(request):
    team , error = authenticate_user(request)
    if not team :
        return JsonResponse("Invalid Credentials", safe = False, status=400)
    events = Event.objects.filter(Team = team.TeamName)
    events_serializer = EventSerializer(events, many = True)
    return JsonResponse(events_serializer.data, status = 200 , safe = False)

@api_view(['GET'])
def get_team_event_player(request):
    user , error = authenticate_user(request)
    if not user :
        return JsonResponse("Invalid Credentials", safe = False, status=400)
    events = Event.objects.filter(Team = user.Team)
    events_serializer = EventSerializer(events, many = True)
    return JsonResponse(events_serializer.data, status = 200 , safe = False)



@api_view(['POST'])
@csrf_exempt
def PlayerGameApi(request, username = 0):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        playergame_serializer = PlayerGameSerializer(data =data)
        if playergame_serializer.is_valid():
            playergame_serializer.save()
            return JsonResponse(playergame_serializer.data, status=201)
        return JsonResponse(playergame_serializer.errors, status=400)



@api_view(['GET'])
def GetPlayerGames(request,username):
    games = PlayerGame.objects.filter(player=username)
    print(games)
    playergame_serializer = PlayerGameSerializer(games, many=True)
    return JsonResponse(playergame_serializer.data, status=200, safe=False)

@api_view(['GET'])
def GetMyGames(request):
    user, error = authenticate_user(request)
    if error:
        return Response("Bad Request", 400)
    games = PlayerGame.objects.filter(player = user.username)
    games_serialized = PlayerGameSerializer(games, many= True)
    return Response(games_serialized.data, 200)





@csrf_exempt
@csrf_exempt
def RefApi(request, username=0):
    if request.method == 'GET':
        referee = Referee.objects.all()
        referee_serializer = RefereeSerializer(referee, many=True)
        return JsonResponse(referee_serializer.data, safe=False)
    elif request.method == 'POST':
        referee_data = JSONParser().parse(request)
        referee_serializer = RefereeSerializer(data=referee_data)
        if referee_serializer.is_valid():
            referee_serializer.save()
            return JsonResponse(referee_serializer.data, status=201)
        return JsonResponse(referee_serializer.errors, status=400)
    elif request.method == 'PUT':
        referee_data = JSONParser().parse(request)
        referee = Referee.objects.get(username=referee_data['username'])
        referee_serializer = RefereeSerializer(referee, data=referee_data)
        if referee_serializer.is_valid():
            referee_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif request.method == 'DELETE':
        referee = Referee.objects.get(username=username)
        referee.delete()
        return JsonResponse("Deleted Successfully", safe=False)














