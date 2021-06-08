from django.contrib import admin
from . import models


@admin.register(models.Message)
class MeassageAdmin(admin.ModelAdmin):

    list_display = ("__str__", "created")


@admin.register(models.Conversation)
class ConversationsAdmin(admin.ModelAdmin):

    list_display = (
        "__str__",
        "count_message",
        "count_participants",
    )
