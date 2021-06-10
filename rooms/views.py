from datetime import datetime
from django.shortcuts import render
from . import models


def all_rooms(request):
    all_rooms = models.Room.objects.all()
    return render(
        request, "rooms/home.html", context={"rooms": all_rooms}
    )  # html 파일의 변수와 변수명이 같아야함
