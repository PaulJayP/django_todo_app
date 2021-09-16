from location.models.city_model import City
from django import forms


class CityForm(forms.ModelForm):

    class Meta:
        model = City
        fields = '__all__'
