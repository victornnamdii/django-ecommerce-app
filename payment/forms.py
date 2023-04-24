from django import forms

from datetime import datetime


class PaymentForm(forms.Form):
    name_on_card = forms.CharField(max_length=100, required=True,
                                   widget=forms.TextInput(
                                    attrs={'placeholder': 'John Doe'}
                                    ))
    cardno = forms.CharField(min_length=14, max_length=19, label='Card Number',
                             required=True)
    expirymonth = forms.IntegerField(max_value=12, min_value=1,
                                     label='MM', required=True)
    expiryyear = forms.IntegerField(min_value=datetime.now().year,
                                    label='YYYY', required=True)
    cvv = forms.CharField(max_length=3, required=True,
                          label='CVV')

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        if len(cvv) != 3:
            raise forms.ValidationError('Enter complete CVV')
        return cvv
