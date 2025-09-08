from .models import Category


def footer_categories(request):
    return {
        "footer_categories": Category.objects.filter(show_in_footer=True).order_by("name")
    }


