from django import forms
from locations.models import City
from .models import Gender, Employee


class EmployeeCreationForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'pan_number', 'age', 'gender', 'email','city']

    def __init__(self, *args, **kwargs):
        super(EmployeeCreationForm, self).__init__(*args, **kwargs)
        self.fields['city'].choices = [('0','---')]+[(city.id, city.name) for city in City.objects.all()]
        self.fields['gender'].choices = [('0','---')]+[(gender.id, gender.get_gender_display()) for gender in Gender.objects.all()]
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
