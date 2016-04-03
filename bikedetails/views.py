from django.shortcuts import render
from models import BikeDetails
from django.http import HttpResponseRedirect
import json

# Create your views here.
def get_image(request):
    """This function to provide data to show bike images and model"""
    data = [{'model': i.bike_model, 'image': i.image, 'id': i.id} for i in BikeDetails.objects.all()]
    data = {'data': data}
    return render(request, 'show_image.html', data)

def detail_view(request):
    """This Function render the Detail view of Byke"""
    id_ = request.GET['id']
    detail = BikeDetails.objects.get(id=id_)
    data = {'reg_no': detail.bike_reg_no, 'model': detail.bike_model, 'km_driven': detail.km_driven, 'top_speed': detail.top_speed, 'milege': detail.milege, 'fuel_capacity': detail.fuel_tank_capacity, 'max_power': detail.max_power,'image': detail.image}
    return render(request, 'bike_detail.html', data)

def save_details(request):
    """This method to save the bike details"""
    image = request.GET['image']
    bike = BikeDetails.objects.create(bike_reg_no='TN12 RE 8888', bike_model='RoyalEnfield Himalaya', image=image, km_driven=180, top_speed=190, milege=30, fuel_tank_capacity=8.5, max_power=4000)
    return HttpResponseRedirect('/')

from django import forms

class PostForm(forms.Form):
    content = forms.CharField(max_length=256)
    created_at = forms.DateTimeField()
    
def post_form_upload(request):
    if request.method == 'GET':
        form = PostForm()
    else:
        # A POST request: Handle Form Upload
        form = PostForm(request.POST) # Bind data from request.POST into a PostForm
 
        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            content = form.cleaned_data['content']
            created_at = form.cleaned_data['created_at']
            post = m.Post.objects.create(content=content,
                                         created_at=created_at)
            return HttpResponseRedirect(reverse('post_detail',
                                                kwargs={'post_id': post.id}))
 
    return render(request, 'post/post_form_upload.html', {
        'form': form,
    })