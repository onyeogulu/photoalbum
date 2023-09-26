from django.shortcuts import render, redirect
from .models import Category, Photo
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.generic import (
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomeUserCreationForm

def loginUser(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request,username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('gallery')
            
    return render(request, 'photos/login_register.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerUser(request):
    form = CustomeUserCreationForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
        user = authenticate(request,username=user.username, password=request.POST['password1'])
        
        if user is not None:
            login(request, user)
            return redirect('gallery')
    
    context = {'form':form}
    return render(request, 'photos/register.html', context)
        

# Create your views here.
@login_required(login_url='login')
def gallery(request):
    user = request.user
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.filter(Category__user=user)
    else:
        photos = Photo.objects.filter(Category__name=category, Category__user=user)
        
    categories = Category.objects.filter(user=user)
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)

@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    context = {'photo':photo}
    return render(request, 'photos/photo.html', context)

@login_required(login_url='login')
def addPhoto(request):
    user = request.user
    
    categories = user.category_set.all()
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
       
        if data['category'] != 'none':
           category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
           category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
           category = None
        photo = Photo.objects.create(
            Category=category,
            description=data['description'],
            image=image,
        )
        return redirect('gallery')
           
    
    context = {'categories': categories}
    return render(request, 'photos/add.html', context)

class deletePhoto(LoginRequiredMixin, DeleteView):
    model = Photo
    template_name = 'photos/photo_confirm_delete.html'
    context_object_name = 'photo'
    success_url = reverse_lazy('gallery')