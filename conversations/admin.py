from django.contrib import admin
from . import models


@admin.register(models.Message)
class MeassageAdmin(admin.ModelAdmin):

    pass


@admin.register(models.Conversations)
class ConversationAdmin(admin.ModelAdmin):

    pass
