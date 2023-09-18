from django.shortcuts import render, redirect
from .models import Category, Photo
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    DeleteView
)


# Create your views here.
def gallery(request):
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(Category__name=category)
        
    categories = Category.objects.all()
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)

def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    context = {'photo':photo}
    return render(request, 'photos/photo.html', context)

def addPhoto(request):
    categories = Category.objects.all()
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

class deletePhoto(DeleteView):
    model = Photo
    template_name = 'photos/photo_confirm_delete.html'
    context_object_name = 'photo'
    success_url = reverse_lazy('gallery')