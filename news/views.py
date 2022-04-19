from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewsForm
from .models import News, Category


def index(request):
    news = News.objects.all()
    context = {'news': news,
               'title': 'Список новостей',}
    return render(request, 'news/index.html', context=context)


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    context = {'news': news,
               'category': category}
    return render(request, 'news/category.html', context=context)


def view_news(request, news_id):
    # news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, "news/view_news.html", context={'news_item': news_item})


def add_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            # current_news = News.objects.create(**form.cleaned_data)
            current_news = form.save()
            return redirect(current_news)
    else:
        form = NewsForm()
        context = {
            "form": form
        }
        return render(request, "news/add_news.html", context=context)
