import random
import string

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from mail import forms, models

menu = [
    {"title": "Список проифлей", "url_name": "home"},
    {"title": "Чаты", "url_name": "chats"},
    {"title": "Аккаунт", "url_name": "account"},
    {"title": "О сайте", "url_name": "about"},
]


class ProfileList(LoginRequiredMixin, generic.ListView):
    paginate_by = 5
    model = models.Profile
    template_name = "mail/profile_list.html"
    context_object_name = "profiles"
    login_url = reverse_lazy("login")

    def get_queryset(self):
        user = self.request.user
        p_list = models.User.objects.get(username=user)
        p_list = p_list.users.filter(hidden=0)
        return p_list

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data()
        ctx["title"] = "Список профилей"
        user = self.request.user
        if len(user.users.all()) >= 1:
            ctx["menu"] = menu
        try:
            a = self.request.GET["a"]
            ctx["error"] = "Такого пользователся не найдено"
        except KeyError:
            pass
        return ctx


class ProfileCreate(LoginRequiredMixin, generic.CreateView):
    form_class = forms.CreateProfileForm
    template_name = "mail/profile_create.html"
    success_url = reverse_lazy("home")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        user = models.User.objects.get(username=self.request.user)
        instance = form.save(commit=False)
        instance.save()
        prof = models.Profile.objects.get(id=form.instance.pk)
        prof.user.add(user)
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data()
        ctx["title"] = "Создать профиль"
        user = self.request.user
        if len(user.users.all()) >= 1:
            ctx["menu"] = menu
        return ctx


class ProfileDetail(LoginRequiredMixin, generic.DetailView):
    model = models.Profile
    template_name = "mail/profile_detail.html"
    context_object_name = "profile"
    slug_url_kwarg = "profile_slug"
    login_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data()
        ctx["title"] = "Список профилей"
        ctx["menu"] = menu

        active_user = self.request.user
        this_profile = self.object
        owner_of_profile = self.object.user.all()
        act_profile = models.User.objects.get(username=active_user)
        act_profile = act_profile.users.get(is_active=1)
        all_request_from_me = active_user.users.get(is_active=1).request_to_friend.all()
        my_friends = (act_profile.friend.all() | act_profile.friend.all()).distinct()

        if active_user in owner_of_profile:
            fr = (
                (self.object.friend.all() | self.object.friends.all())
                .filter(hidden=0)
                .distinct()
            )
            ctx["friends"] = fr
            ctx["status"] = "Мой профиль"
        else:
            ctx["status"] = "another_account"

        if self.object.slug in str(all_request_from_me.values()):
            ctx["status1"] = "account_already_asked"

        if this_profile in my_friends:
            ctx["friend"] = True
        return ctx


class ProfileUpdate(LoginRequiredMixin, generic.UpdateView):
    model = models.Profile
    form_class = forms.CreateProfileForm
    template_name = "mail/profile_update.html"
    context_object_name = "profile"
    slug_url_kwarg = "profile_slug"
    login_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data()
        ctx["title"] = "Список профилей"
        ctx["menu"] = menu
        return ctx


class ChatList(LoginRequiredMixin, generic.ListView):
    paginate_by = 20
    model = models.Chat
    template_name = "mail/chat_list.html"
    context_object_name = "chats"
    login_url = reverse_lazy("login")

    def get_queryset(self):

        act_profile = models.User.objects.get(username=self.request.user)
        act_profile = act_profile.users.get(is_active=1)
        ch_list = models.Profile.objects.get(slug=act_profile.slug)
        ch_list = ch_list.profiles.filter(hidden=0)

        return ch_list

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data()
        ctx["title"] = "Чаты"
        ctx["menu"] = menu
        return ctx


class ChatLog(LoginRequiredMixin, generic.DetailView):
    model = models.Chat
    template_name = "mail/chat_log.html"
    context_object_name = "messages"
    slug_url_kwarg = "chat_slug"
    login_url = reverse_lazy("login")

    def get_object(self, queryset=None):
        chat_id = super().get_object().id
        messages = models.Message.objects.filter(chat_id=chat_id)

        return messages.order_by("-send_time")

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data()
        ctx["title"] = "Чат"
        ctx["menu"] = menu
        ctx["form"] = forms.MessageForm
        ctx["chat"] = super().get_object().slug
        return ctx


def to_chat(request, profile_slug):
    active_user = request.user
    act_profile = models.User.objects.get(username=active_user)
    act_profile = act_profile.users.get(is_active=1)
    friend = models.Profile.objects.get(slug=profile_slug)

    my_chats = act_profile.profiles.filter(hidden=0)
    friend_chats = friend.profiles.filter(hidden=0)

    chat = my_chats & friend_chats

    if chat:
        slug = chat[0].slug
        return redirect("/chat/{}".format(slug))

    def generate_random_string(length):
        letters = string.ascii_lowercase
        rand_string = "".join(random.choice(letters) for i in range(length))
        return rand_string

    slug = generate_random_string(10)
    new_chat = models.Chat(
        chat_name="{} и {}".format(act_profile, friend), slug=slug, hidden=0
    )
    new_chat.save()
    new_chat.profile.add(act_profile, friend)

    return redirect("/chat/{}".format(slug))


