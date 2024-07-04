from django import forms
from stories.models import Story
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
import os




class NewStoryForm(forms.ModelForm):
    content = forms.FileField(required=True)
    caption = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder':'caption'}), required=True)
    
    class Meta:
        model = Story
        fields = ['content', 'caption']