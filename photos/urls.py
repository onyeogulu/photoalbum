from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('photo/<str:pk>/', views.viewPhoto, name='photo'), 
    path('add/', views.addPhoto, name='add'),
    path("photo-delete/<int:pk>/", views.deletePhoto.as_view(), name='photo-delete'), 
]
