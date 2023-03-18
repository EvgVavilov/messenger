from django import forms
from mail import models


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = [
            "name",
            "last_name",
            "date_birth",
            "email",
            "contact_inform",
            "live_place",
            "avatar",
            "about_self",
            "slug",
        ]

        widgets = {
            "name": forms.TextInput(),
            "last_name": forms.TextInput(),
            "date_birth": forms.SelectDateWidget(),
            "about_self": forms.Textarea(),
            "email": forms.EmailInput(),
            "contact_inform": forms.TextInput(),
            "live_place": forms.TextInput(),
            "slug": forms.TextInput(),
        }


class SearchForm(forms.ModelForm):
    class Meta:
        fields = ["search"]
        widgets = {"search": forms.TextInput()}


class MessageForm(forms.ModelForm):
    class Meta:
        model = models.Message
        fields = ["text", "attached_photo", "attached_file"]
        widgets = {
            "text": forms.Textarea(attrs={"cols": 70, "rows": 2}),
        }
