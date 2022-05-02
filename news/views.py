from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DeleteView, CreateView
from django.urls import reverse_lazy

from .forms import NewsForm
from .models import News, Category


class HomeNews(ListView):
    model = News
    template_name = "news/index.html"
    context_object_name = "news"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Главная страница"
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)


# def index(request):
#     news = News.objects.all()
#     context = {'news': news,
#                'title': 'Список новостей',}
#     return render(request, 'news/index.html', context=context)


class CategoryNews(ListView):
    model = News
    template_name = "news/category.html"
    context_object_name = "news"
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs["category_id"])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs["category_id"], is_published=True)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     context = {'news': news,
#                'category': category}
#     return render(request, 'news/category.html', context=context)


class ViewNews(DeleteView):
    model = News
    pk_url_kwarg = "news_id"
    template_name = "news/view_news.html"
    context_object_name = "news_item"


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, "news/view_news.html", context={'news_item': news_item})

class CreateNews(CreateView):
    form_class = NewsForm
    template_name = "news/add_news.html"
    success_url = reverse_lazy("home")



def add_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            # current_news = News.objects.create(**form.cleaned_data)
            current_news = form.save()
            return redirect(current_news)
        return HttpResponse("нет валидации")
    else:
        form = NewsForm()
        context = {
            "form": form
        }
        return render(request, "news/add_news.html", context=context)
