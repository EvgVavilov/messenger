from django.contrib import admin
from mail.models import Chat, Message, Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "last_name", "time_create", "is_active", "avatar")
    list_display_links = ("id", "name", "last_name", "avatar")
    search_fields = ("id", "name", "last_name")
    list_filter = ("id", "name", "time_create")
    prepopulated_fields = {
        "slug": (
            "name",
            "last_name",
        )
    }


class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "chat_name", "time_update")
    list_display_links = ("id", "chat_name")
    search_fields = ("id", "chat_name")
    list_filter = ("id", "chat_name", "time_update")


class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "text", "chat")
    list_display_links = ("id", "sender", "text")
    search_fields = ("id", "sender", "text ")
    list_filter = ("id", "sender", "text")


# @admin.register(Profile, ProfileAdmin, Chat, ChatAdmin, Message, MessageAdmin)
class MailModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
