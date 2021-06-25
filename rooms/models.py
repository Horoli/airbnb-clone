from django.db import models
from django.urls import reverse
from django.db.models.deletion import SET_NULL
from django_countries.fields import CountryField
from core import models as core_models


class AbstractItem(core_models.TimeStampedModel):

    """Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """RoomType Model Definition"""

    class Meta:
        verbose_name = "Room Type"
        ordering = ["created"]  # 정렬


class Amenity(AbstractItem):

    """Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """Facility Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):

    """Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()  # django-countries
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField(help_text="How many people will be staying?")
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )  # 1개 선택
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=SET_NULL, null=True
    )  # 1개 선택
    amenities = models.ManyToManyField(
        "Amenity", related_name="rooms", blank=True
    )  # 다중 선택
    facilities = models.ManyToManyField(
        "Facility", related_name="rooms", blank=True
    )  # 다중 선택
    house_rules = models.ManyToManyField(
        "HouseRule", related_name="rooms", blank=True
    )  # 다중 선택

    def __str__(self):
        return self.name

    # 앞글자 대문자로 저장
    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    # admin에서 detail로 연결
    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    # 전체 리뷰 평균
    def total_rationg(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews))
        return 0

    def first_photo(self):
        (photo,) = self.photos.all()[:1]
        return photo.file.url
