from .models import Video
from django import forms
from django.forms import ModelForm

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields =['url']
        labels = {'title':'Title','youtube_id':'YouTube_Id','url':'YouTube_URL'}


class SearchForm(forms.Form):
    search_term = forms.CharField(max_length=255, label='SEARCH A VIDEO')