from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class BuySellForm(forms.Form):
    price = forms.DecimalField(widget=forms.NumberInput(
        attrs={"readonly":"readonly"}
    ))
    amount = forms.IntegerField(validators=[MinValueValidator(1)])

    def __init__(self, *args, **kwargs):
        max_count = None
        if "max_count" in kwargs:
            max_count = kwargs["max_count"]
            del kwargs["max_count"]
        super().__init__(*args, **kwargs)
        if not max_count is None:
            self.fields["amount"].validators.append(MaxValueValidator(max_count))