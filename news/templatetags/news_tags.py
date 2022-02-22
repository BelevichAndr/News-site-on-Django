from django import template

from news.models import Category

register = template.Library()


@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('news/templates_for_filter/list_categories.html')
def show_categories():
    categories = Category.objects.all()
    return {'categories': categories}
