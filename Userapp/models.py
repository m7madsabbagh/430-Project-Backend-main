from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    username = models.CharField(primary_key = True,max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    Firstname = models.CharField(max_length=60)
    Lastname = models.CharField(max_length=60)
    Age = models.IntegerField()
    Team = models.CharField(max_length=60)
    Position = models.CharField(max_length=60)
    Height = models.IntegerField()
    Weight = models.IntegerField()
    College = models.CharField(max_length=60)
    AccountBalance = models.IntegerField(default= 0)

class Referee(models.Model):
    username = models.CharField(primary_key=True, max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    Firstname = models.CharField(max_length=60)
    Lastname = models.CharField(max_length=60)

class Teams(models.Model):
    TeamName = models.CharField(primary_key = True,max_length=60)
    TeamManagerUserName = models.CharField(max_length=60)
    TeamManagerEmail = models.CharField(max_length=60)
    TeamManagerPassword = models.CharField(max_length=60)
    TeamManagerFirstname = models.CharField(max_length=60)
    TeamManagerLastname = models.CharField(max_length=60)
    Country = models.CharField(max_length=60)
    GamesWon = models.IntegerField()
    GamesLost = models.IntegerField()

class TournamentOrganizer(models.Model):
    username = models.CharField(primary_key=True, max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    Firstname = models.CharField(max_length=60)
    Lastname = models.CharField(max_length=60)

class Games(models.Model):
    id = models.AutoField(primary_key=True)
    Team1 = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='games_team1')
    Team2 = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='games_team2')
    GameDate = models.DateTimeField(default=timezone.now)
    Referee = models.ForeignKey(Referee, on_delete=models.CASCADE)

#We assume no tournaments are being made with more than 16 players
class Tournament(models.Model):
    Organizer = models.ForeignKey(TournamentOrganizer, on_delete = models.CASCADE)
    CurrentStage = models.IntegerField()
    Name = models.CharField(max_length=60)
    Skill_Level = models.IntegerField()
    TournamentSize = models.IntegerField()


class Event(models.Model):
    EventName = models.CharField(max_length = 300, default="TeamEvent")
    EventType = models.CharField(max_length = 60)
    Team = models.ForeignKey(Teams, on_delete = models.CASCADE)
    EventStart = models.DateTimeField(default = timezone.now())
    EventEnd = models.DateTimeField()
    EventParticipants = models.CharField(max_length = 500)
    EventOrganizer = models.CharField(max_length = 200)


class PlayerGame(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    game_number = models.ForeignKey(Games, on_delete=models.CASCADE)
    points = models.IntegerField()
    assists = models.IntegerField()
    rebounds = models.IntegerField()
    steals = models.IntegerField()
    blocks = models.IntegerField()


class TournamentStage1(models.Model):
    Tournament = models.ForeignKey(Tournament, on_delete = models.CASCADE)
    Game1 = models.ForeignKey(Games, on_delete = models.CASCADE, related_name = 'ts1_games_team1')
    Game2 = models.ForeignKey(Games, on_delete = models.CASCADE, related_name = 'ts1_games_team2')

class TournamentStage2(models.Model):
    Tournament = models.ForeignKey(Tournament, on_delete = models.CASCADE)
    Game1 = models.ForeignKey(Games, on_delete = models.CASCADE, related_name = 'ts2_games_team1')
    Game2 = models.ForeignKey(Games, on_delete = models.CASCADE, related_name = 'ts2_games_team2')

class TournamentStage3(models.Model):
    Tournament = models.ForeignKey(Tournament, on_delete = models.CASCADE)
    Game1 = models.ForeignKey(Games, on_delete = models.CASCADE, related_name = 'ts3_games_team1')
    Game2 = models.ForeignKey(Games, on_delete = models.CASCADE, related_name = 'ts3_games_team2')
    Game3 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts3_games_team3')
    Game4 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts3_games_team4')

class TournamentStage4(models.Model):
    Tournament = models.ForeignKey(Tournament, on_delete = models.CASCADE)
    Game1 = models.ForeignKey(Games, on_delete = models.CASCADE, related_name = 'ts4_games_team1')
    Game2 = models.ForeignKey(Games, on_delete = models.CASCADE, related_name = 'ts4_games_team2')
    Game3 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts4_games_team3')
    Game4 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts4_games_team4')
    Game5 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts4_games_team5')
    Game6 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts4_games_team6')
    Game7 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts4_games_team7')
    Game8 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts4_games_team8')

class TournamentStage5(models.Model):
    Tournament = models.ForeignKey(Tournament, on_delete = models.CASCADE)
    Game1 = models.ForeignKey(Games, on_delete = models.CASCADE, related_name = 'ts5_games_team1')
    Game2 = models.ForeignKey(Games, on_delete = models.CASCADE, related_name = 'ts5_games_team2')
    Game3 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts5_games_team3')
    Game4 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts5_games_team4')
    Game5 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts5_games_team5')
    Game6 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts5_games_team6')
    Game7 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts5_games_team7')
    Game8 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts5_games_team8')
    Game9 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts5_games_team9')
    Game10 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts5_games_team10')
    Game11 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts5_games_team11')
    Game12 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts5_games_team12')
    Game13 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts5_games_team13')
    Game14 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts5_games_team14')
    Game15 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts5_games_team15')
    Game16 = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='ts5_games_team16')

