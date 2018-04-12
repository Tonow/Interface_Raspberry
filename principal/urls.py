from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^accueil', views.home),
    url(r'^date', views.date_actuelle),
    url(r'^graph_lac', views.graph_lac),
    url(r'^graph_air', views.graph_air),
    url(r'^getimage', views.getimage),
]
