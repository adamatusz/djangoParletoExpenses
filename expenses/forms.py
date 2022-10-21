from django import forms

from .models import Expense


class DateInput(forms.DateInput):
    input_type = 'date'


class ExpenseSearchForm(forms.ModelForm):
    asc_date = forms.BooleanField()
    des_date = forms.BooleanField()
    from_date = forms.DateField(widget=DateInput(attrs={'placeholder': 'from_date'}),
                                label="from:",
                                required=False)
    to_date = forms.DateField(widget=DateInput(attrs={'placeholder': 'to_date'}),
                              label="to:",
                              required=False)

    class Meta:
        model = Expense
        fields = ('category', 'name', 'from_date', 'to_date', 'asc_date', 'des_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['asc_date'].label = 'ascending date'
        self.fields['asc_date'].required = False

        self.fields['des_date'].label = 'descending date'
        self.fields['des_date'].required = False

        self.fields['name'].required = False
        self.fields['name'].widget.attrs['placeholder'] = 'Name'
        self.fields['name'].label = ''

        self.fields['category'].required = False
        self.fields['category'].widget.attrs['placeholder'] = 'category'
        self.fields['category'].label = ''
