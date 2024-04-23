from rest_framework import serializers
from Userapp.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'Firstname', 'Lastname', 'Age', 'Team', 'Position', 'Height', 'Weight', 'College', 'AccountBalance']


class RefereeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referee
        fields = ['username', 'email', 'password', 'Firstname', 'Lastname']


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ['TeamName', 'TeamManagerUserName', 'TeamManagerEmail', 'TeamManagerPassword', 'TeamManagerFirstname', 'TeamManagerLastname', 'Country', 'GamesWon', 'GamesLost']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','EventName','EventType', 'Team', 'EventStart', 'EventEnd', 'EventParticipants', 'EventOrganizer']


class TournamentOrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentOrganizer
        fields = ['username', 'email', 'password', 'Firstname', 'Lastname']


class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ['id', 'Team1', 'Team2', 'GameDate', 'Referee']

class PlayerGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerGame
        fields = ['player', 'game_number' , 'points' , 'assists' , 'rebounds', 'steals', 'blocks']


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['Organizer', 'CurrentStage', 'Name', 'Skill_Level', 'TournamentSize']


class TournamentStage1Serializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentStage1
        fields = ['Tournament', 'Game1', 'Game2']


class TournamentStage2Serializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentStage2
        fields = ['Tournament', 'Game1', 'Game2']


class TournamentStage3Serializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentStage3
        fields = ['Tournament', 'Game1', 'Game2', 'Game3', 'Game4']


class TournamentStage4Serializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentStage4
        fields = ['Tournament', 'Game1', 'Game2', 'Game3', 'Game4', 'Game5', 'Game6', 'Game7', 'Game8']


class TournamentStage5Serializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentStage5
        fields = ['Tournament', 'Game1', 'Game2', 'Game3', 'Game4', 'Game5', 'Game6', 'Game7', 'Game8', 'Game9', 'Game10', 'Game11', 'Game12', 'Game13', 'Game14', 'Game15', 'Game16']
