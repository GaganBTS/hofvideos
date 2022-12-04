from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.http import Http404,JsonResponse
from django.views import generic
from .models import *
from .forms import *
from django.forms.utils import ErrorList
import urllib
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
YOUTUBE_API_KEY = ''
def home(request):
    recent_halls = Hall.objects.all().order_by('-id')[:3]
    # popular_halls = [Hall.objects.get(pk=1), Hall.objects.get(pk=2), Hall.objects.get(pk=3)]
    return render(request, 'hofvid/home.html', {'recent_halls': recent_halls, 'popular_halls': recent_halls})
@login_required
def dashboard(request):
    hall = Hall.objects.filter(user=request.user)
    return render(request,'hofvid/dashboard.html',{'halls':hall})

class Signup(generic.CreateView):
    form_class= UserCreationForm
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/signup.html'
    def form_valid(self, form):
        view = super(Signup,self).form_valid(form)
        username,password = form.cleaned_data.get('username'),form.cleaned_data.get('password1')
        user = authenticate(username=username,password=password)
        login(self.request,user)
        return view

class CreateHall(LoginRequiredMixin,generic.CreateView):
    model = Hall
    fields = ['title']
    template_name = 'hofvid/create_hall.html'
    success_url = reverse_lazy('dashboard')
    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateHall,self).form_valid(form)
        return redirect('dashboard')
class DetailHall(generic.DetailView):
    model = Hall
    template_name = 'hofvid/detail_hall.html'
class UpdateHall(LoginRequiredMixin,generic.UpdateView):
    model = Hall
    template_name = 'hofvid/update_hall.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')
    def get_object(self):
        hall = super(UpdateHall, self).get_object()
        if not hall.user == self.request.user:
            raise Http404
        return hall

class DeleteHall(LoginRequiredMixin,generic.DeleteView):
    model = Hall
    template_name = 'hofvid/delete_hall.html'
    success_url = reverse_lazy('dashboard')
    def get_object(self):
        hall = super(DeleteHall, self).get_object()
        if not hall.user == self.request.user:
            raise Http404
        return hall
class DeleteVideo(LoginRequiredMixin,generic.DeleteView):
    model = Video
    template_name = 'hofvid/delete_video.html'
    success_url = reverse_lazy('dashboard')
    def get_object(self):
        video = super(DeleteVideo, self).get_object()
        if not video.hall.user == self.request.user:
            raise Http404
        return video
@login_required
def search_video(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        encoded_search_term = search_form.cleaned_data['search_term']
        response = requests.get(
            f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={encoded_search_term}&key={YOUTUBE_API_KEY}')
        return JsonResponse(response.json())
    return JsonResponse({'error': 'Not able to validate form'})
@login_required
def add_video(request,pk):
    form = VideoForm()
    search_form = SearchForm()
    hall= Hall.objects.get(pk=pk)
    if hall.user != request.user:
        raise Http404
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
         video = Video()
         video.hall = hall
         video.url = form.cleaned_data['url']
         parsed_url = urllib.parse.urlparse(video.url)
         video_id = urllib.parse.parse_qs(parsed_url.query).get('v')
         if video_id:
          url = f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={video_id[0]}&key={YOUTUBE_API_KEY}'
          response = requests.get(url=url)
          data = response.json()
          video.title = data['items'][0]['snippet']['title']
          video.youtube_id = video_id[0]
          video.save()
          return redirect('detail_hall',pk)
         else:
          errors = form._errors.setdefault('url',ErrorList())
          errors.append('Need to be a youtube url')

    return render(request,'hofvid/add_video.html',{'form':form,'search_form':search_form,'hall':hall})
