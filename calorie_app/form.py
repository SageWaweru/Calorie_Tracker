from django import forms
from .models import Food, Image

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['food_name', 'quantity', 'fat', 'carbohydrates', 'protein', 'category']

    def __init__(self, *args, **kwargs):
        super(FoodForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_food_name(self):
            food_name = self.cleaned_data.get('food_name')
            if food_name:
                return food_name.strip().title() 
            return food_name
    
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.visible_fields()[0].field.widget.attrs['class'] = 'form-control'