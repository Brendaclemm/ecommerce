from .models import Category


def store_context(request):
    categories = Category.objects.all()

    return {"categories": categories}