class AccountDetail(LoginRequiredMixin, generic.View):
    template_name = "mail/account_detail.html"
    login_url = reverse_lazy("login")

    def get(self, request):
        return self.render_template()

    def render_template(self) -> HttpResponse:
        user = self.request.user
        user = models.User.objects.get(username=user)
        ctx = {"account": user}
        ctx["title"] = "аккаунт"
        ctx["menu"] = menu

        return render(self.request, "mail/account_detail.html", ctx)


class AccountUpdate(LoginRequiredMixin, generic.FormView):
    # form_class = forms.CreateProfileForm
    model = models.User
    success_url = "/profile/"
    template_name = "mail/account_update.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data()
        ctx["title"] = "Список профилей"
        ctx["menu"] = menu
        return ctx


class RequestList(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy("login")

    def get(self, request):
        return self.render_template()

    def render_template(self) -> HttpResponse:
        active_user = self.request.user
        all_request_to_me = active_user.users.get(is_active=1).requests.all()
        all_request_from_me = active_user.users.get(is_active=1).request_to_friend.all()

        ctx = {}
        ctx["title"] = "Заявки в друзья"
        ctx["menu"] = menu
        ctx["incoming"] = all_request_to_me
        ctx["outgoing"] = all_request_from_me

        return render(self.request, "mail/requests.html", ctx)


@login_required
def about(request):
    context = {}
    context["title"] = "Список профилей"
    context["menu"] = menu
    return render(request, template_name="mail/about.html", context=context)


@login_required
def active_profile(request):
    id = request.GET["id"]
    p_list = models.User.objects.get(username=request.user)
    p_list = p_list.users.all()
    active = p_list.get(id=id)
    not_active = p_list.exclude(id=id)

    active.is_active = 1
    active.save()

    for n in not_active:
        n.is_active = 0
        n.save()

    return redirect("home")


def search(request):
    search_word = request.POST["search"]

    if len(models.Profile.objects.filter(slug=search_word, hidden=0)) == 1:
        path = "/profile/detail/{}/".format(search_word)
        return redirect(path)
    else:
        return redirect("/?a=1")


def accept_request(request, profile_slug):
    active_user = request.user
    act_profile = models.User.objects.get(username=active_user)
    act_profile = act_profile.users.get(is_active=1)
    friend = models.Profile.objects.get(slug=profile_slug)
    act_profile.friend.add(friend)

    act_profile.requests.remove(friend)
    return redirect("home")


def cancel_request(request, profile_slug):
    active_user = request.user
    act_profile = models.User.objects.get(username=active_user)
    act_profile = act_profile.users.get(is_active=1)
    not_friend = models.Profile.objects.get(slug=profile_slug)

    act_profile.request_to_friend.remove(not_friend)
    return redirect("home")


def send_request(request, profile_slug):
    active_user = request.user
    act_profile = models.User.objects.get(username=active_user)
    act_profile = act_profile.users.get(is_active=1)
    future_friend = models.Profile.objects.get(slug=profile_slug)
    act_profile.friend.add(future_friend)

    act_profile.request_to_friend.add(future_friend)
    return redirect("home")


@login_required
def delete(request, profile_slug):
    active_user = request.user
    delete_profile = active_user.users.get(slug=profile_slug)
    delete_profile.hidden = 1
    delete_profile.save()
    return redirect("home")


@login_required
def message_send(request):
    active_user = request.user
    act_profile = models.User.objects.get(username=active_user)
    act_profile = act_profile.users.get(is_active=1)
    if request.method == "POST":
        form = forms.MessageForm(request.POST, request.FILES)
        slug = request.POST["chat"]
        chat = models.Chat.objects.get(slug=slug)
        text = request.POST["text"]

        try:
            attached_file = request.FILES["attached_file"]
        except KeyError:
            attached_file = ""

        try:
            attached_photo = request.FILES["attached_photo"]
        except KeyError:
            attached_photo = ""

        message = models.Message(
            text=text,
            sender=act_profile,
            chat=chat,
            attached_photo=attached_photo,
            attached_file=attached_file,
        )
        message.save()

    return redirect("/chat/{}/".format(slug))


class RegisterUser(generic.CreateView):
    form_class = UserCreationForm
    template_name = "mail/register.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data()
        ctx["title"] = "Регистрация"
        ctx["menu"] = menu
        return ctx

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = "mail/login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data()
        ctx["title"] = "Войти"
        ctx["menu"] = menu
        return ctx

    def get_success_url(self):
        return reverse_lazy("home")


def logout_user(request):
    logout(request)
    return redirect("login")
