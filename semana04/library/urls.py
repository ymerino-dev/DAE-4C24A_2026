"""URL configuration for the library application."""

from django.urls import path

from library import views

app_name = 'library'

urlpatterns = [
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
]
