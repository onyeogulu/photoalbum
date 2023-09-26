from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('', views.gallery, name='gallery'),
    path('photo/<str:pk>/', views.viewPhoto, name='photo'), 
    path('add/', views.addPhoto, name='add'),
    path("photo-delete/<int:pk>/", views.deletePhoto.as_view(), name='photo-delete'), 
]
