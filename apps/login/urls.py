from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^process_login$', views.process_login),
    url(r'^register$', views.register),
    url(r'^process_reg$', views.process_reg),
    url(r'^register/pick_class$', views.pick_class),
    url(r'^process_pick$', views.process_pick),
    url(r'^main$', views.main),
    url(r'^main/search$', views.search),
    url(r'^main/add_friend$', views.add_friend),
    url(r'^display/(?P<id>\d+)$', views.display_player),
    url(r'^logout$', views.logout),
    url(r'^start_game', views.start_game),
    url(r'^game_sess/(?P<id>\d+)$', views.game_sess),
    url(r'^game_sess/attack$', views.attack),
    url(r'^game_sess/leave$', views.leave),
]