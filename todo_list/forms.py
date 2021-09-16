from django import forms

from location.models.city_model import City
from location.models.country_model import Country
from .models import TodoItem


class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = "__all__"
        exclude = ('updated_at', 'completed_at',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()
        self.fields['country'].queryset = Country.objects.all().order_by('name')

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')


class TodoFormUpdate(forms.ModelForm):

    task_complete = forms.BooleanField(
        label='Task complete',
        required=False,
        initial=False
    )

    class Meta:
        model = TodoItem
        fields = ("title", "content", "task_complete", "country", "city")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()
        self.fields['country'].queryset = Country.objects.all().order_by('name')

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')
