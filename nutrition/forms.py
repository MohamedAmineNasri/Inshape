# forms.py
from decimal import Decimal, InvalidOperation
from django import forms
from .models import Nutrition

class NutritionForm(forms.ModelForm):
    class Meta:
        model = Nutrition
        fields = ['name', 'calories', 'protein', 'carbohydrates', 'sugars', 'fats']

    # Additional validation for Decimal fields
    def clean_calories(self):
        return self._validate_decimal('calories')

    def clean_protein(self):
        return self._validate_decimal('protein')

    def clean_carbohydrates(self):
        return self._validate_decimal('carbohydrates')

    def clean_sugars(self):
        return self._validate_decimal('sugars')

    def clean_fats(self):
        return self._validate_decimal('fats')

    # Helper function to ensure the value is a valid decimal
    def _validate_decimal(self, field_name):
        value = self.cleaned_data.get(field_name)
        try:
            return Decimal(value) if value is not None else None
        except (InvalidOperation, ValueError):
            raise forms.ValidationError(f"Please enter a valid decimal number for {field_name}.")
class BarcodeImageForm(forms.Form):
    image = forms.ImageField(label='Upload an image')
class SearchForm(forms.Form):
    query = forms.CharField(label='Search for food', max_length=100)