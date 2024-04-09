from django import forms
from .models import ImageUpload

class ImageUploadForm(forms.ModelForm):
    city_choices = [
        ('Нижний Новгород', 'Нижний Новгород'),
        ('Ярославль', 'Ярославль'),
        ('Екатеринбург', 'Екатеринбург'),
        ('Владимир', 'Владимир'),
        # Add more cities as needed
    ]

    city = forms.ChoiceField(choices=city_choices)

    class Meta:
        model = ImageUpload
        fields = ['image', 'city']


class TextForm(forms.ModelForm):
    city_choices = [
        ('Нижний Новгород', 'Нижний Новгород'),
        ('Ярославль', 'Ярославль'),
        ('Екатеринбург', 'Екатеринбург'),
        ('Владимир', 'Владимир'),
        # Add more cities as needed
    ]

    city = forms.ChoiceField(choices=city_choices)
    text_input = forms.CharField(max_length=100)  # Additional input field for caption

    class Meta:
        model = ImageUpload
        fields = ['city', 'text_input']