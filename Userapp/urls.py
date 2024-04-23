from django.urls import re_path
from Userapp import views

urlpatterns = [
    re_path(r'^user$',views.UserApi),
    re_path(r'^user/(?P<username>\w+)$', views.get_user_by_username_or_delete),
    re_path(r'^user/me', views.get_my_user),
    re_path(r'^usernames', views.get_players_usernames),
    re_path(r'^games$',views.GameApi),
    re_path(r'^games/([0-9]+)$',views.GameApi),
    re_path(r'^login', views.login),
    re_path(r'^teamlogin', views.login_team),
    re_path(r'^teams/me', views.get_my_team),
    re_path(r'^teams/user', views.get_user_team),
    re_path(r'^getteamates/user', views.get_teammates_usernames),
    re_path(r'^getteamates/team', views.get_teammates_usernames_team),
    re_path(r'^teams$', views.TeamApi),
    re_path(r'^team/(?P<team_name>\w+)/$', views.get_team_by_team_name),
    re_path(r'^team/update/(?P<team_name>\w+)/$', views.UpdateTeam),
    re_path(r'^event',views.EventApi),
    re_path(r'^delete/event/(?P<EventID>\w+)$', views.delete_event),
    re_path(r'^teamevents', views.get_team_event),
    re_path(r'^myteamevents', views.get_team_event_player),
    re_path(r'^event/(?P<EventName>\w+)/$', views.EventApi),
    re_path(r'^stats', views.PlayerGameApi),
    re_path(r'^getstats/(?P<username>\w+)/$', views.GetPlayerGames),
    re_path(r'^getmystats',views.GetMyGames),
    re_path(r'^coachpay/(?P<username>\w+)$', views.coach_pay),
    re_path(r'^playerpay', views.pay_user)

]