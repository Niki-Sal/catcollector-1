from django import forms
from .models import Feeding, Cat

class FeedingForm(forms.ModelForm):
    # meta class beacuse that's how django can do it
    class Meta:
        # which model
        model = Feeding
        fields = ['date', 'meal']

# added a catform
class CatForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = ('name', 'breed', 'description', 'age')
