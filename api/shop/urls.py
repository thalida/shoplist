from django.urls import path
from . import views

app_name = "shop"
urlpatterns = [
    # ex: /
    path("", views.index, name="index"),
    # ex: /list/5/
    # path("list/<str:list_id>/", views.list_detail, name="list-detail"),
]
