from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DeleteView, CreateView, DetailView
from django.urls import reverse_lazy

from .forms import NewsForm, UserRegisterForm, UserLoginForm, CommentForm
from .models import News, Category, Comment


class HomeNews(ListView):
    model = News
    template_name = "news/index.html"
    context_object_name = "news"
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Главная страница"
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related("category")


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
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs["category_id"])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs["category_id"], is_published=True).select_related("category")


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     context = {'news': news,
#                'category': category}
#     return render(request, 'news/category.html', context=context)


# class ViewNews(DetailView):
#     model = News
#     pk_url_kwarg = "news_id"
#     template_name = "news/view_news.html"
#     context_object_name = "news_item"


def view_news(request, news_id):
    # news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    comments = Comment.objects.filter(news=news_id)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news_item
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                  "news/view_news.html",
                  {'news_item': news_item,
                   'comments': comments,
                   'comment_form': comment_form})


class CreateNews(CreateView):
    form_class = NewsForm
    template_name = "news/add_news.html"
    success_url = reverse_lazy("home")


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            result = False
            form = UserRegisterForm()
            context = {"form": form,
                       "result":result}
            return render(request, "news/register.html", context=context)
    else:
        form = UserRegisterForm()
        context = {"form": form}
        return render(request, "news/register.html", context=context)


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        # form = UserLoginForm(request.POST)
        # if form.is_valid():
        #     user = form.get_user()
        #     login(request, user)
            return redirect("home")
        else:
            result = False
            form = UserLoginForm()
            context = {"form": form,
                       "result": result}
            return render(request, "news/login.html", context=context)
    else:
        form = UserLoginForm()
        context = {"form": form}
        return render(request, "news/login.html", context=context)


def user_logout(request):
    logout(request)
    return redirect("login")

# def add_news(request):
#     if request.method == "POST":
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # current_news = News.objects.create(**form.cleaned_data)
#             current_news = form.save()
#             return redirect(current_news)
#         return HttpResponse("нет валидации")
#     else:
#         form = NewsForm()
#         context = {
#             "form": form
#         }
#         return render(request, "news/add_news.html", context=context)
