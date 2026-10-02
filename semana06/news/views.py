from django.shortcuts import render


def home(request):
    """Public home page of the news app."""
    return render(request, 'news/home.html')
