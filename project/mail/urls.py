from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.static import serve

from mail import views

from project import settings

urlpatterns = [
    path("", views.ProfileList.as_view(), name="home"),
    path("send/", views.message_send, name="send"),
    path("chats/", views.ChatList.as_view(), name="chats"),
    path("chat/<slug:chat_slug>/", views.ChatLog.as_view(), name="chat"),
    path("chat/to_chat/<slug:profile_slug>/", views.to_chat, name="to_chat"),
    path(
        "profile/detail/<slug:profile_slug>/",
        views.ProfileDetail.as_view(),
        name="profile",
    ),
    path("profile/create/", views.ProfileCreate.as_view(), name="profile_create"),
    path(
        "profile/update/<slug:profile_slug>/",
        views.ProfileUpdate.as_view(),
        name="profile_update",
    ),
    path("profile/delete/<slug:profile_slug>/", views.delete, name="profile_delete"),
    path("account/", views.AccountDetail.as_view(), name="account"),
    path("account/update/", views.AccountUpdate.as_view(), name="account_update"),
    path("login/", views.LoginUser.as_view(), name="login"),
    path("register/", views.RegisterUser.as_view(), name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("active/", views.active_profile, name="active"),
    path("about/", views.about, name="about"),
    path("search/", views.search, name="search"),
    path("request/", views.RequestList.as_view(), name="request"),
    path(
        "request/accept/<slug:profile_slug>/",
        views.accept_request,
        name="accept_request",
    ),
    path(
        "request/cancel/<slug:profile_slug>/",
        views.cancel_request,
        name="cancel_request",
    ),
    path("request/send/<slug:profile_slug>/", views.send_request, name="send_request"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),]
