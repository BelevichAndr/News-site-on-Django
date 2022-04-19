from django import forms
from news.models import *


# class NewsForm(forms.Form):
#     title = forms.CharField(max_length=150, label="Заголовок", widget=forms.TextInput(
#         attrs={"class": "form-control",
#                }))
#     content = forms.CharField(label="Содержание", required=False, widget=forms.Textarea(
#         attrs={"class": "form-control",
#                "cols": 10,
#                "rows": 5}))
#     is_published = forms.BooleanField(label="Опубликовать?", initial=True)
#     category = forms.ModelChoiceField(empty_label="Не выбрано",
#                                       queryset=Category.objects.all(), label="Категория",
#                                       widget=forms.Select(
#                                           attrs={"class": "form-control",
#                                                  }))


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ("title", "content", "is_published", "category")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control",
                                             "rows": 5}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }
