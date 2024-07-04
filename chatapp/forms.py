from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    roomname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Room Name', 'class': 'form-control padd'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control padd'}))
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control padd'}))

    class Meta:
        model = Room
        fields = ['topic', 'roomname', 'description', 'image']