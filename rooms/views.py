from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


class RoomDetail(DetailView):

    """Roomdetail Definition"""

    model = models.Room
    pk_url_kwarg = "pk"  # defalut = "pk"


def search(request):
    city = request.GET.get(
        "city", "Anywhere"
    )  # capitalize는 str을 필요로하기 때문에 defalut를 지정해주어야함
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))  # int의 경우 defalut=0 을 정의
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = request.GET.get("instant", False)
    superhost = request.GET.get("superhost", False)
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    form = {
        "city": city,
        "s_country": country,
        "s_room_type": room_type,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "superhost": superhost,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    # 필터링
    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city
    filter_args["country"] = country
    if city != 0:
        filter_args["room_type__pk"] = room_type
    # if price != 0:
    #     filter_args["price__lte"] = price
    # if guests != 0:
    #     filter_args["guests__gte"] = guests
    # if bedrooms != 0:
    #     filter_args["bedrooms__gte"] = bedrooms
    # if beds != 0:
    #     filter_args["beds__gte"] = beds
    # if baths != 0:
    #     filter_args["baths__gte"] = baths
    # if instant is True:
    #     filter_args["instant_book"] = True
    # if superhost is True:
    #     filter_args["host__superhost"] = True  # ForeignKey를 활용한 필터링이 가능함
    rooms = models.Room.objects.filter(**filter_args)
    return render(request, "rooms/search.html", {**form, **choices, "rooms": rooms})
