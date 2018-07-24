from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main),
    url(r'^register$', views.register),
    url(r'^process_reg$', views.process_reg),
    url(r'^register/pick_class$', views.pick_class),
]